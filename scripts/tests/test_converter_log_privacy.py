"""Synthetic source-only privacy contract for PDF conversion/splitting logs.

These checks do not prove runtime privacy, exception-handler safety, client
response confidentiality, access logs, retention, or proxy behavior.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "app/core/src/main/java/stirling/software/SPDF/controller/api"

CONTROLLERS = (
    "converters/ConvertEmlToPDF.java",
    "converters/ConvertSvgToPDF.java",
    "misc/AutoSplitPdfController.java",
    "PosterPdfController.java",
    "SplitPdfBySectionsController.java",
)


def log_calls(source: str):
    """Extract only SLF4J logging invocations without swallowing following code."""
    for match in re.finditer(r"\blog\.(?:error|warn|info|debug|trace)\s*\(", source):
        end = source.find(");", match.end())
        if end < 0:
            raise AssertionError("Unclosed log call")
        yield source[match.start():end + 2]


class ConverterLoggingPrivacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {
            path: (API / path).read_text(encoding="utf-8")
            for path in CONTROLLERS
        }

    def test_no_raw_filename_request_exception_body_or_stacktrace_in_logs(self):
        forbidden = re.compile(
            r"\b(?:originalFilename|baseFilename|errorMessage|filename|fileName)\b"
            r"|\bpdf\.filename\b|\.getOriginalFilename\s*\("
            r"|\.getMessage\s*\(|\brequest\s*(?=,|\))"
            r"|,\s*(?:e|ex|ioe)\s*\)"
        )
        for path, source in self.sources.items():
            calls = list(log_calls(source))
            self.assertGreater(len(calls), 0, path)
            for call in calls:
                # Ignore the fixed literal message; inspect only dynamic data.
                args = re.sub(r'"(?:\\.|[^"\\])*"', '""', call)
                with self.subTest(path=path, call=call[:110]):
                    self.assertNotRegex(args, forbidden)
        self.assertNotIn(
            'ExceptionUtils.logException("PDF poster split process"',
            self.sources["PosterPdfController.java"],
        )

    def test_normal_response_file_names_and_error_response_contract_remain(self):
        eml = self.sources["converters/ConvertEmlToPDF.java"]
        svg = self.sources["converters/ConvertSvgToPDF.java"]
        split = self.sources["SplitPdfBySectionsController.java"]
        auto = self.sources["misc/AutoSplitPdfController.java"]
        poster = self.sources["PosterPdfController.java"]
        self.assertIn('baseFilename + ".pdf"', eml)
        self.assertIn('baseFilename + ".html"', eml)
        self.assertIn('errorResponse(HttpStatus.INTERNAL_SERVER_ERROR, errorMessage)', eml)
        self.assertIn('WebResponseUtils.pdfFileToWebResponse', svg)
        self.assertIn('WebResponseUtils.zipFileToWebResponse(zipTempFile, filename + ".zip")', split)
        self.assertIn('WebResponseUtils.zipFileToWebResponse(outputTempFile, filename + ".zip")', auto)
        self.assertIn('new ZipEntry(filename + "_poster.pdf")', poster)

    def test_deterministic_diagnostic_context_is_preserved(self):
        self.assertIn('Auto-split starting: size={} bytes, duplexMode={}', self.sources["misc/AutoSplitPdfController.java"])
        self.assertIn('Generated output PDF with {} pages', self.sources["PosterPdfController.java"])
        self.assertIn('Error creating section {} for page {} ({})', self.sources["SplitPdfBySectionsController.java"])
        self.assertIn('Email to PDF conversion failed ({})', self.sources["converters/ConvertEmlToPDF.java"])


if __name__ == "__main__":
    unittest.main()
