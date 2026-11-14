#!/usr/bin/env python3
"""Read-only desktop JS shell exposure guard, not a Tauri sandbox certification."""
from __future__ import annotations

import json
from pathlib import Path


def verify_desktop_webview_shell_boundary(capability: dict, tauri: dict, native_source: str) -> dict:
    if not isinstance(capability, dict) or not isinstance(tauri, dict):
        raise ValueError("Expected explicit Tauri capability and configuration maps")
    grants = capability.get("permissions")
    if not isinstance(grants, list) or not all(isinstance(x, str) for x in grants):
        raise ValueError("Malformed Tauri capability permission array")
    if len(grants) != len(set(grants)):
        raise ValueError("Duplicate capability grants require review")
    shell_grants = [x for x in grants if x.startswith("shell:")]
    if shell_grants:
        raise ValueError("Desktop webview unexpectedly exposes the shell plugin")
    plugins = tauri.get("plugins")
    if not isinstance(plugins, dict):
        raise ValueError("Missing Tauri plugin config")
    shell = plugins.get("shell")
    if shell is not None and (not isinstance(shell, dict) or shell.get("open") is not False):
        raise ValueError("Legacy Tauri shell open configuration must be disabled")
    if tauri.get("bundle", {}).get("active") is not False:
        raise ValueError("Nonpublishing desktop bundle policy has changed")
    if "tauri_plugin_shell::init()" not in native_source:
        raise ValueError("Native-only backend sidecar plugin disappeared")
    if "ShellExt" not in native_source:
        raise ValueError("Native sidecar command implementation must be audited")
    return {
        "status": "STATIC_WEBVIEW_SHELL_PERMISSION_POLICY_ONLY",
        "webview_shell_grants": 0,
        "legacy_shell_open_disabled": True,
        "native_sidecar_plugin_retained": True,
        "bundle_active": False,
        "unreviewed_other_permissions": [
            "core:default", "dialog:default", "opener:default",
            "window-state", "deep-link", "native Rust commands",
        ],
        "desktop_runtime_verified": False,
        "production_release_approved": False,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "frontend/src-tauri"
    cap = json.loads((root / "capabilities/default.json").read_text())
    tauri = json.loads((root / "tauri.conf.json").read_text())
    native = (root / "src/lib.rs").read_text()
    backend = (root / "src/commands/backend.rs").read_text()
    report = verify_desktop_webview_shell_boundary(cap, tauri, native + "\n" + backend)
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
