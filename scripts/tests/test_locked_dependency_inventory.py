#!/usr/bin/env python3
"""Regression tests for the intentionally partial, offline lockfile inventory."""
import base64
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import locked_dependency_inventory as inventory


class LockfileInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        digest = base64.b64encode(hashlib.sha512(b"unit-test-tarball").digest()).decode("ascii")
        frontend = {
            "lockfileVersion": 3,
            "packages": {
                "": {"name": "fixture", "version": "0.0.1"},
                "node_modules/@fixture/pkg": {
                    "version": "1.2.3",
                    "integrity": "sha512-" + digest,
                    "license": "MIT", "dev": True,
                },
                "node_modules/other/node_modules/@fixture/pkg": {
                    "version": "1.2.3",
                    "integrity": "sha512-" + digest,
                    "dev": True,
                },
            },
        }
        devtools = {"lockfileVersion": 3, "packages": {
            "": {"name": "devtool-fixture", "version": "0.1.0"},
            "node_modules/pkg-tools": {"version": "2.0.0"},
        }}
        for rel, data in (("frontend/package-lock.json", frontend),
                          ("devTools/package-lock.json", devtools)):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data), encoding="utf-8")
        for rel in inventory.LOCKFILES[2:]:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                'version = 3\n\n[[package]]\nname = "pdf-preview-local"\nversion = "0.1.0"\n'
                '\n[[package]]\nname = "serde"\nversion = "1.2.0"\n'
                'source = "registry+https://github.com/rust-lang/crates.io-index"\n'
                'checksum = "' + "a" * 64 + '"\n',
                encoding="utf-8",
            )

    def test_deterministic_deduplicated_cyclonedx(self):
        one = inventory.render_inventory(self.root)
        two = inventory.render_inventory(self.root)
        self.assertEqual(one, two)
        bom = json.loads(one)
        self.assertEqual(bom["bomFormat"], "CycloneDX")
        self.assertEqual(bom["specVersion"], "1.5")
        self.assertEqual(len(bom["components"]), 3)
        self.assertEqual(len({item["bom-ref"] for item in bom["components"]}), 3)
        component = next(c for c in bom["components"] if c["name"] == "@fixture/pkg")
        self.assertEqual(component["purl"], "pkg:npm/%40fixture/pkg@1.2.3")
        self.assertEqual(component["hashes"][0]["alg"], "SHA-512")
        self.assertEqual(len(component["hashes"][0]["content"]), 128)
        self.assertTrue(any(p["name"] == "goreecloud:unverified-license-hint" for p in component["properties"]))
        self.assertNotIn("licenses", component)  # no unverified legal attribution
        self.assertFalse(any(c["name"] == "pdf-preview-local" for c in bom["components"]))
        self.assertEqual(len([p for p in bom["metadata"]["properties"] if "source-sha256:" in p["name"]]), 5)

    def test_missing_lockfile_fails_closed(self):
        (self.root / "frontend/src-tauri/provisioner/Cargo.lock").unlink()
        with self.assertRaisesRegex(ValueError, "Missing"):
            inventory.generate_inventory(self.root)

    def test_bad_integrity_fails_closed(self):
        path = self.root / "frontend/package-lock.json"
        data = json.loads(path.read_text())
        data["packages"]["node_modules/@fixture/pkg"]["integrity"] = "sha512-not-base64"
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Invalid npm lockfile integrity"):
            inventory.generate_inventory(self.root)

    def test_conflicting_hashes_fail_closed(self):
        path = self.root / "frontend/package-lock.json"
        data = json.loads(path.read_text())
        alt = base64.b64encode(hashlib.sha512(b"different-tarball").digest()).decode()
        data["packages"]["node_modules/@fixture/pkg"]["integrity"] = "sha512-" + alt
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            inventory.generate_inventory(self.root)

    def test_invalid_cargo_checksum_fails_closed(self):
        path = self.root / "frontend/src-tauri/Cargo.lock"
        path.write_text(path.read_text().replace("a" * 64, "broken"))
        with self.assertRaisesRegex(ValueError, "Invalid Cargo checksum"):
            inventory.generate_inventory(self.root)

    def test_real_checkout_metadata_is_partial(self):
        root = Path(__file__).resolve().parents[2]
        bom = inventory.generate_inventory(root)
        self.assertGreater(len(bom["components"]), 500)
        self.assertTrue(any(x["name"] == "goreecloud:known-exclusions"
                            for x in bom["metadata"]["properties"]))
        self.assertEqual({c["purl"] for c in bom["components"]},
                         {c["bom-ref"] for c in bom["components"]})


if __name__ == "__main__":
    unittest.main()
