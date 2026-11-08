# GoreeCloud PDF Manager

**Status: source-import development preview; not released, deployed, or production-verified.**

GoreeCloud PDF Manager is a GoreeCloud-branded, self-hostable PDF-management project built from the **MIT-licensed open-core portions** of [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF). It is an independently maintained derivative and is not affiliated with, sponsored by, or endorsed by Stirling PDF Inc.

## Source and license

- Upstream repository: [Stirling-Tools/Stirling-PDF](https://github.com/Stirling-Tools/Stirling-PDF)
- Imported branch: `main`; imported revision: `046f1a0e7163fae43ad9b687fdd1c697f05dda8d` (November 7, 2026).
- License: **MIT** for imported redistributable portions. See [LICENSE](LICENSE) and [UPSTREAM.md](UPSTREAM.md).
- The source-available/commercial portions of the upstream repository **have not been copied into this public repository**. Features depending on those modules are not claimed here.
- This is a **sanitized source snapshot with a fresh Git history**, not a complete fork of all upstream history. Internal package names and some UI assets have not yet been comprehensively rebranded.

## Development architecture

The imported server currently uses Java, Spring Boot and Gradle (`app/core`, `app/common`), and the editor frontend uses TypeScript/Vite (`frontend`). The Gradle and Vite configurations reject non-core modes; the shared build also removes an inherited task dependency on the absent proprietary module. Building requires the correct upstream toolchains and further compatibility work. Desktop packaging, upstream updater endpoints and inherited update-test scripts are disabled until independently validated. HTTPS backend proxying now verifies certificates.

**Do not deploy this source for sensitive PDF processing yet.** Complete dependency review, integration testing, feature entitlement auditing, security/privacy review, GoreeCloud UI migration and platform-specific acceptance first.

## Security defaults for development

The imported application now denies cross-origin browser access unless a specific HTTP(S) origin is configured. Default analytics, feedback, Scarf tracking, update prompts, self-signed server signing and desktop-install promotion are disabled. No automatic Tauri update publication is configured. This is a source-level default, **not proof of complete privacy or security assurance**.

## Next steps

1. Resolve missing commercial-module imports and make the complete MIT-only backend and frontend reproducibly buildable.
2. Replace remaining upstream branding and upstream update/signing references with GoreeCloud-approved assets and settings, without erasing required attribution.
3. Verify core PDF functions, file isolation, PDF-content sanitization, OCR/conversion sandboxing, access controls, and data retention policy.
4. Add pinned, least-privilege build/test workflows after inspecting their dependencies.
5. Integrate GoreeCloud UI and GoreeCloud Mesh while applying GoreeShield privacy policy and Wardveil cybersecurity controls.

See [UPSTREAM.md](UPSTREAM.md) for provenance and exclusions.
