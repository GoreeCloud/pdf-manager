#!/usr/bin/env python3
"""Deterministic nonpublishing evidence for runtime JARs inside the core archive.

This is a SHA-256/filename inventory, *not* a license determination, complete
SBOM, vulnerability scan, provenance attestation, or permission to redistribute.
The archive and nested jars are never extracted or executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

MAX_ARCHIVE_BYTES = 2 * 1024 * 1024 * 1024
MAX_LIBRARY_BYTES = 512 * 1024 * 1024
MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024
LIB_PREFIX = "BOOT-INF/lib/"
BLOCKED_FRAGMENTS = ("-proprietary-", "/proprietary/", "-saas-", "/saas/")


def file_sha256(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def inspect_runtime_libraries(path: Path) -> dict[str, object]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("Expected a regular, non-symlinked core JAR")
    archive_size = path.stat().st_size
    if archive_size < 100 or archive_size > MAX_ARCHIVE_BYTES:
        raise ValueError("Core JAR is empty or exceeds bounded size")

    libraries: list[dict[str, object]] = []
    total_bytes = 0
    try:
        with zipfile.ZipFile(path) as jar:
            entries = jar.infolist()
            if len(entries) != len({e.filename for e in entries}):
                raise ValueError("Duplicate ZIP entry names are not permitted")
            for info in entries:
                name = info.filename
                if not name.startswith(LIB_PREFIX):
                    continue
                if name == LIB_PREFIX and info.is_dir():
                    continue
                if not name.endswith(".jar"):
                    raise ValueError("Unexpected non-JAR file in runtime library directory")
                basename = name[len(LIB_PREFIX):]
                if not basename or "/" in basename or "\\" in basename or basename in (".", ".."):
                    raise ValueError("Unexpected runtime library path")
                if any(fragment in name.lower() for fragment in BLOCKED_FRAGMENTS):
                    raise ValueError("Excluded commercial module in runtime libraries")
                if info.is_dir() or info.file_size < 4 or info.file_size > MAX_LIBRARY_BYTES:
                    raise ValueError("Runtime JAR library size or file type invalid")
                total_bytes += info.file_size
                if total_bytes > MAX_TOTAL_BYTES:
                    raise ValueError("Runtime library aggregate expansion limit exceeded")
                # Reject symlink ZIP members even when their names look like JARs.
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError("Symlinked runtime JAR member is forbidden")
                sha = hashlib.sha256()
                read_bytes = 0
                with jar.open(info, "r") as source:
                    first = source.read(4)
                    if first != b"PK\x03\x04":
                        raise ValueError("Embedded runtime library is not a ZIP/JAR file")
                    sha.update(first)
                    read_bytes += len(first)
                    for block in iter(lambda: source.read(1024 * 1024), b""):
                        read_bytes += len(block)
                        if read_bytes > MAX_LIBRARY_BYTES or read_bytes > info.file_size:
                            raise ValueError("Embedded runtime library expanded unexpectedly")
                        sha.update(block)
                if read_bytes != info.file_size:
                    raise ValueError("Embedded runtime library size changed during inspection")
                libraries.append({
                    "file": basename,
                    "size_bytes": info.file_size,
                    "sha256": sha.hexdigest(),
                    "license_status": "UNVERIFIED",
                    "vulnerability_status": "NOT_ASSESSED",
                })
    except (OSError, zipfile.BadZipFile, RuntimeError, EOFError) as exc:
        raise ValueError("Unreadable or corrupt core runtime JAR archive") from exc
    if not libraries:
        raise ValueError("No BOOT-INF/lib runtime libraries in archive")
    libraries.sort(key=lambda component: component["file"])
    return {
        "format": "GoreeCloud core JAR library metadata v1",
        "source_sha256": file_sha256(path),
        "source_size_bytes": archive_size,
        "library_count": len(libraries),
        "total_uncompressed_library_bytes": total_bytes,
        "license_cleared": False,
        "vulnerabilities_resolved": False,
        "release_approved": False,
        "libraries": libraries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = inspect_runtime_libraries(args.jar)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "NONPUBLISHING_RUNTIME_JAR_METADATA_ONLY",
        "library_count": report["library_count"],
        "license_cleared": False,
        "release_approved": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
