#!/usr/bin/env python3
"""Run the unreleased core JAR on loopback with synthetic PDFs only.

An isolated CI smoke test, not a production deployment, sandbox, security
assessment, full PDF correctness test, or authorized external service.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import urllib.parse
from pathlib import Path

MAX_RESULT_BYTES = 8 * 1024 * 1024


def synthetic_pdf(label: str) -> bytes:
    """Produce a tiny, valid one-page PDF 1.4 without third-party packages."""
    if not (label.isascii() and label.isalpha() and 1 <= len(label) <= 20):
        raise ValueError("Synthetic fixture labels must be short ASCII letters")
    text = f"BT /F1 12 Tf 35 150 Td ({label}) Tj ET".encode("ascii")
    parts = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(text)).encode() + b" >>\nstream\n" + text + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, data in enumerate(parts, start=1):
        offsets.append(len(result))
        result.extend(f"{index} 0 obj\n".encode("ascii") + data + b"\nendobj\n")
    xref_position = len(result)
    result.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010} 00000 n \n".encode())
    result.extend(
        b"trailer\n<< /Size "
        + str(len(offsets)).encode()
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_position).encode()
        + b"\n%%EOF\n"
    )
    return bytes(result)


def multipart_pdf_payload(
    documents: tuple[bytes, bytes] | None = None,
) -> tuple[bytes, str]:
    """Encode exactly two controlled synthetic PDFs as multipart form data."""
    if documents is None:
        documents = (synthetic_pdf("Alpha"), synthetic_pdf("Beta"))
    if len(documents) != 2:
        raise ValueError("The smoke fixture requires exactly two documents")
    boundary = "goreecloud-ci-synthetic-pdf-boundary"
    chunks = []
    for index, pdf in enumerate(documents, start=1):
        chunks.extend((
            f"--{boundary}\r\n".encode(),
            (f'Content-Disposition: form-data; name="fileInput"; '
             f'filename="synthetic-{index}.pdf"\r\n').encode(),
            b"Content-Type: application/pdf\r\n\r\n",
            pdf,
            b"\r\n",
        ))
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def select_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def http_open(url: str, *, data: bytes | None = None, content_type: str = ""):
    address = urllib.parse.urlsplit(url)
    if (address.scheme != "http" or address.hostname != "127.0.0.1"
            or address.username is not None or address.password is not None
            or address.fragment or not address.port):
        raise ValueError("Only direct HTTP 127.0.0.1 loopback requests are permitted")
    headers = {"User-Agent": "GoreeCloud-Nonpublishing-Core-Smoke/1"}
    if content_type:
        headers["Content-Type"] = content_type
    request = urllib.request.Request(url, data=data, headers=headers)
    # Do not honor proxies or follow redirects (which might escape loopback).
    class RejectRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, request, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), RejectRedirect())
    return opener.open(request, timeout=25)



def startup_error_summary(path: Path) -> str:
    """Return only bounded redacted error markers; never publish a whole log."""
    if not path.is_file():
        return "no startup log available"
    with path.open("rb") as source:
        source.seek(0, 2)
        source.seek(max(0, source.tell() - 256 * 1024))
        tail = source.read().decode("utf-8", errors="replace")
    markers = ("exception", "caused by:", "error", "failed to", "application run failed")
    entries = []
    for raw in tail.splitlines():
        if not any(marker in raw.lower() for marker in markers):
            continue
        clean = re.sub(r"\x1b\[[0-9;]*m", "", raw)
        clean = re.sub(
            r"(?i)\b(password|secret|token|api[_-]?key|authorization)\s*[:=]\s*[^\s,;]+",
            r"\1=<redacted>", clean,
        )
        clean = re.sub(r"https?://\S+", "<url-redacted>", clean)
        entries.append(clean[-220:])
    return " | ".join(entries[-8:]) if entries else "no classified startup error found"


def inspect_synthetic_merge_result(
    merged: bytes, pdfinfo: str, pdftotext: str
) -> dict[str, object]:
    """Verify the real response is a readable two-page PDF with ordered fixture text.

    Poppler is used only as an external CI verification tool, never bundled,
    deployed, or asked to parse actual user documents by this script.
    """
    if len(merged) < 200 or len(merged) > MAX_RESULT_BYTES or not merged.startswith(b"%PDF-"):
        raise ValueError("Synthetic merge response must be bounded PDF bytes")
    for executable in (pdfinfo, pdftotext):
        if not Path(executable).is_absolute() or not Path(executable).is_file():
            raise ValueError("PDF semantic checks require trusted absolute executable paths")

    verification_environment = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "LANG": "C",
        "LC_ALL": "C",
    }
    for executable, arguments, label in (
        (pdfinfo, ["-"], "PDF metadata"),
        (pdftotext, ["-layout", "-", "-"], "PDF page text"),
    ):
        try:
            result = subprocess.run(
                [executable, *arguments],
                input=merged,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=verification_environment,
                timeout=12,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"{label} verifier timed out") from exc
        if result.returncode != 0:
            # Do not print converter output: it may eventually include file content.
            raise RuntimeError(f"{label} verifier rejected the synthetic merged PDF")
        if len(result.stdout) > 8192:
            raise RuntimeError(f"{label} verifier produced oversized output")
        if label == "PDF metadata":
            matching_pages = re.findall(rb"(?m)^Pages:[ \t]*(\d+)[ \t]*$", result.stdout)
            if len(matching_pages) != 1 or matching_pages[0] != b"2":
                raise RuntimeError("Synthetic merge must have exactly two readable PDF pages")
        else:
            try:
                page_texts = [
                    section.strip() for section in result.stdout.decode("utf-8", errors="strict").split("\f")
                    if section.strip()
                ]
            except UnicodeError as exc:
                raise RuntimeError("Synthetic merged PDF page text was not decodable") from exc
            if page_texts != ["Alpha", "Beta"]:
                raise RuntimeError("Synthetic merge did not preserve both pages and their order")

    return {"pages": 2, "synthetic_page_content_and_order_verified": True}



def assert_malformed_pdf_is_rejected_and_server_remains_healthy(base: str) -> None:
    """A deterministic malformed second fixture must fail as client input, not crash JVM."""
    invalid = b"%PDF-1.4\n% generated truncated fixture without any PDF objects\n"
    payload, content_type = multipart_pdf_payload((synthetic_pdf("Alpha"), invalid))
    response_status: int
    try:
        with http_open(
            base + "/api/v1/general/merge-pdfs",
            data=payload,
            content_type=content_type,
        ) as response:
            response_status = response.status
    except urllib.error.HTTPError as exc:
        response_status = exc.code
        exc.close()  # Never log the error body, request bytes or stack traces.
    if response_status != 400:
        raise RuntimeError(f"Synthetic corrupted PDF got HTTP {response_status}; required HTTP 400")
    try:
        with http_open(base + "/api/v1/info/health") as response:
            if response.status != 200:
                raise RuntimeError("Core health check failed after malformed PDF upload")
            health = json.loads(response.read(4096))
    except (ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError("Core health response invalid after malformed PDF upload") from exc
    if health.get("status") != "UP":
        raise RuntimeError("Core did not remain healthy after malformed PDF upload")


def smoke_core_jar(path: Path, java: str, startup_timeout: int = 150) -> dict:
    if not path.is_file() or path.is_symlink():
        raise ValueError("Expected a regular core JAR file")
    if not 10 <= startup_timeout <= 240:
        raise ValueError("Invalid startup timeout")
    if not Path(java).is_file():
        raise ValueError("No trusted Java executable selected")

    port = select_loopback_port()
    base = f"http://127.0.0.1:{port}"
    with tempfile.TemporaryDirectory(prefix="goreecloud-pdf-core-smoke-") as tmp:
        work = Path(tmp)
        env = {
            key: os.environ[key]
            for key in ("PATH", "JAVA_HOME", "HOME", "LANG", "LC_ALL")
            if key in os.environ
        }
        env.update({
            "SERVER_ADDRESS": "127.0.0.1",
            "SERVER_PORT": str(port),
            "STIRLING_FLAVOR": "core",
            "ENABLE_SAAS": "false",
            "DISABLE_ADDITIONAL_FEATURES": "true",
            "SECURITY_ENABLELOGIN": "false",   # ephemeral synthetic local-only fixture
            "SYSTEM_ENABLEANALYTICS": "false",
            "SYSTEM_ENABLEFEEDBACK": "false",
            "SYSTEM_SHOWUPDATE": "false",
            "SYSTEM_ENABLEURLTOPDF": "false",
            "SYSTEM_ENABLEMOBILESCANNER": "false",
        })
        cmd = [
            java, "-Xms128m", "-Xmx768m", "-Djava.awt.headless=true",
            f"-Djava.io.tmpdir={tmp}",
            "-jar", str(path.resolve()),
            "--server.address=127.0.0.1", f"--server.port={port}",
            "--security.enableLogin=false",
        ]
        with (work / "application.log").open("wb") as logfile:
            proc = subprocess.Popen(
                cmd, cwd=work, env=env, stdin=subprocess.DEVNULL,
                stdout=logfile, stderr=subprocess.STDOUT,
            )
            try:
                deadline = time.monotonic() + startup_timeout
                while time.monotonic() < deadline:
                    if proc.poll() is not None:
                        details = startup_error_summary(work / "application.log")
                        raise RuntimeError(
                            f"Core JVM terminated before health check (exit {proc.returncode}): {details}"
                        )
                    try:
                        with http_open(base + "/api/v1/info/health") as response:
                            status_body = response.read(4096)
                            health = json.loads(status_body)
                            if response.status == 200 and health.get("status") == "UP":
                                break
                    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
                        pass
                    time.sleep(1)
                else:
                    details = startup_error_summary(work / "application.log")
                    raise TimeoutError(f"Local core HTTP health check never became ready: {details}")

                payload, content_type = multipart_pdf_payload()
                with http_open(base + "/api/v1/general/merge-pdfs", data=payload, content_type=content_type) as response:
                    merged = response.read(MAX_RESULT_BYTES + 1)
                    if response.status != 200:
                        raise RuntimeError(f"PDF merge returned HTTP {response.status}")
                    if not response.headers.get("Content-Type", "").lower().startswith("application/pdf"):
                        raise RuntimeError("PDF merge did not respond with application/pdf")
                    if len(merged) > MAX_RESULT_BYTES or len(merged) < 200 or not merged.startswith(b"%PDF-"):
                        raise RuntimeError("PDF merge returned invalid or oversized PDF bytes")
                pdfinfo = shutil.which("pdfinfo")
                pdftotext = shutil.which("pdftotext")
                if not pdfinfo or not pdftotext:
                    raise RuntimeError("Poppler pdfinfo and pdftotext are required for the semantic smoke gate")
                semantic = inspect_synthetic_merge_result(merged, pdfinfo, pdftotext)
                assert_malformed_pdf_is_rejected_and_server_remains_healthy(base)
                return {
                    "result": "PASS",
                    "evidence": "Loopback health=UP and synthetic two-file PDF merge preserved two pages and ordered text",
                    "output_bytes": len(merged),
                    **semantic,
                    "malformed_synthetic_pdf_rejected_http_400": True,
                    "jvm_healthy_after_invalid_upload": True,
                    "runtime_and_auth_security_audited": False,
                    "input_pdf_safety_audited": False,
                    "production_deployed": False,
                }
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=8)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--startup-timeout", type=int, default=150)
    args = parser.parse_args()
    java = shutil.which("java")
    if not java:
        raise SystemExit("Java not found on PATH")
    try:
        result = smoke_core_jar(args.jar, java, args.startup_timeout)
    except Exception as exc:
        raise SystemExit(f"Nonpublishing loopback core smoke FAILED: {type(exc).__name__}: {exc}") from exc
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
