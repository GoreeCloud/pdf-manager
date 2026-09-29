# Notes

## Working state

GoreeCloud PDF Manager is currently a **Lab**-stage exploratory implementation.

Verified foundation:

- Native Rust 2024 workspace on Rust 1.85.1.
- `unsafe_code = "forbid"`.
- No third-party runtime crates in the first slice.
- Bounded PDF input preflight library.
- Development-only preflight CLI.
- Unit tests and GitHub Actions validation for formatting, build, tests, and clippy.
- AGPL-3.0-or-later project license.

There is no usable end-user application, full PDF engine, supported deployment, or production acceptance.

## Immediate development decisions still open

- Select open-source PDF parsing, editing, and rendering foundations.
- Define process isolation, resource enforcement, and untrusted-document sandboxing.
- Select OCR, office-conversion, image, signature, and archival-format foundations.
- Define persistent storage, metadata, job, and temporary-file models.
- Define web/desktop client boundaries and the first user-facing Glaze UI surface.
- Define REST API and asynchronous job contracts.
- Define MCP authorization and operation boundaries.
- Define the first usable product feature slice and representative PDF fixture corpus.
- Add malformed, adversarial, and resource-exhaustion document fixtures.
- Establish accepted Platform Contract validation and Integral Platform System runtime integration evidence.

## Closed foundation decisions

- Native implementation language/runtime: Rust 2024, current minimum Rust 1.85.1.
- Initial dependency posture: Rust standard library only.
- Project license: AGPL-3.0-or-later.
- Source-validation workflow: rustfmt, workspace build, unit tests, and clippy with warnings denied.

These decisions may evolve through governed architecture changes; they are not claims that the final PDF engine or product stack has been selected.

## Documentation boundaries

- `SPECIFICATIONS.md` is the canonical repository-level implementation contract.
- `PROJECT-SPECIFICATIONS.md` holds the detailed product scope.
- `IMPLEMENTED-FEATURES.md` controls evidence-backed implemented feature state.
- `PLANNED-FEATURES.md` controls planned feature obligations.
- `CAPABILITIES.md` summarizes current verified capability state.
- `CHANGELOGS.md` records meaningful repository changes.
- `PROJECT-RECORD.md` records significant project history and evidence.
- `DEPENDENCIES.md` records material dependency state and selection rules.
- `docs/ARCHITECTURE.md` records the current native architecture boundary.

## Current known limitations

The repository cannot yet provide normal user-facing PDF workflows. The development preflight can perform only the narrowly documented bounded structural inspection.

No supported application release or deployment exists.
