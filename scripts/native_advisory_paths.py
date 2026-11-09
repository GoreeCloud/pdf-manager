#!/usr/bin/env python3
"""Bounded offline Cargo.lock advisory path evidence, NOT a vuln/license clearance."""
from __future__ import annotations

import argparse
import collections
import json
import tomllib
from pathlib import Path

MAX_PACKAGES = 15000
MAX_PATH_NODES = 32
ROOT_PACKAGE = "goreecloud-pdf-manager"
REVIEWED_TARGETS = (
    ("glib", "0.18.5", "GHSA-wrw7-89jp-8q8g"),
    ("rand", "0.7.3", "GHSA-cq8v-f236-94qc"),
)


def dependency_path_report(lock: dict) -> dict:
    entries = lock.get("package")
    if not isinstance(entries, list) or not 0 < len(entries) <= MAX_PACKAGES:
        raise ValueError("Invalid or unbounded Cargo package inventory")

    packages: dict[tuple[str, str], dict] = {}
    by_name: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Invalid Cargo package entry")
        name = entry.get("name")
        version = entry.get("version")
        if not isinstance(name, str) or not isinstance(version, str) or not name or not version:
            raise ValueError("Cargo package entry has invalid identity")
        key = (name, version)
        if key in packages:
            raise ValueError("Duplicate package identity requires manual review")
        packages[key] = entry
        by_name[name].append(key)

    roots = sorted(k for k in packages if k[0] == ROOT_PACKAGE)
    if len(roots) != 1:
        raise ValueError("Expected precisely one application root in Cargo.lock")

    edges: dict[tuple[str, str], list[tuple[tuple[str, str], bool]]] = {}
    for key, entry in packages.items():
        dependencies = entry.get("dependencies", [])
        if not isinstance(dependencies, list) or len(dependencies) > MAX_PACKAGES:
            raise ValueError("Invalid Cargo dependency list")
        resolved: set[tuple[tuple[str, str], bool]] = set()
        for dep in dependencies:
            if not isinstance(dep, str):
                raise ValueError("Unexpected Cargo dependency format")
            fields = dep.split()
            if len(fields) == 1:
                options = by_name.get(fields[0], [])
            elif len(fields) == 2:
                options = [(fields[0], fields[1])]
            else:
                raise ValueError("Unsupported Cargo dependency identifier")
            if not options or any(k not in packages for k in options):
                raise ValueError("Unresolved Cargo.lock dependency; manual review required")
            for option in options:
                # Cargo's bare dependency names are ambiguous when multiple
                # versions are locked; keep *all* possible targets and mark
                # the resulting chain as a candidate, not a verified edge.
                resolved.add((option, len(options) > 1))
        edges[key] = sorted(resolved)

    paths: dict[tuple[str, str], tuple[list[tuple[str, str]], bool]] = {}
    queue = collections.deque([(roots[0], [roots[0]], False)])
    paths[roots[0]] = ([roots[0]], False)
    while queue:
        source, path, ambiguous = queue.popleft()
        if len(path) >= MAX_PATH_NODES:
            continue
        for target, has_ambiguous_resolution in edges[source]:
            if target in paths:
                continue
            next_path = path + [target]
            next_ambiguous = ambiguous or has_ambiguous_resolution
            paths[target] = (next_path, next_ambiguous)
            queue.append((target, next_path, next_ambiguous))

    advisories: list[dict] = []
    for name, version, ghsa in REVIEWED_TARGETS:
        key = (name, version)
        present = key in packages
        found = paths.get(key)
        path, ambiguous = found if found else ([], False)
        advisories.append({
            "advisory": ghsa,
            "package": name,
            "locked_version": version,
            "version_present_in_lockfile": present,
            "candidate_path_from_root": [
                {"package": item[0], "version": item[1]} for item in path
            ],
            "candidate_path_available": found is not None,
            "path_has_ambiguous_version_resolution": ambiguous,
            "runtime_exploitability": "NOT_ASSESSED",
            "target_platform_and_feature_reachability": "NOT_ASSESSED",
            "remediation_status": "NOT_VERIFIED",
        })
    return {
        "format": "GoreeCloud Cargo advisory candidate graph v1",
        "status": "LOCKFILE PATH EVIDENCE ONLY — NOT VULNERABILITY OR LICENSE CLEARANCE",
        "source": "Git-tracked Cargo.lock package and dependency fields only",
        "package_count": len(packages),
        "root": {"package": roots[0][0], "version": roots[0][1]},
        "dependency_resolution_caution": (
            "Unversioned edges with multiple locked versions are all considered; "
            "flagged paths are candidate routes, not necessarily executable paths."
        ),
        "advisories": advisories,
        "source_license_cleared": False,
        "security_release_approved": False,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lockfile", type=Path,
                    default=Path(__file__).resolve().parents[1] / "frontend/src-tauri/Cargo.lock")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    path = args.lockfile
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 8 * 1024 * 1024:
        raise ValueError("Cargo.lock must be a bounded regular file")
    with path.open("rb") as stream:
        report = dependency_path_report(tomllib.load(stream))
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "NATIVE_LOCKFILE_CANDIDATE_PATHS_ONLY",
        "packages": report["package_count"],
        "target_versions_present": sum(x["version_present_in_lockfile"] for x in report["advisories"]),
        "routes_present": sum(x["candidate_path_available"] for x in report["advisories"]),
        "release_approved": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
