# Changelogs

## Unreleased — Forge rebuild

### Added

- License-safe maintained-fork baseline from Stirling-PDF core revision `973bff865cc19fbc268859e1fb13103c66c1f5a5`.
- GoreeCloud-owned Glaze workbench.
- Direct merge, split, rotate, optimize/compress, and image-extraction workflows.
- Direct rearrange, metadata, page-numbering, text stamp/watermark, sanitize, add/remove password, repair, and flatten workflows.
- Direct crop, OCR, and PDF/A workflows with backend-contract validation.
- Glaze V1.7 runtime snapshot from `GoreeCloud/glaze@9ab08060d723b022cdf07d001e8c95bca626a764`.
- Canonical PDF Manager icon from GoreeCloud branding authority.
- Repository-native feature, changelog, privacy, security, architecture, upstream, and Glaze records.
- CI and source-boundary enforcement.

### Changed

- Public product identity to GoreeCloud PDF Manager.
- Gradle project identity to `GoreeCloud PDF Manager`, group `com.goreecloud.pdfmanager`, version `0.1.0-dev`.
- Build graph to common/core only.
- Backend-only landing page into the primary GoreeCloud workbench.
- Workbench-ready tool count expanded from 5 to 17 while retaining explicit API-only state for workflows that still need stronger preview/dependency UX.

### Security and privacy

- Restricted upstream directories excluded.
- Same-origin UI asset/request model.
- No optional telemetry or behavioral analytics in the GoreeCloud shell.
- Security/privacy presentation claims tied to evidence rather than iconography.
- Password inputs use password-type controls and are rebuilt when tool dialogs reopen rather than persisted in application state.
