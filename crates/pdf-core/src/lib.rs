//! Security-conscious PDF input preflight for `GoreeCloud` PDF Manager.
//!
//! This crate intentionally uses only the Rust standard library. The initial
//! boundary performs bounded structural hints before a future PDF engine is
//! allowed to parse untrusted input. Preflight is not a complete PDF validator
//! and must not be represented as sanitization, malware scanning, or proof that
//! a document is safe.

#![forbid(unsafe_code)]

use std::error::Error;
use std::fmt;
use std::fs::File;
use std::io::{self, Read, Seek, SeekFrom};
use std::path::Path;

/// Default maximum input size accepted by preflight: 512 MiB.
pub const DEFAULT_MAX_INPUT_BYTES: u64 = 512 * 1024 * 1024;

const HEADER_SCAN_BYTES: usize = 1024;
const EOF_SCAN_BYTES: usize = 2048;
const PDF_HEADER: &[u8] = b"%PDF-";
const PDF_EOF_MARKER: &[u8] = b"%%EOF";

/// Bounded structural observations collected before full PDF parsing.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PdfPreflight {
    size_bytes: u64,
    header_offset: usize,
    version: String,
    eof_marker_present: bool,
}

impl PdfPreflight {
    /// Returns the observed input size.
    #[must_use]
    pub const fn size_bytes(&self) -> u64 {
        self.size_bytes
    }

    /// Returns the byte offset where the PDF header begins.
    #[must_use]
    pub const fn header_offset(&self) -> usize {
        self.header_offset
    }

    /// Returns the three-character PDF version token observed in the header.
    #[must_use]
    pub fn version(&self) -> &str {
        &self.version
    }

    /// Returns whether an EOF marker was observed in the bounded tail scan.
    ///
    /// This is only a structural hint. Its presence does not establish that a
    /// document is valid, safe, complete, or unmodified.
    #[must_use]
    pub const fn eof_marker_present(&self) -> bool {
        self.eof_marker_present
    }
}

/// Errors raised while performing bounded PDF preflight.
#[derive(Debug)]
pub enum PreflightError {
    /// The input exceeds the configured preflight size limit.
    InputTooLarge {
        /// Observed input size.
        size_bytes: u64,
        /// Configured maximum accepted size.
        limit_bytes: u64,
    },
    /// A PDF header was not found in the bounded header scan.
    PdfHeaderNotFound,
    /// A PDF header marker was found but the following version token was invalid.
    InvalidVersion,
    /// An operating-system or filesystem I/O operation failed.
    Io(io::Error),
}

impl fmt::Display for PreflightError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InputTooLarge {
                size_bytes,
                limit_bytes,
            } => write!(
                f,
                "input size {size_bytes} bytes exceeds the configured limit of {limit_bytes} bytes"
            ),
            Self::PdfHeaderNotFound => write!(
                f,
                "PDF header was not found within the first {HEADER_SCAN_BYTES} bytes"
            ),
            Self::InvalidVersion => write!(f, "PDF header contains an invalid version token"),
            Self::Io(error) => write!(f, "I/O error during PDF preflight: {error}"),
        }
    }
}

impl Error for PreflightError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
            Self::InputTooLarge { .. } | Self::PdfHeaderNotFound | Self::InvalidVersion => None,
        }
    }
}

impl From<io::Error> for PreflightError {
    fn from(error: io::Error) -> Self {
        Self::Io(error)
    }
}

/// Performs bounded preflight on a filesystem path.
///
/// The function checks the file size before reading, scans at most the first
/// 1024 bytes for a PDF header, parses a three-character version token, and
/// scans at most the final 2048 bytes for an EOF marker.
///
/// # Errors
///
/// Returns an input-too-large error when the file exceeds the configured
/// maximum, a structural error when the bounded header inspection fails, or
/// an I/O preflight error when filesystem operations fail.
pub fn preflight_path(
    path: impl AsRef<Path>,
    max_input_bytes: u64,
) -> Result<PdfPreflight, PreflightError> {
    let mut file = File::open(path)?;
    let size_bytes = file.metadata()?.len();
    ensure_size_within_limit(size_bytes, max_input_bytes)?;

    let head_len = bounded_len(size_bytes, HEADER_SCAN_BYTES);
    let mut head = vec![0_u8; head_len];
    file.read_exact(&mut head)?;

    let tail_len = bounded_len(size_bytes, EOF_SCAN_BYTES);
    let mut tail = vec![0_u8; tail_len];
    if tail_len > 0 {
        let tail_offset = i64::try_from(tail_len).unwrap_or(i64::MAX);
        file.seek(SeekFrom::End(-tail_offset))?;
        file.read_exact(&mut tail)?;
    }

    inspect_windows(size_bytes, &head, &tail)
}

