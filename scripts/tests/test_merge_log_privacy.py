"""Offline static privacy contract for PDF merge logs; not runtime log attestation."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "app/core/src/main/java/stirling/software/SPDF/controller/api/MergeController.java"


class MergeLogPrivacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text()

    def test_no_parser_exception_message_logged(self):
        self.assertNotIn(".getMessage()", self.source)
        self.assertIn("e.getClass().getSimpleName()", self.source)

    def test_no_raw_exception_stack_or_unsafe_shared_exception_logger(self):
        self.assertNotIn("ExceptionUtils.logException(", self.source)
        self.assertNotIn('log.error("Error in merge pdf process", ex)', self.source)
        self.assertIn('log.error("PDF merge failed ({})", ex.getClass().getSimpleName())', self.source)

    def test_user_original_file_order_name_not_logged(self):
        self.assertNotIn('log.debug("Filename from order list not found', self.source)
        self.assertIn("Unmatched upload order reference", self.source)

    def test_client_sort_field_not_logged(self):
        self.assertNotIn('log.info("Sorting files based on sortType: {}", request.getSortType())',
                         self.source)
        self.assertIn("Applying selected merge file sorting mode", self.source)

    def test_synthetic_error_conditions_still_handled(self):
        self.assertIn("ExceptionUtils.createMultiplePdfCorruptedException", self.source)
        self.assertIn("ExceptionUtils.createFileNullOrEmptyException()", self.source)
        self.assertIn("finally {", self.source)
        self.assertIn("tempFileManager.deleteTempFile(file)", self.source)


if __name__ == "__main__":
    unittest.main()
