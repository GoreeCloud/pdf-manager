"""Offline Cargo.lock candidate-path tests; no Cargo code or network executed."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import native_advisory_paths as mod


def fixture(with_native=True):
    pkgs = [
        {"name": "goreecloud-pdf-manager", "version": "0.1.0",
         "dependencies": ["tauri", "rand 0.10.3"]},
        {"name": "tauri", "version": "2.11.5",
         "dependencies": ["gtk", "phf_codegen 0.8.0"] if with_native else []},
        {"name": "gtk", "version": "0.18.2", "dependencies": ["glib"]},
        {"name": "glib", "version": "0.18.5", "dependencies": []},
        {"name": "phf_codegen", "version": "0.8.0",
         "dependencies": ["phf_generator 0.8.0"]},
        {"name": "phf_generator", "version": "0.8.0",
         "dependencies": ["rand 0.7.3"]},
        {"name": "rand", "version": "0.7.3", "dependencies": []},
        {"name": "rand", "version": "0.10.3", "dependencies": []},
    ]
    return {"version": 4, "package": pkgs}


class NativeAdvisoryPathsTests(unittest.TestCase):
    def test_shortest_exact_versions_and_caution(self):
        report = mod.dependency_path_report(fixture())
        self.assertFalse(report["security_release_approved"])
        self.assertFalse(report["source_license_cleared"])
        self.assertEqual(len(report["advisories"]), 2)
        for item in report["advisories"]:
            self.assertTrue(item["version_present_in_lockfile"])
            self.assertTrue(item["candidate_path_available"])
            self.assertFalse(item["path_has_ambiguous_version_resolution"])
            self.assertEqual(item["candidate_path_from_root"][0]["package"],
                             "goreecloud-pdf-manager")
            self.assertEqual(item["candidate_path_from_root"][-1]["package"], item["package"])
            self.assertEqual(item["remediation_status"], "NOT_VERIFIED")
            self.assertEqual(item["runtime_exploitability"], "NOT_ASSESSED")

    def test_version_present_does_not_imply_root_reachability(self):
        report = mod.dependency_path_report(fixture(with_native=False))
        self.assertTrue(all(x["version_present_in_lockfile"] for x in report["advisories"]))
        self.assertFalse(any(x["candidate_path_available"] for x in report["advisories"]))

    def test_missing_target_does_not_claim_remediation(self):
        lock = fixture()
        lock["package"] = [p for p in lock["package"] if p["name"] != "glib"]
        lock["package"] = [
            {**p, "dependencies": []} if p["name"] == "gtk" else p
            for p in lock["package"]
        ]
        report = mod.dependency_path_report(lock)
        glib = next(x for x in report["advisories"] if x["package"] == "glib")
        self.assertFalse(glib["version_present_in_lockfile"])
        self.assertEqual(glib["remediation_status"], "NOT_VERIFIED")
        self.assertFalse(report["security_release_approved"])

    def test_ambiguous_unversioned_edge_is_explicitly_flagged(self):
        lock = fixture()
        root = lock["package"][0]
        root["dependencies"] = ["rand"]
        report = mod.dependency_path_report(lock)
        rand = next(x for x in report["advisories"] if x["package"] == "rand")
        self.assertTrue(rand["candidate_path_available"])
        self.assertTrue(rand["path_has_ambiguous_version_resolution"])

    def test_missing_package_rejected(self):
        lock = fixture()
        lock["package"][0]["dependencies"].append("not-a-real-package 1.0.0")
        with self.assertRaisesRegex(ValueError, "Unresolved"):
            mod.dependency_path_report(lock)

    def test_duplicate_package_identity_rejected(self):
        lock = fixture()
        lock["package"].append(dict(lock["package"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            mod.dependency_path_report(lock)

    def test_unsafe_dependency_text_is_rejected(self):
        lock = fixture()
        lock["package"][0]["dependencies"] = ["broken 1.0.0 unexpected"]
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            mod.dependency_path_report(lock)

    def test_missing_or_duplicate_roots_rejected(self):
        lock = fixture()
        lock["package"][0]["name"] = "other-application"
        with self.assertRaisesRegex(ValueError, "precisely one"):
            mod.dependency_path_report(lock)

    def test_cycle_terminates_and_path_bounded(self):
        lock = fixture()
        lock["package"][1]["dependencies"] = ["goreecloud-pdf-manager", "gtk"]
        report = mod.dependency_path_report(lock)
        self.assertLessEqual(report["package_count"], mod.MAX_PACKAGES)
        for result in report["advisories"]:
            self.assertLess(len(result["candidate_path_from_root"]), mod.MAX_PATH_NODES)

    def test_deterministic_package_order(self):
        lock = fixture()
        first = mod.dependency_path_report(lock)
        lock["package"].reverse()
        second = mod.dependency_path_report(lock)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
