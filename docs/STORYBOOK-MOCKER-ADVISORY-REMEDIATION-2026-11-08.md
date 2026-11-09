# Storybook 9 mocker dependency advisory: scoped compatibility evidence

**Classification:** Development-only third-party dependency experiment, not production authorization or redistribution-rights clearance. **Date:** November 8, 2026 (America/Chicago).

The public MIT-core snapshot imported `storybook 9.1.21` which directly requested an exact `@vitest/mocker 3.2.4`, reported by two GitHub Dependabot advisories: [GHSA-qxg6-89mg-rqv8](https://github.com/advisories/GHSA-qxg6-89mg-rqv8) (first patched `4.1.12`) and [GHSA-82fw-gwwq-j7x9](https://github.com/advisories/GHSA-82fw-gwwq-j7x9) (first patched `4.1.11`). The already installed Vitest 4.1.12 dev/test paths did **not** remove Storybook's separate vulnerable copy.

## Compatibility experiment and scope

A **Storybook-scoped** npm override replaces just the Storybook dependency edge with `@vitest/mocker 4.1.12`. It preserves Storybook 9 and `@storybook/react-vite` 9 while leaving Vitest 4.1.12 at its previous locked version. The actual mocker 4.1.12 package identifies an MIT license and depends on `@vitest/spy 4.1.12`, which resolves separately from the original 3.2.4 copy.

**This is a deliberate major-version override of an exact upstream dependency, not a version supported by Storybook's declared dependency range.** It must be replaced by an upstream-coherent Storybook dependency update when the project becomes compatible. Third-party license and NOTICE compliance remain open.

The candidate was validated in an isolated disposable Node environment with no dependency lifecycle scripts:

- `npm install --package-lock-only --ignore-scripts`, then `npm ci --ignore-scripts`;
- `tsc --noEmit --project tsconfig.core.vite.json`;
- Actual **MIT-core-only Storybook 9 Vite/docgen preview** from `.storybook-core/main.ts`, using a preexisting core-only Tokens story;
- The actual `@vitest/mocker` path **resolved by Storybook**, not an unrelated nested copy, asserts version `4.1.12`, the main/browser and redirect exports, a valid synthetic local redirect mock, and that a missing mock is not resolved;
- Existing docgen wildcard integration and selected frontend tests.

The default upstream full Storybook configuration still imports intentionally excluded commercial files. This check **does not assert full upstream Storybook support**, arbitrary malicious mock handling, web-exposed Vitest service safety, or complete package/runtime equivalence. The protected Node 24 workflow must run the same direct mocker compatibility check, frontend tests and core-only Storybook build; the entire PR must pass before merge.

## Remaining security/release blockers

GitHub's actual Dependabot alert states #9 and #24 must be **read back independently after merge**; no manual dismissal. The independent native `glib` and `rand` alerts remain separate. Complete upstream source and binary license review, the 389 asset candidate rights, 250 embedded Java library rights, GoreeShield/Wardveil/Identity, source provenance, adversarial PDF testing, Tauri installed cross-platform testing and release approval remain required. No binary, installer, Storybook site or user document is published or deployed by this override.
