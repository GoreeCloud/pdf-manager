# Upstream provenance and source boundaries

**Project:** GoreeCloud PDF Manager

**Original project:** [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF) by its contributors and Stirling PDF Inc.

**Snapshot:** `Stirling-Tools/Stirling-PDF` `main` at `046f1a0e7163fae43ad9b687fdd1c697f05dda8d` (retrieved 2026-11-07).

**Licensing:** Original [LICENSE](LICENSE) is retained without modifying the upstream copyright statement. The root license grants MIT rights to portions outside the explicitly excluded commercial/source-available directories. The public GoreeCloud import intentionally omits those excluded directories; it does not relicense them.

Excluded paths:

- `app/proprietary/`
- `app/saas/`
- `engine/`
- `frontend/src/editor/proprietary/`
- `frontend/src/editor/desktop/`
- `frontend/src/editor/saas/`
- `frontend/src/editor/cloud/`
- `frontend/src/processor/`

Additionally omitted from this baseline: upstream CI/workflows, agent instructions, development-container and editor-private setup files, proprietary-mode environment presets, environment values containing third-party public API identifiers, and bundled private-key test fixtures. Test fixtures must be regenerated before relevant tests. Upstream branding and commercial-only capabilities are not GoreeCloud-created features.

**History:** This sanitized snapshot is a new root commit. Importing upstream history would include restricted blobs from earlier revisions and is intentionally not done. Preserve the upstream URL and revision for auditability and future core-only updates.

**Unverified:** End-to-end core functionality, package-level license metadata consistency, third-party assets, complete GoreeCloud UI rebrand, security, privacy, builds, desktop distribution and releases remain subject to separate review.
