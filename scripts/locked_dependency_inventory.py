#!/usr/bin/env python3
"""Deterministic CycloneDX 1.5 *metadata-only* inventory of committed lockfiles.

No network access, package installation, dependency resolution, license inference,
or project code execution. This is NOT a complete release SBOM or license audit.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import tomllib
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
LOCKFILES = (
    "frontend/package-lock.json",
    "devTools/package-lock.json",
    "frontend/src-tauri/Cargo.lock",
    "frontend/src-tauri/provisioner/Cargo.lock",
    "frontend/src-tauri/thumbnail-handler/Cargo.lock",
)
MAX_LOCK_BYTES = 16 * 1024 * 1024
ALGORITHMS = {"sha512": "SHA-512", "sha384": "SHA-384", "sha256": "SHA-256", "sha1": "SHA-1"}


def _file_bytes(root: Path, rel: str) -> bytes:
    path = root / rel
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Missing or symlinked lockfile: {rel}")
    if path.stat().st_size > MAX_LOCK_BYTES:
        raise ValueError(f"Lockfile too large for bounded metadata parse: {rel}")
    return path.read_bytes()


def _npm_name(location: str) -> str | None:
    if "node_modules/" not in location:
        return None
    name = location.rsplit("node_modules/", 1)[-1]
    parts = name.split("/")
    if name.startswith("@"):
        return name if len(parts) == 2 and all(parts) else None
    return name if len(parts) == 1 and bool(name) else None


def _purl(ecosystem: str, name: str, version: str) -> str:
    if ecosystem == "npm" and name.startswith("@"):
        scope, package = name.split("/", 1)
        encoded_name = quote(scope, safe="") + "/" + quote(package, safe="")
    else:
        encoded_name = quote(name, safe="")
    return f"pkg:{ecosystem}/{encoded_name}@{quote(version, safe='')}"


def _npm_integrity(value: object) -> tuple[str, str] | None:
    if not isinstance(value, str):
        return None
    # SRI lists can contain several algorithms. Preserve the strongest supported one.
    for algorithm in ("sha512", "sha384", "sha256", "sha1"):
        match = re.search(r"(?:^|\s)" + algorithm + r"-([A-Za-z0-9+/=]+)(?=\s|$)", value)
        if match:
            try:
                digest = base64.b64decode(match.group(1), validate=True)
            except ValueError as exc:
                raise ValueError("Invalid npm lockfile integrity digest") from exc
            expected = {"sha512": 64, "sha384": 48, "sha256": 32, "sha1": 20}[algorithm]
            if len(digest) != expected:
                raise ValueError("Invalid npm lockfile integrity digest length")
            return ALGORITHMS[algorithm], digest.hex()
    # A supported integrity algorithm with malformed SRI must fail, not vanish.
    if any(re.search(r"(?:^|\s)" + algorithm + r"-", value)
           for algorithm in ALGORITHMS):
        raise ValueError("Invalid npm lockfile integrity value")
    return None


def generate_inventory(root: Path = ROOT) -> dict:
    records: dict[str, dict] = {}
    source_digests: list[tuple[str, str]] = []
    counts = {"npm_locations": 0, "cargo_registry_packages": 0, "ignored_local_or_link_entries": 0}
    for rel in LOCKFILES:
        raw = _file_bytes(root, rel)
        source_digests.append((rel, hashlib.sha256(raw).hexdigest()))
        if rel.endswith("package-lock.json"):
            data = json.loads(raw)
            if data.get("lockfileVersion") != 3 or not isinstance(data.get("packages"), dict):
                raise ValueError(f"Expected npm package-lock v3 metadata: {rel}")
            iterator = []
            for location, entry in sorted(data["packages"].items()):
                if not isinstance(entry, dict):
                    raise ValueError(f"Invalid npm package entry in {rel}")
                name = entry.get("name") or _npm_name(location)
                version = entry.get("version")
                if not isinstance(name, str) or not isinstance(version, str) or not _npm_name(location):
                    counts["ignored_local_or_link_entries"] += 1
                    continue
                counts["npm_locations"] += 1
                iterator.append(("npm", name, version, _npm_integrity(entry.get("integrity")),
                                 str(entry["license"]) if isinstance(entry.get("license"), str) else "",
                                 str(entry.get("dev", "not-declared")).lower()))
        else:
            data = tomllib.loads(raw.decode("utf-8"))
            if not isinstance(data.get("package"), list):
                raise ValueError(f"Expected Cargo.lock packages: {rel}")
            iterator = []
            for entry in data["package"]:
                if not isinstance(entry, dict):
                    raise ValueError(f"Invalid Cargo package entry: {rel}")
                name, version, source = entry.get("name"), entry.get("version"), entry.get("source", "")
                if not isinstance(name, str) or not isinstance(version, str):
                    raise ValueError(f"Invalid Cargo package identity: {rel}")
                if not isinstance(source, str) or not (source.startswith("registry+") or source.startswith("git+")):
                    counts["ignored_local_or_link_entries"] += 1
                    continue
                checksum = entry.get("checksum")
                if checksum is not None and (not isinstance(checksum, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", checksum)):
                    raise ValueError(f"Invalid Cargo checksum: {rel}")
                counts["cargo_registry_packages"] += 1
                iterator.append(("cargo", name, version, ("SHA-256", checksum.lower()) if checksum else None, "", "not-applicable"))

        for ecosystem, name, version, digest, license_hint, dev_flag in iterator:
            purl = _purl(ecosystem, name, version)
            rec = records.setdefault(purl, {"ecosystem": ecosystem, "name": name, "version": version,
                                             "sources": set(), "hashes": set(), "license_hints": set(), "dev_flags": set()})
            if (rec["name"], rec["version"], rec["ecosystem"]) != (name, version, ecosystem):
                raise ValueError(f"Package URL collision: {purl}")
            rec["sources"].add(rel)
            rec["dev_flags"].add(dev_flag)
            if license_hint:
                rec["license_hints"].add(license_hint)
            if digest:
                if rec["hashes"] and digest not in rec["hashes"]:
                    raise ValueError(f"Conflicting locked integrity digests for {purl}")
                rec["hashes"].add(digest)

    components = []
    for ref, rec in sorted(records.items()):
        props = [
            {"name": "goreecloud:lockfile-evidence", "value": ",".join(sorted(rec["sources"]))},
        ]
        if rec["ecosystem"] == "npm":
            props.append({"name": "goreecloud:npm-dev-flag", "value": ",".join(sorted(rec["dev_flags"]))})
        if rec["license_hints"]:
            props.append({"name": "goreecloud:unverified-license-hint", "value": ",".join(sorted(rec["license_hints"]))})
        comp = {"type": "library", "name": rec["name"], "version": rec["version"],
                "bom-ref": ref, "purl": ref, "properties": props}
        if rec["hashes"]:
            comp["hashes"] = [{"alg": alg, "content": hexdigest} for alg, hexdigest in sorted(rec["hashes"])]
        components.append(comp)

    metadata_props = [
        {"name": "goreecloud:inventory-status", "value": "METADATA ONLY; NOT A COMPLETE OR ATTESTED SBOM"},
        {"name": "goreecloud:known-exclusions", "value": (
            "Resolved Gradle/Java transitive dependencies, container and OS packages, "
            "dynamic modules, third-party assets, source-level embedded code, and effective runtime graph")},
        {"name": "goreecloud:license-review", "value": "NOT PERFORMED; lockfile license hints are unverified"},
        {"name": "goreecloud:network-access", "value": "none"},
    ]
    for rel, digest in source_digests:
        metadata_props.append({"name": "goreecloud:source-sha256:" + rel, "value": digest})
    for key, value in sorted(counts.items()):
        metadata_props.append({"name": "goreecloud:scan-count:" + key, "value": str(value)})

    return {
        "bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
        "metadata": {
            "component": {"type": "application", "name": "GoreeCloud PDF Manager",
                          "version": "development-preview"},
            "tools": {"components": [{"type": "application", "name": "goreecloud-lockfile-metadata-inventory",
                                      "version": "1.0.0"}]},
            "properties": metadata_props,
        },
        "components": components,
    }


def render_inventory(root: Path = ROOT) -> str:
    return json.dumps(generate_inventory(root), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Root of an authorized checkout")
    parser.add_argument("--output", type=Path, help="Write metadata file; default stdout")
    args = parser.parse_args()
    text = render_inventory(args.root)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Lockfile metadata inventory: {len(json.loads(text)['components'])} unique package identities, 5 lockfiles.")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
