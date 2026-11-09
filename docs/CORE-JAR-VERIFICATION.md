# GoreeCloud PDF Manager — Core-only Java archive verification

**Evidence class:** Nonpublishing build and static archive check only. Not a signed release, a deployed server, a complete SBOM, a runtime test, or legal clearance.

## Why this check exists

A successful Java compilation and controller test does not prove an executable core-only Spring Boot application archive can be assembled from the sanitized MIT-only import. The [Open-core build diagnostics](../.github/workflows/core-build.yml) therefore also run a Python verifier after assembling the core-only JAR. The commands are:

    python3 -m unittest discover -s scripts/tests -p test_verify_core_jar.py -v
    gradle :stirling-pdf:bootJar -PbuildWithFrontend=false --no-daemon --stacktrace
    python3 scripts/verify_core_jar.py --jar PATH_TO_GENERATED_JAR

The CI workflow discovers the actual generated filename. Run manually only in an isolated development environment with the source's verified Java 25/Gradle 9.7.1 toolchain.

## Static checks

The standard-library-only verifier inspects the archive without executing, extracting or uploading it. It requires:

- A regular, nonsymlinked, nonempty archive within a conservative size bound
- Unique ZIP entry names; Spring Boot JarLauncher and SPDFApplication entries
- GoreeCloud PDF Manager implementation title and the expected Spring Boot executable entrypoint in the manifest
- Embedded Spring Boot runtime libraries
- No obvious excluded proprietary or SaaS module names in the ZIP entry list

Nine fixtures test expected structure and rejection of invalid or duplicate archives, missing launch classes or libraries, old upstream branding, prohibited modules and symlink input.

## Nonpublishing embedded dependency inventory

The same required Java 25 CI job additionally performs the [runtime library
evidence check](CORE-RUNTIME-LIBRARY-EVIDENCE.md) against the **actual compiled
archive**. It hashes the contents of each nested BOOT-INF/lib/*.jar, records
its uncompressed byte count and filename, and compares two independently
generated JSON reports for exact reproducibility. The inventory is kept only
inside the disposable runner; it is not uploaded as a package or release asset.
Neither existence nor hashing of a nested JAR establishes licensing rights or
security acceptance.

## What this does not prove

The archive is built with frontend assets disabled, so web UI inclusion is not tested. This static check does not start a server, exercise actual HTTP upload/processing, validate authentication or tenant isolation, inspect nested dependency classes/assets and embedded licenses, execute malware scans, evaluate third-party rights, or sign or distribute anything. Filename-level exclusion checking is not proof that restricted code could never enter another transitive artifact.

Release readiness still requires end-to-end disposable deployment, full source/asset rights review, resolved Java dependency inventory, security scanning, reproducibility evidence, privacy acceptance, signing and publication approval. A passing result may be reported only as **nonpublishing JAR structure verified**, not an installable or production-ready release.
