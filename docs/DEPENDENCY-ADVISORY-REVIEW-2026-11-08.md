# PDF Manager — dependency advisory remediation review

**Date:** November 8, 2026

**Scope:** Public, attributed MIT-core development snapshot at `da814d3` and its five open GitHub Dependabot alerts. This is a source/lockfile review, **not** a complete license, supply-chain, exploitation, runtime, or release assessment. The service has not been deployed.

## Verified advisory inventory

| GitHub alert | Reported package and locked version | Advisory and observed dependency route | Decision |
| --- | --- | --- | --- |
| #29, moderate | `minimatch 9.0.9`, `frontend/package-lock.json` | [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249); `@joshwooding/vite-plugin-react-docgen-typescript 0.6.1` → `glob 10.5.0` → `minimatch 9.0.9`. GitHub lists first patched minimatch `11.0.1`. | **Open; unsafe forced patch rejected.** |
| #24 and #9, moderate | `@vitest/mocker 3.2.4`, `frontend/package-lock.json` | [GHSA-qxg6-89mg-rqv8](https://github.com/advisories/GHSA-qxg6-89mg-rqv8) and [GHSA-82fw-gwwq-j7x9](https://github.com/advisories/GHSA-82fw-gwwq-j7x9). `storybook 9.1.21` requests `@vitest/mocker 3.2.4` directly; the already installed `vitest` and `@vitest/browser` use patched `4.1.12` in their own nested dependency paths. | **Open; Storybook compatibility review required before changing its precise major-version dependency.** |
| #30, moderate | `glib 0.18.5`, `frontend/src-tauri/Cargo.lock` | [GHSA-wrw7-89jp-8q8g](https://github.com/advisories/GHSA-wrw7-89jp-8q8g). Native GTK/GLib 0.18 stack includes `gtk 0.18.2`, `gdk 0.18.2`, `webkit2gtk 2.0.2`, `gio 0.18.4`. GitHub lists patched `glib 0.20.0`. | **Open; do not force ABI/API-incompatible GTK stack upgrade without upstream and cross-platform compatibility testing.** |
| #32, low | `rand 0.7.3`, `frontend/src-tauri/Cargo.lock` | [GHSA-cq8v-f236-94qc](https://github.com/advisories/GHSA-cq8v-f236-94qc); transitive through `phf_generator 0.8.0`. `rand 0.8.6` is *also* present but does not replace the vulnerable 0.7.3 instance. | **Open; replacing the upstream phf_generator dependency chain requires an actual compatible upgrade.** |

## Experiment rejected: forced minimatch 11

A targeted lockfile experiment overrode only `glob 10.5.0`'s `minimatch` dependency to `11.0.1`. `npm install --package-lock-only --ignore-scripts` and `npm ci --ignore-scripts` both succeeded, but the actual `glob 10` wildcard API then returned **zero matches** for `*.json` and `**/*.tsx` despite matching local files being present. Direct `minimatch()` still reported matches; the failure was an **integration contract break**, not a missing npm install. Therefore **no minimatch override or changed package lockfile was accepted into this PR**.

The new [synthetic glob compatibility check](../frontend/scripts/verify-docgen-glob.mjs) uses the glob instance resolved by the actual Storybook docgen plugin; it asserts wildcard matching over disposable local `.json` and `.tsx` fixtures. It failed on the rejected forced upgrade, then passed on the existing locked dependency tree. [Required Node 24 CI](../.github/workflows/core-build.yml) runs it after `npm ci --ignore-scripts` and before the frontend build to prevent silent functional breakage in future security-patch PRs.

The `minimatch 11.0.1` tarball describes itself as BlueOak-1.0.0 licensed and has a changed dependency tree; no separate downstream license acceptance is implied. Existing npm audit checks distinguish runtime and development tooling; they do not certify desktop dependencies, imported assets, or production readiness.

## Subsequent narrow docgen compatibility experiment

A separate [controlled Storybook 9 dependency-tree bridge](STORYBOOK-DOCGEN-ADVISORY-REMEDIATION-2026-11-08.md)
has since passed local clean Node 24 install, real plugin wildcard matching,
TypeScript, frontend core Vite build and a core-only Storybook preview.
Unlike the rejected `glob 10` / `minimatch 11` combination, the tested pair
is `glob 13.0.7` with `minimatch 11.0.1`, scoped only under the original
docgen plugin. It remains an **unsupported major-version override** in the
declaring dependency graph, and protected GitHub CI and the actual Dependabot
alert #29 must be checked before claiming a fix. The historical five-alert
table above describes the original snapshot, not the post-merge alert state.
All other alerts and legal/security release gates remain independently open.

## Next compatible remediation gates

- **JavaScript:** Prefer supported, audited updates of the Storybook/docgen plugin and their upstream glob/mocker dependencies, not a global override to a new major API. In a disposable Node 24 environment run the locked install, new glob integration test, Storybook smoke, frontend typecheck, JavaScript tests, and the core build; read back resolved versions and GitHub alerts after merging.
- **Native:** Resolve desktop GTK/GLib and rand/phf-generator with a coherent dependency-stack upgrade only after reviewing Tauri/WebKit/GTK API compatibility, license evidence, and passing the native Linux compile test. A Linux typecheck does not imply an installed Tauri binary works or that macOS/Windows behave correctly.
- **Security and legal:** Maintain all five open advisories as explicit release-readiness risks until a compatible fix or documented risk decision is independently verified. Do not dismiss alerts or equate a passing development CI run with complete artifact safety, GoreeShield privacy acceptance, Wardveil security approval, or deployment permission.

No dependency was force-upgraded or declared patched solely based on package metadata.