/// Performs the same bounded preflight logic against in-memory bytes.
///
/// This is useful for tests and for future adapters that already own a bounded
/// byte buffer. It does not copy or retain the input bytes.
///
/// # Errors
///
/// Returns an input-too-large error when the input exceeds the configured
/// maximum, a missing-header error when no header is found in the first 1024
/// bytes, or an invalid-version error when the header version token is
/// malformed.
pub fn preflight_bytes(bytes: &[u8], max_input_bytes: u64) -> Result<PdfPreflight, PreflightError> {
    let size_bytes = u64::try_from(bytes.len()).unwrap_or(u64::MAX);
    ensure_size_within_limit(size_bytes, max_input_bytes)?;

    let head_end = bytes.len().min(HEADER_SCAN_BYTES);
    let tail_start = bytes.len().saturating_sub(EOF_SCAN_BYTES);
    inspect_windows(size_bytes, &bytes[..head_end], &bytes[tail_start..])
}

fn ensure_size_within_limit(size_bytes: u64, max_input_bytes: u64) -> Result<(), PreflightError> {
    if size_bytes > max_input_bytes {
        return Err(PreflightError::InputTooLarge {
            size_bytes,
            limit_bytes: max_input_bytes,
        });
    }
    Ok(())
}

fn bounded_len(size_bytes: u64, bound: usize) -> usize {
    let bound_u64 = u64::try_from(bound).unwrap_or(u64::MAX);
    usize::try_from(size_bytes.min(bound_u64)).unwrap_or(bound)
}

fn inspect_windows(
    size_bytes: u64,
    head: &[u8],
    tail: &[u8],
) -> Result<PdfPreflight, PreflightError> {
    let header_offset = find_subslice(head, PDF_HEADER).ok_or(PreflightError::PdfHeaderNotFound)?;
    let version = parse_version(head, header_offset)?;
    let eof_marker_present = find_subslice(tail, PDF_EOF_MARKER).is_some();

    Ok(PdfPreflight {
        size_bytes,
        header_offset,
        version,
        eof_marker_present,
    })
}

fn parse_version(head: &[u8], header_offset: usize) -> Result<String, PreflightError> {
    let version_start = header_offset
        .checked_add(PDF_HEADER.len())
        .ok_or(PreflightError::InvalidVersion)?;
    let version_end = version_start
        .checked_add(3)
        .ok_or(PreflightError::InvalidVersion)?;
    let version = head
        .get(version_start..version_end)
        .ok_or(PreflightError::InvalidVersion)?;

    let valid = version[0].is_ascii_digit() && version[1] == b'.' && version[2].is_ascii_digit();

    if !valid {
        return Err(PreflightError::InvalidVersion);
    }

    std::str::from_utf8(version)
        .map(str::to_owned)
        .map_err(|_| PreflightError::InvalidVersion)
}

fn find_subslice(haystack: &[u8], needle: &[u8]) -> Option<usize> {
    if needle.is_empty() {
        return Some(0);
    }
    haystack
        .windows(needle.len())
        .position(|window| window == needle)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn accepts_pdf_header_at_start_and_reports_eof_hint() {
        let bytes = b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n";

        let result = preflight_bytes(bytes, 1024).unwrap();

        assert_eq!(
            result.size_bytes(),
            u64::try_from(bytes.len()).expect("test fixture length fits in u64")
        );
        assert_eq!(result.header_offset(), 0);
        assert_eq!(result.version(), "1.7");
        assert!(result.eof_marker_present());
    }

    #[test]
    fn accepts_header_within_bounded_prefix() {
        let mut bytes = vec![b' '; 32];
        bytes.extend_from_slice(b"%PDF-2.0\n%%EOF");

        let result = preflight_bytes(&bytes, 1024).unwrap();

        assert_eq!(result.header_offset(), 32);
        assert_eq!(result.version(), "2.0");
    }

    #[test]
    fn rejects_missing_pdf_header() {
        let error = preflight_bytes(b"not a pdf", 1024).unwrap_err();

        assert!(matches!(error, PreflightError::PdfHeaderNotFound));
    }

    #[test]
    fn rejects_invalid_version_token() {
        let error = preflight_bytes(b"%PDF-one\n%%EOF", 1024).unwrap_err();

        assert!(matches!(error, PreflightError::InvalidVersion));
    }

    #[test]
    fn enforces_size_limit_before_structural_acceptance() {
        let bytes = b"%PDF-1.7\n%%EOF";
        let error = preflight_bytes(bytes, 4).unwrap_err();

        assert!(matches!(
            error,
            PreflightError::InputTooLarge {
                size_bytes: 14,
                limit_bytes: 4
            }
        ));
    }

    #[test]
    fn missing_eof_marker_is_reported_as_hint() {
        let result = preflight_bytes(b"%PDF-1.4\n1 0 obj\n", 1024).unwrap();

        assert!(!result.eof_marker_present());
    }

    #[test]
    fn header_outside_scan_window_is_rejected() {
        let mut bytes = vec![0_u8; HEADER_SCAN_BYTES + 1];
        bytes.extend_from_slice(b"%PDF-1.7\n%%EOF");

        let error = preflight_bytes(&bytes, 4096).unwrap_err();

        assert!(matches!(error, PreflightError::PdfHeaderNotFound));
    }
}
