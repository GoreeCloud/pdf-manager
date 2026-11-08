# Dependency security — GoreeCloud PDF Manager

**Status:** Development preview, not production-ready. This file records specific audit boundaries; it is not a security certificate.

## Scope and evidence

- Original imported source: Stirling-Tools/Stirling-PDF `main` at `046f1a0e7163fae43ad9b687fdd1c697f05dda8d`; proprietary/source-available directories were omitted, as documented in [UPSTREAM.md](../UPSTREAM.md).
- On November 8, 2026, after enabling GitHub Dependabot alerts, its initial index identified **33** alerts across `frontend/package-lock.json`, `devTools/package-lock.json` and the unbuilt desktop `frontend/src-tauri/Cargo.lock` (5 critical, 10 high, 13 medium, 5 low). An earlier zero-alert view was superseded by this completed indexing.
- The scoped `npm audit fix --package-lock-only --ignore-scripts --no-fund` pass used compatible semver updates and **did not execute package install scripts**. It updated the frontend lockfile, including Vite 7.3.7, Storybook 9.1.21 and React Router 7.18.5.
- The `devTools` lockfile was separately updated, and `npm audit` reported no remaining advisories for its 121 packages.
- A post-update `npm audit --omit=dev --json` check reported **zero known frontend runtime dependency advisories** on the revised lockfile. This is an npm advisory snapshot, not an audit of source security, packages not in the npm lockfile, runtime behavior, or all OSS licenses.
- An *all-scopes* frontend audit still reported 30 advisories (3 critical, 10 high and 17 medium), primarily involving development/testing dependencies such as Vitest, tinypool, extract-zip and related tooling. The remaining findings cannot be assumed safe solely because they are development-scoped. Many require coordinated major-version upgrades or have no compatible direct fix.
- The Rust/Tauri lockfile still needs a separate supported `cargo update` and desktop security audit. The desktop packaging/updater are disabled in this import; this mitigation does not make the vulnerable packages acceptable for a desktop release.

## Gates

1. Keep read-only import checks, core Java/PDF regression tests, Node frontend typechecking and build checks passing on every relevant change.
2. Run `npm audit --omit=dev --audit-level=low` for frontend runtime and `npm audit --audit-level=low` for development tools. A new known runtime advisory fails the CI gate until resolved or explicitly reviewed.
3. Review the [open Dependabot alerts](https://github.com/GoreeCloud/pdf-manager/security/dependabot) and automated update PRs individually. Do **not** run forceful major upgrades or auto-merge without testing compatibility.
4. Resolve remaining development-only and Rust/Tauri critical/high advisories, audit transient dependencies and license compatibility, and validate real PDF processing/security before any deployment.
5. Keep user PDF documents and credentials out of CI and public issues; use only synthetic fixtures.

GitHub is authoritative for live alert counts and dependency state. See [release gate #1](https://github.com/GoreeCloud/pdf-manager/issues/1) for open obligations.
