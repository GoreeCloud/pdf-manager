"""No-network, no-license-text interpretation: tracked notice candidate queue tests."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_notice_review_queue as evidence


class NoticeReviewQueueTests(unittest.TestCase):
    def test_same_directory_candidate_only(self):
        assets = ["public/fonts/Alpha.woff2", "public/icons/Beta.svg", "public/other/Gamma.pdf"]
        tracked = assets + [
            "public/fonts/LICENSE-fonts.txt",
            "public/icons/COPYING.md",
            "public/LICENSE",
            "LICENSE",
        ]
        result = evidence.match_license_notices(assets, tracked)
        self.assertEqual(result["asset_count"], 3)
        self.assertEqual(result["assets_with_adjacent_notices"], 2)
        by_asset = {x["asset"]: x for x in result["review_queue"]}
        self.assertEqual(by_asset["public/fonts/Alpha.woff2"]["adjacent_notice_candidates"],
                         ["public/fonts/LICENSE-fonts.txt"])
        self.assertEqual(by_asset["public/icons/Beta.svg"]["adjacent_notice_candidates"],
                         ["public/icons/COPYING.md"])
        self.assertEqual(by_asset["public/other/Gamma.pdf"]["adjacent_notice_candidates"], [])

    def test_noto_license_and_lucide_notice_recognized(self):
        result = evidence.match_license_notices(
            ["fonts/NotoSans.ttf", "icons/icon.svg"],
            ["fonts/NotoSans-OFL.txt", "icons/LICENSE-lucide.txt"],
        )
        self.assertEqual(result["assets_with_adjacent_notices"], 2)

    def test_license_named_source_and_json_do_not_count(self):
        result = evidence.match_license_notices(
            ["icons/example.svg"],
            ["icons/LicenseServiceInterface.java", "icons/license-states.spec.ts",
             "icons/license-overrides.json", "LICENSE"],
        )
        self.assertEqual(result["assets_with_adjacent_notices"], 0)

    def test_always_unverified_even_with_notice(self):
        result = evidence.match_license_notices(["icons/a.svg"], ["icons/LICENSE"])
        self.assertEqual(result["rights_verified"], 0)
        self.assertTrue(all(x["redistribution_rights"] == "UNVERIFIED" for x in result["review_queue"]))
        self.assertIn("REVIEW QUEUE ONLY", result["status"])

    def test_deterministic_paths_and_notice_order(self):
        assets = ["icons/b.svg", "icons/a.svg"]
        files = ["icons/NOTICE.md", "icons/LICENSE", "icons/a.svg"]
        result = evidence.match_license_notices(assets, list(reversed(files)))
        self.assertEqual([x["asset"] for x in result["review_queue"]], ["icons/a.svg", "icons/b.svg"])
        self.assertEqual(result["review_queue"][0]["adjacent_notice_candidates"],
                         ["icons/LICENSE", "icons/NOTICE.md"])

    def test_untrusted_path_traversal_rejected(self):
        for bad in ("/outside/license", "../outside.txt", "icons/../../evil.svg", ".git/private.txt"):
            with self.assertRaisesRegex(ValueError, "Unsafe tracked path"):
                evidence.match_license_notices(["icons/a.svg"], [bad])
            with self.assertRaisesRegex(ValueError, "Unsafe tracked path"):
                evidence.match_license_notices([bad], ["icons/LICENSE"])

    def test_missing_notices_never_implies_unlicensed(self):
        result = evidence.match_license_notices(["icons/a.svg"], [])
        self.assertEqual(result["assets_without_adjacent_notices"], 1)
        self.assertEqual(result["review_queue"][0]["redistribution_rights"], "UNVERIFIED")
        self.assertTrue(result["notice_presence_does_not_imply"])


if __name__ == "__main__":
    unittest.main()
