"""Pure synthetic archive tests; never execute or extract nested runtime JARs."""
import hashlib
import io
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import runtime_jar_inventory as inv


def jar_bytes(marker=b"offline synthetic"):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as archive:
        archive.writestr("META-INF/MANIFEST.MF", marker)
        archive.writestr("synthetic/Example.class", b"not executable bytecode")
    return buf.getvalue()


class EmbeddedJarMetadataTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="gcpdf-jar-evidence-test-")
        self.addCleanup(temp.cleanup)
        self.jar = Path(temp.name) / "synthetic-core.jar"

    def make_archive(self, entries=None):
        if entries is None:
            entries = [
                ("BOOT-INF/lib/", None),
                ("BOOT-INF/lib/alpha-1.jar", jar_bytes(b"alpha")),
                ("BOOT-INF/lib/beta-2.jar", jar_bytes(b"beta")),
                ("BOOT-INF/classes/main.class", b"synthetic class"),
            ]
        with zipfile.ZipFile(self.jar, "w") as archive:
            for name, value in entries:
                archive.writestr(name, b"" if value is None else value)

    def test_inventory_hashes_and_sorting_deterministic(self):
        self.make_archive()
        first = inv.inspect_runtime_libraries(self.jar)
        second = inv.inspect_runtime_libraries(self.jar)
        self.assertEqual(first, second)
        self.assertEqual(first["library_count"], 2)
        self.assertFalse(first["license_cleared"])
        self.assertFalse(first["release_approved"])
        self.assertEqual(first["source_sha256"], hashlib.sha256(self.jar.read_bytes()).hexdigest())
        self.assertEqual([x["file"] for x in first["libraries"]], ["alpha-1.jar", "beta-2.jar"])
        self.assertEqual(
            first["libraries"][0]["sha256"], hashlib.sha256(jar_bytes(b"alpha")).hexdigest()
        )
        self.assertTrue(all(x["license_status"] == "UNVERIFIED" for x in first["libraries"]))
        self.assertTrue(all(x["vulnerability_status"] == "NOT_ASSESSED" for x in first["libraries"]))

    def test_mutated_dependency_content_changes_hash(self):
        self.make_archive([("BOOT-INF/lib/alpha.jar", jar_bytes(b"original"))])
        original = inv.inspect_runtime_libraries(self.jar)["libraries"][0]["sha256"]
        self.make_archive([("BOOT-INF/lib/alpha.jar", jar_bytes(b"changed"))])
        updated = inv.inspect_runtime_libraries(self.jar)["libraries"][0]["sha256"]
        self.assertNotEqual(original, updated)

    def test_non_jar_runtime_members_fail(self):
        self.make_archive([("BOOT-INF/lib/debug.txt", b"hello")])
        with self.assertRaisesRegex(ValueError, "non-JAR"):
            inv.inspect_runtime_libraries(self.jar)

    def test_path_traversal_inside_library_names_fail(self):
        for name in ("BOOT-INF/lib/deep/a.jar", "BOOT-INF/lib/../outside.jar"):
            self.make_archive([(name, jar_bytes())])
            with self.assertRaisesRegex(ValueError, "library path"):
                inv.inspect_runtime_libraries(self.jar)

    def test_commercial_names_fail(self):
        self.make_archive([("BOOT-INF/lib/sample-proprietary-1.jar", jar_bytes())])
        with self.assertRaisesRegex(ValueError, "commercial"):
            inv.inspect_runtime_libraries(self.jar)

    def test_nonjar_magic_bytes_fail(self):
        self.make_archive([("BOOT-INF/lib/malicious.jar", b"not a ZIP archive")])
        with self.assertRaisesRegex(ValueError, "ZIP/JAR"):
            inv.inspect_runtime_libraries(self.jar)

    def test_missing_runtime_libraries_fail(self):
        self.make_archive([("BOOT-INF/classes/app.class", b"class")])
        with self.assertRaisesRegex(ValueError, "No BOOT-INF"):
            inv.inspect_runtime_libraries(self.jar)

    def test_duplicate_entries_fail(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            self.make_archive([
                ("BOOT-INF/lib/duplicate.jar", jar_bytes()),
                ("BOOT-INF/lib/duplicate.jar", jar_bytes()),
            ])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            inv.inspect_runtime_libraries(self.jar)

    def test_symlink_input_and_zip_member_fail(self):
        self.make_archive()
        link = self.jar.with_name("linked.jar")
        link.symlink_to(self.jar)
        with self.assertRaisesRegex(ValueError, "non-symlinked"):
            inv.inspect_runtime_libraries(link)
        member = zipfile.ZipInfo("BOOT-INF/lib/virtual.jar")
        member.create_system = 3
        member.external_attr = (0o120777 << 16)
        self.make_archive([(member, jar_bytes())])
        with self.assertRaisesRegex(ValueError, "Symlinked"):
            inv.inspect_runtime_libraries(self.jar)

    def test_size_limit_fail_closed(self):
        self.make_archive([("BOOT-INF/lib/oversized.jar", jar_bytes())])
        with patch.object(inv, "MAX_LIBRARY_BYTES", 8):
            with self.assertRaisesRegex(ValueError, "size"):
                inv.inspect_runtime_libraries(self.jar)


if __name__ == "__main__":
    unittest.main()
