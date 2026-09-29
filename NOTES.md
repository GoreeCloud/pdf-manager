# Notes

## Working state

GoreeCloud PDF Manager is currently a **Seed**-stage, documentation-only repository.

No application source, runtime, selected PDF-processing engine, tests, deployment artifact, release, or production acceptance is verified.

## Immediate development decisions still open

- Select the product architecture and implementation language/runtime.
- Select open-source PDF parsing/editing/rendering foundations.
- Select OCR, office-conversion, image, signature, and archival-format foundations.
- Define process isolation and untrusted-document sandboxing.
- Define persistent storage, metadata, job, and temporary-file models.
- Define web/desktop client boundaries.
- Define REST API and asynchronous job contracts.
- Define MCP authorization and operation boundaries.
- Define the first usable feature slice and test fixture corpus.
- Select and approve the long-term recognized open-source software license.
- Establish CI and repository validation appropriate to the selected stack.
- Establish accepted Platform Contract validation and Integral Platform System integration evidence.

## Documentation boundaries

- `SPECIFICATIONS.md` is the canonical repository-level implementation contract.
- `PROJECT-SPECIFICATIONS.md` holds the detailed product scope.
- `IMPLEMENTED-FEATURES.md` controls evidence-backed implemented feature state.
- `PLANNED-FEATURES.md` controls planned feature obligations.
- `CAPABILITIES.md` summarizes current verified capability state.
- `CHANGELOGS.md` records meaningful repository changes.
- `PROJECT-RECORD.md` records significant project history and evidence.

## Current known limitations

The repository is not yet a software product and cannot process user documents.

Public repository visibility does not grant reuse rights. See [RIGHTS.md](RIGHTS.md) until an approved open-source license replaces the interim rights notice.
