"""Offline negative-upload contracts: synthetic PDFs and mocked HTTP, no network."""
import io
import json
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import smoke_core_http as smoke


class MockHealth(io.BytesIO):
    status = 200


def fake_http(bad_code=400, health_status="UP"):
    calls = []
    def request(url, *, data=None, content_type=""):
        calls.append((url, data, content_type))
        if data is not None:
            if bad_code == 200:
                r = MockHealth(b"%PDF-1.4")
                r.status = 200
                return r
            return_error = urllib.error.HTTPError(
                url, bad_code, "synthetic upload error", {}, io.BytesIO(b"synthetic error body")
            )
            raise return_error
        return MockHealth(json.dumps({"status": health_status}).encode())
    return request, calls


class InvalidUploadTests(unittest.TestCase):
    def test_malformed_input_returns_400_and_health_recovers(self):
        request, calls = fake_http()
        with patch.object(smoke, "http_open", side_effect=request):
            smoke.assert_malformed_pdf_is_rejected_and_server_remains_healthy(
                "http://127.0.0.1:12345"
            )
        self.assertEqual(len(calls), 2)
        self.assertIn(b"Alpha", calls[0][1])
        self.assertIn(b"truncated fixture", calls[0][1])
        self.assertEqual(calls[0][2].split(";")[0], "multipart/form-data")
        self.assertTrue(calls[1][0].endswith("/api/v1/info/health"))

    def test_invalid_pdf_must_not_return_success(self):
        request, _ = fake_http(bad_code=200)
        with patch.object(smoke, "http_open", side_effect=request):
            with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
                smoke.assert_malformed_pdf_is_rejected_and_server_remains_healthy(
                    "http://127.0.0.1:12345"
                )

    def test_non_client_status_not_allowed(self):
        for status in (422, 500, 503):
            request, _ = fake_http(bad_code=status)
            with patch.object(smoke, "http_open", side_effect=request):
                with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
                    smoke.assert_malformed_pdf_is_rejected_and_server_remains_healthy(
                        "http://127.0.0.1:12345"
                    )

    def test_unhealthy_server_is_rejected(self):
        request, _ = fake_http(health_status="DOWN")
        with patch.object(smoke, "http_open", side_effect=request):
            with self.assertRaisesRegex(RuntimeError, "remain healthy"):
                smoke.assert_malformed_pdf_is_rejected_and_server_remains_healthy(
                    "http://127.0.0.1:12345"
                )

    def test_missing_file_upload_is_rejected_and_contains_no_data(self):
        request, calls = fake_http(bad_code=400)
        with patch.object(smoke, "http_open", side_effect=request):
            smoke.assert_no_file_merge_is_rejected("http://127.0.0.1:12345")
        self.assertEqual(len(calls), 1)
        self.assertTrue(calls[0][0].endswith("/merge-pdfs"))
        self.assertEqual(calls[0][1], b"--goreecloud-ci-no-files-boundary--\r\n")
        self.assertNotIn(b"filename=", calls[0][1])
        self.assertEqual(calls[0][2], "multipart/form-data; boundary=goreecloud-ci-no-files-boundary")

    def test_missing_file_request_cannot_succeed(self):
        request, _ = fake_http(bad_code=200)
        with patch.object(smoke, "http_open", side_effect=request):
            with self.assertRaisesRegex(RuntimeError, "expected 400"):
                smoke.assert_no_file_merge_is_rejected("http://127.0.0.1:12345")

    def test_oversized_synthetic_pdf_rejected_as_413(self):
        request, calls = fake_http(bad_code=413)
        with patch.object(smoke, "http_open", side_effect=request):
            smoke.assert_oversized_synthetic_upload_is_rejected(
                "http://127.0.0.1:12345"
            )
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1].count(b"%PDF-"), 2)
        self.assertLess(len(calls[0][1]), 64 * 1024)
        self.assertGreater(len(calls[0][1]), 32 * 1024)
        self.assertNotIn(b"password=", calls[0][1])
        self.assertIn("boundary=", calls[0][2])

    def test_oversized_upload_must_not_succeed_or_be_server_error(self):
        for code in (200, 400, 500, 503):
            request, _ = fake_http(bad_code=code)
            with patch.object(smoke, "http_open", side_effect=request):
                with self.assertRaisesRegex(RuntimeError, "required HTTP 413"):
                    smoke.assert_oversized_synthetic_upload_is_rejected(
                        "http://127.0.0.1:12345"
                    )

    def test_aggregate_exceeded_rejected_even_when_each_file_is_small(self):
        request, calls = fake_http(bad_code=413)
        with patch.object(smoke, "http_open", side_effect=request):
            smoke.assert_aggregate_synthetic_upload_is_rejected(
                "http://127.0.0.1:12345")
        self.assertEqual(len(calls), 1)
        self.assertGreater(len(calls[0][1]), 64 * 1024)
        self.assertLess(len(calls[0][1]), 72 * 1024)
        self.assertEqual(calls[0][1].count(b"%PDF-"), 2)
        self.assertIn("multipart/form-data; boundary=", calls[0][2])

    def test_aggregate_limit_client_error_cannot_be_success(self):
        request, _ = fake_http(bad_code=200)
        with patch.object(smoke, "http_open", side_effect=request):
            with self.assertRaisesRegex(RuntimeError, "required HTTP 413"):
                smoke.assert_aggregate_synthetic_upload_is_rejected(
                    "http://127.0.0.1:12345")

    def test_wrong_number_of_docs_rejected_before_request(self):
        for docs in ((), (smoke.synthetic_pdf("Alpha"),)):
            with self.assertRaisesRegex(ValueError, "exactly two"):
                smoke.multipart_pdf_payload(docs)


if __name__ == "__main__":
    unittest.main()
