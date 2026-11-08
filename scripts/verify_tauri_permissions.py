#!/usr/bin/env python3
"""Fail-closed policy for the unreleased MIT-core desktop WebView.

The upstream desktop-specific UI was excluded from this public import. The
remaining core editor does not need unscoped filesystem or arbitrary HTTP
plugin permissions. Review any future permission expansion independently.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY = ROOT / "frontend/src-tauri/capabilities/default.json"
payload = json.loads(CAPABILITY.read_text(encoding="utf-8"))
permissions = payload["permissions"]
assert permissions, "The desktop WebView must have an explicit permission policy"

def identifier(item):
    return item if isinstance(item, str) else item.get("identifier", "")

for permission in permissions:
    name = identifier(permission)
    assert not name.startswith(("fs:", "http:")), (
        f"Desktop WebView bridge grants unreviewed broad access: {name}"
    )
    assert name != "shell:allow-execute", "Do not grant arbitrary command execution"
    if isinstance(permission, dict):
        for grant in permission.get("allow", []):
            assert grant.get("path") != "**", "Unbounded file access is prohibited"
            assert grant.get("url") not in {"http://*", "https://*"}, (
                "Unbounded HTTP access is prohibited"
            )

# Validate the retained core frontend does not depend on bridges we removed.
core_src = ROOT / "frontend/src/editor/core"
for src in core_src.rglob("*"):
    if src.is_file() and src.suffix.lower() in {".ts", ".tsx", ".js", ".mjs"}:
        content = src.read_text(encoding="utf-8")
        assert "@tauri-apps/plugin-fs" not in content, str(src.relative_to(ROOT))
        assert "@tauri-apps/plugin-http" not in content, str(src.relative_to(ROOT))

print("Native WebView: broad FS/HTTP bridges denied; core imports verified: PASS")
