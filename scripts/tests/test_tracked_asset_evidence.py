"""Offline tests: no code execution, license assertions, or network activity."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tracked_asset_evidence as evidence


class AssetEvidenceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="gcpdf-assets-tests-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.put("public/fonts/example.ttf", b"sample_font_bytes")
        self.put("public/logo.svg", b'<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.put("app/core/src/test/resources/synthetic.pdf", b"%PDF-1.4\nsynthetic")
        self.put("src/code.ts", b"export const ok = true;")
        self.add()

    def put(self, rel, data):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)

    def add(self):
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_tracks_only_binary_asset_candidates(self):
        report = evidence.build_report(self.root)
        self.assertEqual(report["candidate_count"], 3)
        self.assertEqual(report["hashed_count"], 3)
        self.assertEqual({r["category"] for r in report["candidates"]}, {"font", "image", "document"})
        self.assertFalse(any("licenses" in r for r in report["candidates"]))
        self.assertTrue(all(r["license_status"] == "UNVERIFIED" for r in report["candidates"]))
        font = next(x for x in report["candidates"] if x["category"]=="font")
        self.assertEqual(font["sha256"], hashlib.sha256(b"sample_font_bytes").hexdigest())

    def test_output_byte_determinism(self):
        self.assertEqual(evidence.render(self.root), evidence.render(self.root))

    def test_staged_symlink_never_dereferenced(self):
        (self.root / "external.ttf").symlink_to("/etc/passwd")
        self.add()
        x = evidence.build_report(self.root)
        y = next(v for v in x["candidates"] if v["path"] == "external.ttf")
        self.assertEqual(y["state"], "tracked-symlink-not-read")
        self.assertNotIn("sha256", y)

    def test_tracked_asset_under_symlinked_parent_is_never_read(self):
        # Reproduce a working-tree directory replaced after git add.
        # The external target contains only generated, non-user test bytes.
        with tempfile.TemporaryDirectory(prefix="gcpdf-synthetic-outside-") as outside:
            outside_root = Path(outside)
            external_bytes = b"SYNTHETIC_EXTERNAL_DIRECTORY_TEST_ONLY"
            (outside_root / "example.ttf").write_bytes(external_bytes)
            shutil.rmtree(self.root / "public/fonts")
            (self.root / "public/fonts").symlink_to(outside_root, target_is_directory=True)

            report = evidence.build_report(self.root)
            entry = next(x for x in report["candidates"] if x["path"] == "public/fonts/example.ttf")
            self.assertEqual(entry["state"], "tracked-symlink-not-read")
            self.assertEqual(entry["license_status"], "UNVERIFIED")
            self.assertNotIn("sha256", entry)
            self.assertNotIn("bytes", entry)

    def test_deleted_staged_file_is_reported_not_opened(self):
        (self.root / "public/logo.svg").unlink()
        x = evidence.build_report(self.root)
        y = next(v for v in x["candidates"] if v["path"]=="public/logo.svg")
        self.assertEqual(y["state"], "tracked-file-missing")

    def test_untracked_asset_is_not_in_inventory(self):
        self.put("private/untracked.ttf", b"not-staged")
        x = evidence.build_report(self.root)
        self.assertFalse(any(z["path"]=="private/untracked.ttf" for z in x["candidates"]))

    def test_large_asset_fails_bounded_scan(self):
        self.put("public/fonts/example.ttf", b"0"*(evidence.MAX_ASSET_SIZE+1))
        with self.assertRaisesRegex(ValueError, "bounded read limit"):
            evidence.build_report(self.root)

    def test_full_checkout_contains_assets_without_license_inference(self):
        repo = Path(__file__).resolve().parents[2]
        report = evidence.build_report(repo)
        self.assertEqual(report["candidate_count"], len(report["candidates"]))
        self.assertEqual(report["hashed_count"], sum(
            x["state"] == "tracked-asset-bytes-hashed"
            for x in report["candidates"]
        ))
        self.assertEqual(report["status"], "METADATA ONLY — NOT LICENSE CLEARED OR RELEASE READY")
        self.assertNotIn("release_approved", report)


if __name__ == "__main__":
    unittest.main()
