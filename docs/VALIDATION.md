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

## Capability-truth and onboarding candidate

The capability-aware implementation includes JavaScript syntax, workbench-contract, source-boundary, and repository validation with static assertions for:

- the server-authoritative `/api/v1/config/endpoints-availability` capability request;
- fail-closed execution when a tool is disabled or availability is unknown;
- submit gating through the unified `availabilityState(...)` authority rather than the retired per-tool `available` property;
- first-use onboarding state persistence;
- voluntary Guide replay;
- global contextual-hint preference;
- per-hint dismissal;
- required Guide, onboarding, and contextual-hint surfaces in the packaged entry source.

Rendered-browser behavior, clean-profile onboarding, interruption/resume, replay, hint persistence, responsive presentation, keyboard/screen-reader behavior, and representative enabled/disabled/dependency capability states remain pending exact-head runtime/CI acceptance and are not claimed as verified here.

## Conversion and image-watermark verification

The 22-workflow conversion/image-watermark expansion is merged and source/build/test verified:

- PR #11 exact head `b37473530509e1189ab1f32132c4f67032929a2f` passed Repository and source boundary, Compile and package core, and Core test suite in GitHub Actions run `37708184781`;
- PR #11 merged to protected `main` as `a0956be4ded11c1a04f1fc2396fc075bc50aba12`;
- post-merge push run `37708434868` passed the same three jobs on that exact main revision;
- the merged topic branch was removed and the remaining non-main branches are active Dependabot branches;
- the local pre-merge JDK 25 evidence also included repository validation, successful core JAR packaging, focused `EndpointConfigurationTest`, packaged-JAR readback, and `git diff --check`.

This verifies the repository source/build/test state only. Rendered end-user conversion behavior and broader fidelity/accessibility acceptance remain open.

## Forms, attachments, and signature-removal candidate

The current `feature/forms-attachments-signatures` candidate has local evidence for the 26-workflow expansion:

- `./scripts/validate_repository.sh` passes with `workbench-contract: PASS (26 ready workflows, server-authoritative availability)`;
- `./gradlew :stirling-pdf:bootJar -PnoSpotless --no-daemon` completes successfully on JDK 25;
- focused `EndpointConfigurationTest`, `AttachmentControllerTest`, `AttachmentControllerMoreTest`, `UnlockPDFFormsControllerTest`, `UnlockPDFFormsControllerMoreTest`, and `RemoveCertSignControllerTest` runs complete successfully;
- packaged-JAR readback confirms form unlock, add/extract attachments, certificate-signature removal, and multi-file `FormData.getAll(...)` handling are present in the shipped workbench asset;
- `git diff --check` passes.

The filtered test runs report low aggregate JaCoCo percentages because only the targeted classes are selected; those coverage percentages are informational for these focused runs and the Gradle tasks completed successfully. Exact-head GitHub CI and rendered end-user acceptance remain required before this candidate can be represented as merged or runtime-accepted.

## Acceptance boundary

These results support Forge source validation only. They do not establish Seal or Anchor, production deployment acceptance, full hostile-file security acceptance, Glaze human/accessibility acceptance, or GoreeCloud platform-system production acceptance.
