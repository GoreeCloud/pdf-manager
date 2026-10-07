# Validation — GoreeCloud PDF Manager

Validation below was performed on the Forge rebuild candidate on 2026-10-07 before the final branch update.

## Passed

- `./scripts/validate_repository.sh`
  - restricted/ambiguous Stirling trees absent;
  - core-only Gradle graph enforced;
  - canonical PDF Manager branding blob exact;
  - Glaze V1.7 module closure complete;
  - GoreeCloud shell contains no unexpected external/tracking references;
  - required repository records present.
- `./gradlew :stirling-pdf:compileJava -PnoSpotless --no-daemon`
- `./gradlew :stirling-pdf:bootJar -PnoSpotless --no-daemon`
- Packaged JAR inspection:
  - `Implementation-Title: GoreeCloud PDF Manager`;
  - `Implementation-Version: 0.1.0-dev`;
  - GoreeCloud workbench packaged as `static/index.html`;
  - Glaze V1.7 assets packaged;
  - GoreeCloud security-header filter packaged;
  - no restricted project entry names observed.
- `ToolChainValidatorConformanceTest` after restoring the required open-source `testing/tool-io-cases.json` fixture.
- `GoreeCloudWorkbenchSecurityHeadersFilterTest`.

## Host-limited full-suite result

A full `:common:test :stirling-pdf:test` run executed 2,177 tests on the authorized development laptop. The run produced native JPDFium failures because the host provides **GLIBC 2.35** while the retained upstream `libpdfium.so` requires **GLIBC 2.38**.

This is an environment compatibility limitation rather than a GoreeCloud source compilation failure. The missing tool-chain fixture discovered during that run has been restored and its dedicated conformance test now passes.

Canonical GitHub CI is pinned to Ubuntu 24.04 with Temurin JDK 25 so the native suite executes on a compatible runtime environment.

## Acceptance boundary

These results support Forge source validation only. They do not establish Seal or Anchor, production deployment acceptance, full hostile-file security acceptance, Glaze human/accessibility acceptance, or GoreeCloud platform-system production acceptance.
