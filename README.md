# GoreeCloud PDF Manager

GoreeCloud PDF Manager is a planned privacy-focused, self-hosted PDF and document-management platform for reading, editing, converting, organizing, securing, signing, scanning, automating, storing, and processing PDF documents.

## Project status

**Lifecycle:** Lab

As of September 28, 2026, the repository contains an exploratory native Rust implementation foundation: a reusable bounded PDF preflight core, a development-only CLI, unit tests, and CI validation. There is still no usable end-user PDF Manager application, PDF engine, service, deployment, or supported release. The broader documented product scope remains planned.

## Repository documentation

- [SPECIFICATIONS.md](SPECIFICATIONS.md) — canonical repository-level technical specification.
- [PROJECT-SPECIFICATIONS.md](PROJECT-SPECIFICATIONS.md) — detailed project scope and normative product requirements.
- [PROJECT-RECORD.md](PROJECT-RECORD.md) — significant project history and evidence.
- [FEATURES.md](FEATURES.md) — product feature-state overview.
- [BENEFITS.md](BENEFITS.md) — evidence-aware current and planned product benefits.
- [COMPETITIVE-OBJECTIVES.md](COMPETITIVE-OBJECTIVES.md) — benchmark objectives and deliberate product boundaries.
- [PLANNED-FEATURES.md](PLANNED-FEATURES.md) — open and future feature obligations.
- [IMPLEMENTED-FEATURES.md](IMPLEMENTED-FEATURES.md) — evidence-backed implemented feature inventory.
- [CAPABILITIES.md](CAPABILITIES.md) — current verified capability state.
- [CHANGELOGS.md](CHANGELOGS.md) — meaningful repository change history.
- [BRANDING.md](BRANDING.md) — canonical product naming and visual-identity boundaries.
- [USER-MANUAL.md](USER-MANUAL.md) — Lab-stage availability boundary and intended workflow model.
- [SECURITY.md](SECURITY.md) — repository-safe security and vulnerability guidance.
- [NOTES.md](NOTES.md) — repository working notes.
- [goreecloud.platform.yaml](goreecloud.platform.yaml) — machine-readable Platform Contract declaration.
- [LICENSE](LICENSE) — governing AGPL-3.0-or-later software license.
- [RIGHTS.md](RIGHTS.md) — project rights and third-party licensing notice.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — current native implementation architecture and boundaries.
- [DEPENDENCIES.md](DEPENDENCIES.md) — dependency inventory and selection rules.
- [CONTRIBUTING.md](CONTRIBUTING.md) — development and validation workflow.

## Product role

The project is intended to operate both as a standalone GoreeCloud PDF application and as the shared PDF-processing foundation for the wider GoreeCloud ecosystem.

## Current implementation boundary

A bounded development preflight can size-gate a PDF candidate, locate a PDF header within the first 1024 bytes, parse its version token, and report whether an EOF marker appears in the final 2048 bytes. This does **not** establish full PDF validity or document safety. PDF editing, rendering, conversion, OCR, scanning, forms, signatures, redaction, document-library, workflow, API, MCP/AI, storage-integration, collaboration, deployment, and enterprise-processing capabilities remain unimplemented.

## License

GoreeCloud PDF Manager is licensed under the **GNU Affero General Public License v3.0 or later** (`AGPL-3.0-or-later`). See [LICENSE](LICENSE).

The project remains Lab / exploratory implementation; licensing does not imply a software release, production readiness, or a usable PDF-processing application. Future third-party dependencies remain subject to compatibility review and their own required notices.
