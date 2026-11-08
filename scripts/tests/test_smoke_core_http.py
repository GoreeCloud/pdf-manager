"""Offline tests of synthetic PDF fixture and loopback-only request policy."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import smoke_core_http as smoke


class SyntheticSmokeTests(unittest.TestCase):
    def test_pdf_header_xref_and_offsets(self):
        pdf = smoke.synthetic_pdf("Alpha")
        self.assertTrue(pdf.startswith(b"%PDF-1.4"))
        self.assertTrue(pdf.rstrip().endswith(b"%%EOF"))
        self.assertIn(b"/Type /Page ", pdf)
        startxref = int(re.search(rb"startxref\n(\d+)\n", pdf).group(1))
        self.assertEqual(pdf[startxref:startxref + 4], b"xref")
        for match in re.finditer(rb"(?m)^(\d+) 0 obj\n", pdf):
            self.assertTrue(pdf[match.start():].startswith(match.group(0)))

    def test_multipart_contains_only_synthetic_pdf_parts(self):
        body, ctype = smoke.multipart_pdf_payload()
        self.assertIn("multipart/form-data; boundary=", ctype)
        self.assertEqual(body.count(b'filename="synthetic-'), 2)
        self.assertEqual(body.count(b"%PDF-1.4"), 2)
        self.assertIn(b"Alpha", body)
        self.assertIn(b"Beta", body)
        self.assertNotIn(b"Content-Disposition: form-data; name=\"url\"", body)

    def test_rejects_arbitrary_fixture_labels(self):
        for value in ("A)", "A/B", "too long and with spaces", "", "x"*21):
            with self.assertRaises(ValueError):
                smoke.synthetic_pdf(value)

    def test_http_requests_cannot_escape_loopback(self):
        for url in (
            "http://localhost:9999",
            "http://192.168.1.1:8080",
            "https://127.0.0.1:8443",
            "http://127.0.0.1.evil.example:8080",
            "http://127.0.0.1:8000@evil.example/",
            "http://user:secret@127.0.0.1:8080/",
        ):
            with self.assertRaises(ValueError):
                smoke.http_open(url)

    def test_missing_jar_is_refused_without_starting_java(self):
        with self.assertRaisesRegex(ValueError, "regular core JAR"):
            smoke.smoke_core_jar(Path("/nonexistent/core.jar"), "/usr/bin/java")

    def test_ephemeral_port_is_valid(self):
        port = smoke.select_loopback_port()
        self.assertGreaterEqual(port, 1)
        self.assertLessEqual(port, 65535)


if __name__ == "__main__":
    unittest.main()
