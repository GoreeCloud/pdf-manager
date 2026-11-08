#!/usr/bin/env python3
"""Run the unreleased core JAR on loopback with synthetic PDFs only.

An isolated CI smoke test, not a production deployment, sandbox, security
assessment, full PDF correctness test, or authorized external service.
"""
from __future__ import annotations

import argparse
import json
import os
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


def multipart_pdf_payload() -> tuple[bytes, str]:
    boundary = "goreecloud-ci-synthetic-pdf-boundary"
    chunks = []
    for index, pdf in enumerate((synthetic_pdf("Alpha"), synthetic_pdf("Beta")), start=1):
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
                        raise RuntimeError(f"Core JVM terminated before health check (exit {proc.returncode})")
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
                    raise TimeoutError("Local core HTTP health check never became ready")

                payload, content_type = multipart_pdf_payload()
                with http_open(base + "/api/v1/general/merge-pdfs", data=payload, content_type=content_type) as response:
                    merged = response.read(MAX_RESULT_BYTES + 1)
                    if response.status != 200:
                        raise RuntimeError(f"PDF merge returned HTTP {response.status}")
                    if not response.headers.get("Content-Type", "").lower().startswith("application/pdf"):
                        raise RuntimeError("PDF merge did not respond with application/pdf")
                    if len(merged) > MAX_RESULT_BYTES or len(merged) < 200 or not merged.startswith(b"%PDF-"):
                        raise RuntimeError("PDF merge returned invalid or oversized PDF bytes")
                return {
                    "result": "PASS",
                    "evidence": "Loopback health=UP and synthetic two-file PDF merge returned PDF content",
                    "output_bytes": len(merged),
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
