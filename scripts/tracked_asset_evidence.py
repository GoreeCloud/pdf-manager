#!/usr/bin/env python3
"""Offline, deterministic tracked-asset evidence. NOT a license clearance report."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

MAX_ASSET_SIZE = 50 * 1024 * 1024
MAX_ASSETS = 15000
CATEGORIES = {
    "font": {".ttf", ".woff", ".woff2", ".otf", ".eot"},
    "image": {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".icns", ".webp", ".bmp", ".tif", ".tiff", ".avif"},
    "embedded-code-or-model": {".wasm", ".jar", ".so", ".dll", ".dylib", ".exe", ".bin", ".onnx", ".model"},
    "document": {".pdf"},
}
EXT_TO_CATEGORY = {suffix: group for group, suffixes in CATEGORIES.items() for suffix in suffixes}
EXCLUDED_GIT_PREFIXES = (".git/", "node_modules/", "target/", "build/")

def tracked_assets(root: Path) -> list[dict]:
    root = root.resolve(strict=True)
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "-z", "--full-name"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=30,
    )
    if not result.stdout.endswith(b"\x00") and result.stdout:
        raise ValueError("Unexpected git ls-files response framing")
    entries = result.stdout.split(b"\x00")
    files = [os.fsdecode(x) for x in entries if x]
    selected = [name for name in files if Path(name).suffix.lower() in EXT_TO_CATEGORY]
    if len(selected) > MAX_ASSETS:
        raise ValueError("Too many tracked asset candidates; explicit review required")
    evidence = []
    for rel in sorted(selected):
        relative = Path(rel)
        if relative.is_absolute() or ".." in relative.parts or rel.startswith(EXCLUDED_GIT_PREFIXES):
            raise ValueError("Unsafe asset source path from git metadata")
        file = root / relative
        # Ignore symlink content, including symlinks that might escape the checkout.
        if file.is_symlink():
            evidence.append({"path": rel, "state": "tracked-symlink-not-read", "license_status": "UNVERIFIED"})
            continue
        if not file.is_file():
            evidence.append({"path": rel, "state": "tracked-file-missing", "license_status": "UNVERIFIED"})
            continue
        size = file.stat().st_size
        if size > MAX_ASSET_SIZE:
            raise ValueError(f"Asset exceeds bounded read limit: {rel}")
        digest = hashlib.sha256()
        with file.open("rb") as f:
            for chunk in iter(lambda: f.read(512 * 1024), b""):
                digest.update(chunk)
        evidence.append({
            "path": rel,
            "category": EXT_TO_CATEGORY[file.suffix.lower()],
            "bytes": size,
            "sha256": digest.hexdigest(),
            "state": "tracked-asset-bytes-hashed",
            "license_status": "UNVERIFIED",
        })
    return evidence

def build_report(root: Path) -> dict:
    evidence = tracked_assets(root)
    return {
        "format": "GoreeCloud tracked-asset-evidence v1",
        "status": "METADATA ONLY — NOT LICENSE CLEARED OR RELEASE READY",
        "method": "offline git ls-files metadata and SHA-256 of regular tracked asset bytes",
        "does_not_prove": [
            "origin, authorship or redistribution rights of any asset",
            "complete bundle/deployment contents, dynamic assets or resolved dependencies",
            "exhaustive license or third-party trademark clearance",
            "security of native/model binaries or use of embedded documents",
        ],
        "candidate_count": len(evidence),
        "hashed_count": sum(x["state"] == "tracked-asset-bytes-hashed" for x in evidence),
        "candidates": evidence,
    }

def render(root: Path) -> str:
    return json.dumps(build_report(root), sort_keys=True, indent=2, ensure_ascii=False) + "\n"

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    data = render(args.root)
    if args.output:
        args.output.write_text(data, encoding="utf-8")
        print(f"Tracked asset evidence: {json.loads(data)['candidate_count']} candidates, not license cleared")
    else:
        print(data, end="")

if __name__ == "__main__":
    main()
