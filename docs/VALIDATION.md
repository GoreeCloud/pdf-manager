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

## Conversion and image-watermark merge evidence

The 22-workflow conversion/image-watermark expansion was verified on GitHub before and after merge:

- PR #11 exact head `b37473530509e1189ab1f32132c4f67032929a2f` passed the protected **Repository and source boundary**, **Compile and package core**, and **Core test suite** checks in workflow run `37708184781`;
- PR #11 merged to protected `main` as GitHub-signed commit `a0956be4ded11c1a04f1fc2396fc075bc50aba12`;
- post-merge `main` workflow run `37708434868` completed successfully on that exact merge commit.

## Forms, attachments, and signature-removal merge evidence

- PR #12 exact head `bbe1d84f4df9333783dcd08695f93f0204307b96` passed the protected three-job validation workflow in run `37709997018`;
- PR #12 merged to protected `main` as `9519d3c312d203f849b8f7d48f4ba6bf40a434c4`;
- post-merge workflow run `37710280996` passed **Repository and source boundary**, **Compile and package core**, and **Core test suite** on that exact merge commit.

## Combined document utility candidate

The document-utility branch is forward-merged with PR #12's verified `main` and has fresh local evidence for the combined 31-workflow candidate:

- `node --check app/core/src/main/resources/static/goreecloud/pdf-manager.js` passes;
- `./scripts/validate_repository.sh` passes with `workbench-contract: PASS (31 ready workflows, server-authoritative availability)`;
- focused `EndpointConfigurationTest` execution passes after synchronization;
- `./gradlew :stirling-pdf:bootJar -PnoSpotless --no-daemon` completes successfully on JDK 25;
- packaged-JAR readback confirms the utility workflows, form unlock, attachment add/extract, certificate-signature removal, multi-file attachment handling, expanded workspace input acceptance, and `validateWorkspaceForTool` are all present in the same shipped workbench asset;
- `git diff --check` passes;
- PDF→images intentionally excludes WebP until its additional Python-specific dependency can be represented by authoritative option-level capability evidence.

The focused unit-test run reports low aggregate JaCoCo percentages because only one small test class is selected; those percentages are informational for the filtered run and the Gradle task completed successfully. Exact-head GitHub CI is still required on the synchronized PR #13 head before merge. Rendered end-user behavior and broader fidelity/accessibility acceptance remain separate from source/build/test acceptance.

## Acceptance boundary

These results support Forge source validation only. They do not establish Seal or Anchor, production deployment acceptance, full hostile-file security acceptance, Glaze human/accessibility acceptance, or GoreeCloud platform-system production acceptance.
