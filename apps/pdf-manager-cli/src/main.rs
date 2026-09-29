//! Development command-line interface for GoreeCloud PDF Manager.
//!
//! This is not the planned end-user application. It exposes the first bounded
//! PDF preflight capability for development, testing, and future service
//! integration.

#![forbid(unsafe_code)]

use goreecloud_pdf_core::{DEFAULT_MAX_INPUT_BYTES, PreflightError, preflight_path};
use std::borrow::Cow;
use std::env;
use std::ffi::OsString;
use std::path::PathBuf;
use std::process::ExitCode;

fn main() -> ExitCode {
    match run(env::args_os().collect()) {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("error: {error}");
            ExitCode::from(2)
        }
    }
}

fn run(args: Vec<OsString>) -> Result<(), String> {
    let program: Cow<'_, str> = args
        .first()
        .map_or_else(|| Cow::Borrowed("pdf-manager-cli"), |value| value.to_string_lossy());

    if args.len() == 1 {
        print_help(&program);
        return Ok(());
    }

    let command = args[1].to_string_lossy();
    match command.as_ref() {
        "inspect" => run_inspect(&args[2..]),
        "-h" | "--help" | "help" => {
            print_help(&program);
            Ok(())
        }
        "-V" | "--version" | "version" => {
            println!("pdf-manager-cli {}", env!("CARGO_PKG_VERSION"));
            Ok(())
        }
        _ => Err(format!(
            "unknown command {command}; run {program} --help for usage"
        )),
    }
}

fn run_inspect(args: &[OsString]) -> Result<(), String> {
    if args.is_empty() {
        return Err("inspect requires a PDF path".to_owned());
    }

    let path = PathBuf::from(&args[0]);
    let mut max_input_bytes = DEFAULT_MAX_INPUT_BYTES;
    let mut index = 1;

    while index < args.len() {
        let option = args[index].to_string_lossy();
        match option.as_ref() {
            "--max-bytes" => {
                let value = args
                    .get(index + 1)
                    .ok_or_else(|| "--max-bytes requires an integer value".to_owned())?;
                max_input_bytes = value
                    .to_string_lossy()
                    .parse::<u64>()
                    .map_err(|_| "--max-bytes must be a non-negative integer".to_owned())?;
                index += 2;
            }
            _ => {
                return Err(format!("unknown inspect option {option}"));
            }
        }
    }

    let result = preflight_path(&path, max_input_bytes).map_err(format_preflight_error)?;

    println!("pdf_version={}", result.version());
    println!("size_bytes={}", result.size_bytes());
    println!("header_offset={}", result.header_offset());
    println!("eof_marker_present={}", result.eof_marker_present());
    Ok(())
}

fn format_preflight_error(error: PreflightError) -> String {
    error.to_string()
}

fn print_help(program: &str) {
    println!(
        "{program} — GoreeCloud PDF Manager development CLI\n\n\
         Usage:\n  {program} inspect <path> [--max-bytes <bytes>]\n  \
         {program} --version\n\n\
         The inspect command performs bounded structural preflight only. It does\n\
         not establish that a document is safe, sanitized, or fully valid."
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn help_without_arguments_succeeds() {
        let args = vec![OsString::from("pdf-manager-cli")];

        assert!(run(args).is_ok());
    }

    #[test]
    fn inspect_requires_a_path() {
        let args = vec![
            OsString::from("pdf-manager-cli"),
            OsString::from("inspect"),
        ];

        assert_eq!(run(args).unwrap_err(), "inspect requires a PDF path");
    }

    #[test]
    fn unknown_commands_fail() {
        let args = vec![OsString::from("pdf-manager-cli"), OsString::from("nope")];

        assert!(run(args).unwrap_err().contains("unknown command"));
    }
}
