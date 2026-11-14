"""Read-only static log-privacy checks; not JVM runtime log attestation."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "app/core/src/main/java/stirling/software/SPDF/controller/api"


class ChapterRearrangeLogPrivacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (API / "SplitPdfByChaptersController.java").read_text(encoding="utf-8")
        cls.rearrange = (API / "RearrangePagesPDFController.java").read_text(encoding="utf-8")

    def test_source_filename_and_bookmark_titles_not_logged(self):
        self.assertNotIn('log.warn("No outline found for {}"', self.chapter)
        self.assertNotIn('"{}::::{} to {}"', self.chapter)
        self.assertIn('Chapter split identified {} bookmarks', self.chapter)
        self.assertIn('Uploaded PDF does not contain a usable bookmark outline', self.chapter)

    def test_generated_zip_paths_and_chapter_file_names_not_logged(self):
        self.assertNotIn('"Successfully created zip file with split documents: {}"', self.chapter)
        self.assertNotIn('log.debug("Wrote split document {} to zip file", fileName)', self.chapter)
        self.assertEqual(self.chapter.count('log.debug("Wrote split PDF chapter to ZIP");'), 2)
        self.assertIn('log.info("Created ZIP with split PDF documents");', self.chapter)

    def test_rearrange_never_logs_raw_exception_stack_or_parser_text(self):
        self.assertNotIn('log.error("Invalid duplicate count specified", e)', self.rearrange)
        self.assertNotIn('ExceptionUtils.logException("document rearrangement", e)', self.rearrange)
        self.assertIn('log.error("PDF page rearrangement failed ({})", e.getClass().getSimpleName())', self.rearrange)

    def test_public_response_filename_processing_remains_present(self):
        self.assertIn('WebResponseUtils.zipFileToWebResponse(zipTempFile, filename + ".zip")', self.chapter)
        self.assertIn('file.getOriginalFilename()', self.chapter)
        self.assertIn('WebResponseUtils.pdfDocToWebResponse(', self.rearrange)
        self.assertIn('pdfFile.getOriginalFilename()', self.rearrange)


if __name__ == "__main__":
    unittest.main()
