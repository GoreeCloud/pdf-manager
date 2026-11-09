"""Static desktop capability tests; never launch a WebView or native shell."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_desktop_webview_permissions import verify_desktop_webview_shell_boundary


def inputs():
    return (
        {"permissions": ["core:default", "opener:default"]},
        {"plugins": {"shell": {"open": False}}, "bundle": {"active": False}},
        "tauri_plugin_shell::init()\nuse tauri_plugin_shell::ShellExt;",
    )


class WebviewShellBoundaryTests(unittest.TestCase):
    def test_native_plugin_retained_but_js_shell_denied(self):
        report = verify_desktop_webview_shell_boundary(*inputs())
        self.assertEqual(report["webview_shell_grants"], 0)
        self.assertTrue(report["native_sidecar_plugin_retained"])
        self.assertFalse(report["production_release_approved"])

    def test_explicit_open_grant_is_rejected(self):
        a, b, c = inputs()
        a["permissions"].append("shell:allow-open")
        with self.assertRaisesRegex(ValueError, "exposes"):
            verify_desktop_webview_shell_boundary(a, b, c)

    def test_shell_default_grant_is_rejected(self):
        a, b, c = inputs()
        a["permissions"].append("shell:default")
        with self.assertRaisesRegex(ValueError, "exposes"):
            verify_desktop_webview_shell_boundary(a, b, c)

    def test_open_config_must_be_disabled(self):
        a, b, c = inputs()
        b["plugins"]["shell"]["open"] = True
        with self.assertRaisesRegex(ValueError, "disabled"):
            verify_desktop_webview_shell_boundary(a, b, c)

    def test_bundle_must_stay_inactive(self):
        a, b, c = inputs()
        b["bundle"]["active"] = True
        with self.assertRaisesRegex(ValueError, "bundle"):
            verify_desktop_webview_shell_boundary(a, b, c)

    def test_native_backend_shell_plugin_cannot_disappear(self):
        a, b, c = inputs()
        with self.assertRaisesRegex(ValueError, "sidecar plugin"):
            verify_desktop_webview_shell_boundary(a, b, "use ShellExt;")

    def test_malformed_or_duplicate_grants_rejected(self):
        a, b, c = inputs()
        a["permissions"].append("core:default")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            verify_desktop_webview_shell_boundary(a, b, c)
        a["permissions"] = "core:default"
        with self.assertRaisesRegex(ValueError, "Malformed"):
            verify_desktop_webview_shell_boundary(a, b, c)


if __name__ == "__main__":
    unittest.main()
