"""Fail-closed contract tests for real merged-PDF semantic inspection.

No PDF tools are invoked in these unit tests; all subprocess responses are mocked.
"""
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import smoke_core_http as smoke

# Valid shape is irrelevant here because Poppler output is mocked.
BOUND_PDF = b"%PDF-1.4\n" + b"x" * 320
TRUSTED_BINARY = sys.executable


def cli_result(output: bytes, returncode: int = 0):
    return subprocess.CompletedProcess(args=["synthetic"], returncode=returncode, stdout=output, stderr=b"")


class SemanticSmokeTests(unittest.TestCase):
    def check_responses(self, info: bytes = b"Pages:           2\n", text: bytes = b"Alpha\n\fBeta\n\f"):
        with patch.object(smoke.subprocess, "run", side_effect=[cli_result(info), cli_result(text)]) as mocked:
            result = smoke.inspect_synthetic_merge_result(BOUND_PDF, TRUSTED_BINARY, TRUSTED_BINARY)
        self.assertEqual(mocked.call_count, 2)
        for call in mocked.call_args_list:
            self.assertEqual(call.kwargs["input"], BOUND_PDF)
            self.assertEqual(call.kwargs["timeout"], 12)
            self.assertFalse(call.kwargs["check"])
            self.assertNotIn("shell", call.kwargs)
        return result

    def test_two_pages_in_order_accepted(self):
        result = self.check_responses()
        self.assertEqual(result["pages"], 2)
        self.assertTrue(result["synthetic_page_content_and_order_verified"])

    def test_single_page_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "exactly two"):
            self.check_responses(info=b"Pages: 1\n")

    def test_wrong_order_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "preserve both pages"):
            self.check_responses(text=b"Beta\n\fAlpha\n\f")

    def test_missing_text_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "preserve both pages"):
            self.check_responses(text=b"Alpha\n\f\f")

    def test_extra_page_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "exactly two"):
            self.check_responses(info=b"Pages: 3\n")

    def test_missing_or_ambiguous_page_metadata_rejected(self):
        for sample in (b"Page count not available\n", b"Pages: 2\nPages: 2\n"):
            with self.assertRaisesRegex(RuntimeError, "exactly two"):
                self.check_responses(info=sample)

    def test_tool_failure_does_not_leak_contents(self):
        fail = cli_result(b"Sensitive-Synthetic-Tool-Output", 1)
        with patch.object(smoke.subprocess, "run", return_value=fail):
            with self.assertRaisesRegex(RuntimeError, "verifier rejected") as cm:
                smoke.inspect_synthetic_merge_result(BOUND_PDF, TRUSTED_BINARY, TRUSTED_BINARY)
        self.assertNotIn("Sensitive-Synthetic-Tool-Output", str(cm.exception))

    def test_timeout_is_bounded(self):
        with patch.object(smoke.subprocess, "run", side_effect=subprocess.TimeoutExpired("pdfinfo", 12)):
            with self.assertRaisesRegex(RuntimeError, "timed out"):
                smoke.inspect_synthetic_merge_result(BOUND_PDF, TRUSTED_BINARY, TRUSTED_BINARY)

    def test_oversized_tool_output_is_rejected(self):
        with patch.object(smoke.subprocess, "run", return_value=cli_result(b"Pages: 2\n" + b"x" * 8200)):
            with self.assertRaisesRegex(RuntimeError, "oversized output"):
                smoke.inspect_synthetic_merge_result(BOUND_PDF, TRUSTED_BINARY, TRUSTED_BINARY)

    def test_invalid_text_encoding_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "not decodable"):
            self.check_responses(text=b"Alpha\n\f\xffBeta\n\f")

    def test_invalid_pdf_input_is_rejected_before_spawning(self):
        for malformed in (b"", b"x" * 200, b"%PDF-1.4" + b"x" * (smoke.MAX_RESULT_BYTES + 1)):
            with patch.object(smoke.subprocess, "run") as run:
                with self.assertRaisesRegex(ValueError, "bounded PDF"):
                    smoke.inspect_synthetic_merge_result(malformed, TRUSTED_BINARY, TRUSTED_BINARY)
                run.assert_not_called()

    def test_relative_verifier_paths_are_rejected(self):
        with patch.object(smoke.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "absolute executable"):
                smoke.inspect_synthetic_merge_result(BOUND_PDF, "pdfinfo", "pdftotext")
            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
