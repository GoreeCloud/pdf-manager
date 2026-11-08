#!/usr/bin/env python3
"""Validate the core-only Spring Boot JAR structure without executing its code.

This static check does NOT establish dependency license compliance, runtime
correctness, vulnerability status, safety for untrusted PDFs, or release approval.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

MAX_JAR_BYTES = 2 * 1024 * 1024 * 1024
APP_CLASS = "BOOT-INF/classes/stirling/software/SPDF/SPDFApplication.class"
MAIN_LAUNCHER = "org/springframework/boot/loader/launch/JarLauncher.class"
EXPECTED_TITLE = "GoreeCloud PDF Manager"


def inspect_core_jar(path: Path) -> dict[str, object]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("Expected a regular, non-symlinked core JAR")
    if path.stat().st_size <= 0 or path.stat().st_size > MAX_JAR_BYTES:
        raise ValueError("Core JAR exceeds reviewable size or is empty")
    try:
        with zipfile.ZipFile(path, "r") as archive:
            entries = [e.filename for e in archive.infolist()]
            if len(entries) != len(set(entries)):
                raise ValueError("Duplicate JAR entry names")
            required = {"META-INF/MANIFEST.MF", APP_CLASS, MAIN_LAUNCHER}
            if not required.issubset(set(entries)):
                raise ValueError(f"Missing executable Spring Boot core entries: {sorted(required - set(entries))}")
            libraries = sorted(x for x in entries if x.startswith("BOOT-INF/lib/") and x.endswith(".jar"))
            if not libraries:
                raise ValueError("Missing Spring Boot runtime libraries")
            # Restricted upstream modules were deliberately excluded from the public import.
            blocked_fragments = ("-proprietary-", "/proprietary/", "-saas-", "/saas/")
            blocked = [n for n in entries if any(fragment in n.lower() for fragment in blocked_fragments)]
            if blocked:
                raise ValueError("Excluded proprietary or SaaS source/module detected in JAR")
            manifest = archive.read("META-INF/MANIFEST.MF").decode("utf-8", errors="strict")
            if f"Implementation-Title: {EXPECTED_TITLE}" not in manifest:
                raise ValueError("JAR implementation title does not match GoreeCloud PDF Manager")
            if "Start-Class: stirling.software.SPDF.SPDFApplication" not in manifest:
                raise ValueError("Unexpected Spring Boot launch application")
            if "Main-Class: org.springframework.boot.loader.launch.JarLauncher" not in manifest:
                raise ValueError("Missing Spring Boot executable launch manifest")
            return {
                "status": "STATIC_JAR_STRUCTURE_ONLY",
                "implementation_title": EXPECTED_TITLE,
                "library_count": len(libraries),
                "entry_count": len(entries),
                "excluded_modules_found": 0,
                "runtime_tested": False,
                "license_cleared": False,
                "release_approved": False,
            }
    except (zipfile.BadZipFile, UnicodeDecodeError) as exc:
        raise ValueError("Invalid or unreadable core JAR archive") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True, help="Generated nonpublished Spring Boot JAR")
    args = parser.parse_args()
    print(json.dumps(inspect_core_jar(args.jar), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
