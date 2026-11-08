#!/usr/bin/env python3
"""Offline, deterministic tracked-asset evidence. NOT a license clearance report."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import subprocess
import stat
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

@contextlib.contextmanager
def open_checked_asset(root: Path, relative: Path):
    """Open only a regular file through no-follow directory descriptors on POSIX.

    The working tree may contain symlinks even when Git's index lists normal
    files. On POSIX, directory handles plus O_NOFOLLOW protect intermediate
    components as well as the leaf if a path changes after the initial check.
    A non-POSIX fallback rechecks resolved containment before opening.
    """
    target = root / relative
    if not target.resolve(strict=False).is_relative_to(root):
        raise ValueError("Tracked asset resolves outside the checkout")
    secure = (
        os.name == "posix"
        and hasattr(os, "O_NOFOLLOW")
        and hasattr(os, "O_DIRECTORY")
        and os.open in os.supports_dir_fd
    )
    if not secure:
        with target.open("rb") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise ValueError("Tracked asset is not a regular file")
            yield source, os.fstat(source.fileno()).st_size
        return
    dir_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0)
    with contextlib.ExitStack() as stack:
        parent_fd = os.open(root, dir_flags)
        stack.callback(os.close, parent_fd)
        for component in relative.parts[:-1]:
            parent_fd = os.open(component, dir_flags, dir_fd=parent_fd)
            stack.callback(os.close, parent_fd)
        asset_fd = os.open(relative.name, file_flags, dir_fd=parent_fd)
        stack.callback(os.close, asset_fd)
        metadata = os.fstat(asset_fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError("Tracked asset is not a regular file")
        with os.fdopen(os.dup(asset_fd), "rb") as source:
            yield source, metadata.st_size


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
        # A tracked file can sit under a symlinked working-tree *directory*;
        # checking only file.is_symlink() would follow its outside target.
        if any(
            (root.joinpath(*relative.parts[:depth])).is_symlink()
            for depth in range(1, len(relative.parts) + 1)
        ):
            evidence.append({"path": rel, "state": "tracked-symlink-not-read", "license_status": "UNVERIFIED"})
            continue
        if not file.is_file():
            evidence.append({"path": rel, "state": "tracked-file-missing", "license_status": "UNVERIFIED"})
            continue
        digest = hashlib.sha256()
        with open_checked_asset(root, relative) as (source, size):
            if size > MAX_ASSET_SIZE:
                raise ValueError(f"Asset exceeds bounded read limit: {rel}")
            read_bytes = 0
            for chunk in iter(lambda: source.read(512 * 1024), b""):
                read_bytes += len(chunk)
                if read_bytes > MAX_ASSET_SIZE:
                    raise ValueError(f"Asset exceeds bounded read limit: {rel}")
                digest.update(chunk)
            if read_bytes != size:
                raise ValueError(f"Tracked asset changed size during evidence read: {rel}")
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
