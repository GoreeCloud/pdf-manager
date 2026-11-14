"""Source-only logging privacy contract for scanner and Office conversion.

This is not runtime log capture or proof against access/proxy URL logging.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "app/core/src/main/java/stirling/software/SPDF/controller/api"


def calls(code):
    for m in re.finditer(r"\blog\.(?:warn|error|info|debug|trace)\s*\(", code):
        end = code.find(");", m.end())
        if end < 0:
            raise AssertionError("Unclosed SLF4J call")
        yield code[m.start():end + 2]


class ScannerOfficeLogPrivacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scanner = (API / "misc/MobileScannerController.java").read_text(encoding="utf-8")
        cls.office = (API / "converters/ConvertOfficeController.java").read_text(encoding="utf-8")

    def test_no_session_filename_temp_path_exception_message_or_raw_throwable_logged(self):
        forbidden = re.compile(
            r"\b(?:sessionId|filename|inputPath)\b"
            r"|\.getOriginalFilename\s*\(|\.getMessage\s*\("
            r"|\brequest\s*(?=,|\))|,\s*(?:e|ex)\s*\)"
        )
        for name, source in (("scanner", self.scanner), ("office", self.office)):
            messages = list(calls(source))
            self.assertGreater(len(messages), 0, name)
            for message in messages:
                args = re.sub(r'"(?:\\.|[^"\\])*"', '""', message)
                with self.subTest(controller=name, call=message[:115]):
                    self.assertNotRegex(args, forbidden)

    def test_scanner_response_contract_and_intended_counts_unchanged(self):
        self.assertIn('response.put("sessionId", sessionInfo.getSessionId())', self.scanner)
        self.assertIn('response.put("sessionId", sessionId)', self.scanner)
        self.assertIn('response.put("filesUploaded", files.size())', self.scanner)
        self.assertIn('mobileScannerService.getFile(sessionId, filename)', self.scanner)
        self.assertIn('mobileScannerService.deleteSession(sessionId)', self.scanner)
        self.assertIn('Mobile scanner uploaded {} files', self.scanner)
        self.assertIn('e.isServerCapacity()', self.scanner)

    def test_office_failure_still_retries_without_exposing_temp_path(self):
        self.assertIn('officeToPdfService.canFallBack(e)', self.office)
        self.assertIn('Files.deleteIfExists(outputPath)', self.office)
        self.assertIn('Unoconvert command failed ({})', self.office)
        self.assertIn('Stirling Office Convert failed ({})', self.office)


if __name__ == "__main__":
    unittest.main()
