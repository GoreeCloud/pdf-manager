#!/usr/bin/env python3
"""Offline tracked-asset/adjacent-license-NOTICE review queue, not license clearance."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

from tracked_asset_evidence import build_report as build_asset_report

MAX_TRACKED_FILES = 50000
# Only plain license-text/doc files can be candidates. Application code or
# license-related Java classes, JSON policy, etc. are never treated as notices.
NOTICE_FILE = re.compile(
    r"(?i)^(?:(?:licen[cs]e|copying|notice)(?:[._-][\w. -]+)?|ofl(?:[._-][\w. -]+)?|[\w. -]+-ofl)\.(?:txt|md|rst|html?)$"
    r"|^(?:LICENSE|LICENCE|COPYING|NOTICE|OFL)$",
)


def validate_repo_path(value: str) -> Path:
    path = Path(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or any(part in ("", ".") for part in path.parts)
        or value.startswith(".git/")
    ):
        raise ValueError("Unsafe tracked path in evidence metadata")
    return path


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "-z", "--full-name"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
    )
    if result.stdout and not result.stdout.endswith(b"\0"):
        raise ValueError("Unframed Git path listing")
    paths = [os.fsdecode(part) for part in result.stdout.split(b"\0") if part]
    if len(paths) > MAX_TRACKED_FILES:
        raise ValueError("Tracked path inventory exceeds review limit")
    for rel in paths:
        validate_repo_path(rel)
    return sorted(paths)


def match_license_notices(asset_paths: list[str], tracked: list[str]) -> dict:
    """Suggest only same-folder explicit tracked notices; never infer permission."""
    by_dir: dict[str, list[str]] = {}
    for rel in tracked:
        path = validate_repo_path(rel)
        if NOTICE_FILE.fullmatch(path.name):
            by_dir.setdefault(path.parent.as_posix(), []).append(rel)

    queue = []
    for rel in sorted(asset_paths):
        path = validate_repo_path(rel)
        matches = sorted(by_dir.get(path.parent.as_posix(), []))
        queue.append({
            "asset": rel,
            "adjacent_notice_candidates": matches,
            "notice_existence_only": bool(matches),
            "redistribution_rights": "UNVERIFIED",
        })
    return {
        "format": "GoreeCloud adjacent asset-license notice candidates v1",
        "status": "REVIEW QUEUE ONLY; NO LICENSES CLEARED",
        "method": "tracked Git path names only; no external lookup or license-text interpretation",
        "asset_count": len(queue),
        "assets_with_adjacent_notices": sum(bool(x["adjacent_notice_candidates"]) for x in queue),
        "assets_without_adjacent_notices": sum(not x["adjacent_notice_candidates"] for x in queue),
        "rights_verified": 0,
        "notice_presence_does_not_imply": [
            "a license applies to this asset",
            "authorship, permission, redistribution rights or trademark clearance",
            "absence of another notice elsewhere in the repository",
            "safety, vulnerability status or a production release approval",
        ],
        "review_queue": queue,
    }


def build_notice_queue(root: Path) -> dict:
    root = root.resolve(strict=True)
    asset_paths = [x["path"] for x in build_asset_report(root)["candidates"]]
    return match_license_notices(asset_paths, tracked_files(root))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    report = build_notice_queue(args.root)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "NOTICES_ONLY_NO_RIGHTS_CLEARED",
        "assets": report["asset_count"],
        "adjacent_notice_candidates": report["assets_with_adjacent_notices"],
        "rights_verified": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
