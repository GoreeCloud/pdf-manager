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

The imported server currently uses Java, Spring Boot and Gradle (`app/core`, `app/common`), and the editor frontend uses TypeScript/Vite (`frontend`). The Gradle and Vite configurations reject non-core modes; the shared build also removes an inherited task dependency on the absent proprietary module. Building requires the correct upstream toolchains and further compatibility work. Desktop packaging, upstream updater endpoints, inherited update-test scripts and in-app remote update lookups/download URLs are disabled until independently validated. HTTPS backend proxying now verifies certificates.

## Core-only developer preview

The current source build uses **JDK 25**, **Gradle 9.7.1** and **Node.js 24**. No Gradle wrapper JAR is bundled in this snapshot; use an independently installed Gradle 9.7.1 CLI. Do not use upstream proprietary or SaaS modes, inherited engine scripts, or desktop installers.

For a locally isolated development machine (not a public server):

```bash
cd frontend
npm ci --ignore-scripts --no-audit --no-fund
cd ..
./scripts/dev-core.sh verify
./scripts/dev-core.sh both
```

The helper binds the API and frontend to **127.0.0.1** only; it does not install software, supply credentials, enable public hosting or bypass release validation. The API and frontend may also be launched separately with `backend` and `frontend`. If the local Java/Gradle toolchain is unavailable, use the read-only [GitHub core-build CI workflow](.github/workflows/core-build.yml) to verify compilation.

For development-only PDF sample generation and Open Graph previews, the imported Puppeteer scripts use Chrome's normal browser sandbox. They do not disable Chromium isolation or automatically download a browser during the locked `npm ci --ignore-scripts` setup. These helper scripts have syntax checks in CI; actual browser execution and handling of untrusted HTML are not validated.

**Do not deploy this source for sensitive PDF processing yet.** Complete dependency review, integration testing, feature entitlement auditing, security/privacy review, GoreeCloud UI migration and platform-specific acceptance first.

## Reproducible dependency metadata (not a release SBOM)

A Python-standard-library-only [lockfile inventory tool](scripts/locked_dependency_inventory.py) now records package names, exact locked versions, recorded checksums, source lockfile hashes and *unverified* npm license hints across five npm and Cargo lockfiles. Run its [six regression tests](scripts/tests/test_locked_dependency_inventory.py) or retrieve the seven-day output of [Lockfile dependency metadata CI](.github/workflows/lockfile-metadata.yml).

The output is **metadata only**. It omits the resolved Gradle/Java graph, OS/native packages, third-party assets and verified licensing. It cannot be represented as a complete SBOM or used as security/release approval. [Scope, usage and exclusions](docs/LOCKFILE-INVENTORY.md).

## Security defaults for development

The imported application now denies cross-origin browser access unless a specific HTTP(S) origin is configured. Default analytics, feedback, Scarf tracking, update prompts, self-signed server signing and desktop-install promotion are disabled. The unused upstream Tauri updater plugin, bundled update-signing configuration, and its vulnerable transitive `zip` dependency have been removed; the existing desktop command names now return explicit disabled responses. The Rust manifest and lockfile are checked without running build scripts, **but desktop compilation and packaging remain unverified**. This is a source-level default, **not proof of complete privacy or security assurance**.

The in-app update service currently returns no remote release metadata or installer URLs, even if a legacy update screen is reached. **No GoreeCloud production update channel has been configured.** Some inherited installation/help surfaces may still link to upstream Stirling software and must be replaced before a public release.

## Legal-policy and support-link authority

This derivative does **not** adopt Stirling PDF's Terms of Service, Privacy Policy, or official support community. Missing policy URLs remain unconfigured in the backend, API documentation, footer and settings. Policy links are shown only when explicitly configured as HTTPS URLs or safe same-origin paths; only basic URL syntax is validated, **not** the legal content or ownership. The footer directs issue reports to [GoreeCloud PDF Manager's own tracker](https://github.com/GoreeCloud/pdf-manager/issues). Before any public release the operator must establish and independently review applicable GoreeCloud terms, privacy and accessibility documents.

## Next steps

1. Resolve missing commercial-module imports and make the complete MIT-only backend and frontend reproducibly buildable.
2. Replace remaining upstream branding and upstream update/signing references with GoreeCloud-approved assets and settings, without erasing required attribution.
3. Verify core PDF functions, file isolation, PDF-content sanitization, OCR/conversion sandboxing, access controls, and data retention policy.
4. Add pinned, least-privilege build/test workflows after inspecting their dependencies.
5. Integrate GoreeCloud UI and GoreeCloud Mesh while applying GoreeShield privacy policy and Wardveil cybersecurity controls.

See [UPSTREAM.md](UPSTREAM.md) for provenance and exclusions.
