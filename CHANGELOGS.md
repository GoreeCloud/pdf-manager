# Changelogs

## Unreleased

### Native Rust foundation and Lab lifecycle — 2026-09-28

- Established a Rust 2024 workspace on Rust 1.85.1 with unsafe Rust forbidden by workspace policy.
- Added the standard-library-only `goreecloud-pdf-core` bounded PDF preflight library.
- Added a development-only `pdf-manager-cli inspect` command for exercising the preflight boundary.
- Added unit tests for header detection, version parsing, size limits, EOF-marker hints, and bounded scanning.
- Added Rust Foundation CI for formatting, workspace build, unit tests, and clippy with warnings denied.
- Added architecture, dependency, and contribution records.
- Reconciled lifecycle from **Seed** to **Lab** because exploratory implementation now exists and is source-validated.
- Kept every full product capability area planned; the preflight foundation is not full PDF validation, sanitization, security scanning, repair, or a user-facing application.

The source validation establishes an exploratory implementation foundation only. It does not establish a supported platform, release, deployment, production acceptance, or Integral Platform System conformance.


### Licensing — 2026-09-28

- Selected `AGPL-3.0-or-later` under the GoreeCloud Software Licensing Policy.
- Added a root `LICENSE` rights grant.
- Reconciled `RIGHTS.md`, README, specifications, benefits, and the Platform Contract licensing blocker.
- Preserved the requirement to review future third-party dependencies for license compatibility and notices.

This licensing change does not represent application implementation, release, deployment, or production validation.

### Repository controls and lifecycle reconciliation — 2026-09-28

- Added mandatory `BRANDING.md`, `USER-MANUAL.md`, `SECURITY.md`, `NOTES.md`, `.gitignore`, `.editorconfig`, and `goreecloud.platform.yaml` repository controls.
- Added `RIGHTS.md` as an interim no-license-grant rights notice while the required recognized open-source license decision remains open.
- Reconciled the project to the canonical **Seed** lifecycle terminology while keeping implementation status explicitly pre-implementation.
- Added a truthful nine-system Platform Contract declaration with every runtime integration blocked/unverified.
- Kept all user-facing and production capabilities unclaimed.

No application implementation, release, deployment, production acceptance, or open-source license grant is represented by these changes.


### Documentation baseline — 2026-09-28

- Added the mandatory repository-level `SPECIFICATIONS.md`.
- Added `FEATURES.md` with explicit current, partial, planned, and removed-state boundaries.
- Added `BENEFITS.md` without claiming unimplemented user-facing benefits.
- Added `COMPETITIVE-OBJECTIVES.md` with current public benchmark references.
- Expanded the README to link the complete repository documentation set.
- Documented that no repository license is currently present or approved.
- Clarified the authority boundary between repository-level specifications and detailed project-scope requirements.

No application implementation, release, deployment, or production validation is represented by these documentation changes.

### Initial product scope — 2026-09-28

- Established the repository's initial authoritative project specification.
- Recorded the complete supplied PDF Manager feature set as planned work.
- Added an explicit implemented-feature inventory showing that no application features are currently verified.
- Added a current-state capability inventory that separates planned scope from implemented behavior.
- Added the initial project record.
- Expanded the README with project status, role, and documentation links.

No application implementation, release, deployment, or production validation is represented by this documentation change.
