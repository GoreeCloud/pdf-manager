"""No JAR execution or untrusted dependency loading in these structure tests."""
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_core_jar import APP_CLASS, MAIN_LAUNCHER, inspect_core_jar

MANIFEST = (
    "Manifest-Version: 1.0\r\n"
    "Main-Class: org.springframework.boot.loader.launch.JarLauncher\r\n"
    "Start-Class: stirling.software.SPDF.SPDFApplication\r\n"
    "Implementation-Title: GoreeCloud PDF Manager\r\n\r\n"
)


class CoreJarTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.jar = Path(directory.name) / "core.jar"

    def make_jar(self, overrides=None, omitted=()):
        entries = {
            "META-INF/MANIFEST.MF": MANIFEST.encode(),
            APP_CLASS: b"test-only-bytecode-fixture",
            MAIN_LAUNCHER: b"test-only-launcher-fixture",
            "BOOT-INF/lib/pdfbox-3.0.8.jar": b"test-only-library-fixture",
        }
        if overrides:
            entries.update(overrides)
        for key in omitted:
            entries.pop(key, None)
        with zipfile.ZipFile(self.jar, "w") as archive:
            for name, content in entries.items():
                archive.writestr(name, content)

    def test_valid_structure_is_clearly_not_runtime_verified(self):
        self.make_jar()
        result = inspect_core_jar(self.jar)
        self.assertEqual(result["implementation_title"], "GoreeCloud PDF Manager")
        self.assertEqual(result["library_count"], 1)
        self.assertFalse(result["release_approved"])
        self.assertFalse(result["runtime_tested"])
        self.assertFalse(result["license_cleared"])

    def test_rejects_upstream_branding_in_manifest(self):
        self.make_jar({"META-INF/MANIFEST.MF": MANIFEST.replace(
            "Implementation-Title: GoreeCloud PDF Manager",
            "Implementation-Title: Stirling-PDF").encode()})
        with self.assertRaisesRegex(ValueError, "implementation title"):
            inspect_core_jar(self.jar)

    def test_rejects_proprietary_module(self):
        self.make_jar({"BOOT-INF/lib/stirling-pdf-proprietary-3.3.0.jar": b"fixture"})
        with self.assertRaisesRegex(ValueError, "proprietary"):
            inspect_core_jar(self.jar)

    def test_rejects_saas_class(self):
        self.make_jar({"BOOT-INF/classes/com/company/saas/Commercial.class": b"fixture"})
        with self.assertRaisesRegex(ValueError, "SaaS"):
            inspect_core_jar(self.jar)

    def test_rejects_missing_launcher(self):
        self.make_jar(omitted=(MAIN_LAUNCHER,))
        with self.assertRaisesRegex(ValueError, "Missing executable"):
            inspect_core_jar(self.jar)

    def test_rejects_missing_runtime_libraries(self):
        self.make_jar(omitted=("BOOT-INF/lib/pdfbox-3.0.8.jar",))
        with self.assertRaisesRegex(ValueError, "runtime libraries"):
            inspect_core_jar(self.jar)

    def test_rejects_invalid_zip(self):
        self.jar.write_bytes(b"not a JAR")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            inspect_core_jar(self.jar)

    def test_rejects_symlinks(self):
        self.make_jar()
        link = self.jar.with_name("linked.jar")
        link.symlink_to(self.jar)
        with self.assertRaisesRegex(ValueError, "non-symlinked"):
            inspect_core_jar(link)

    def test_rejects_duplicate_names(self):
        with zipfile.ZipFile(self.jar, "w") as archive:
            archive.writestr("META-INF/MANIFEST.MF", MANIFEST)
            archive.writestr("META-INF/MANIFEST.MF", MANIFEST)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            inspect_core_jar(self.jar)


if __name__ == "__main__":
    unittest.main()
