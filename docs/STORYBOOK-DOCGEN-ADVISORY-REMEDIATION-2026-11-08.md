# GoreeCloud PDF Manager — Narrow Storybook docgen advisory remediation

**Review date:** November 8, 2026 (America/Chicago).
**Classification:** Development-only dependency compatibility evidence, not a blanket supply-chain, legal, production, or release approval.

## Source of the risk

In the original Storybook 9 lockfile, `@storybook/react-vite 9.1.21` pins `@joshwooding/vite-plugin-react-docgen-typescript 0.6.1`. That docgen plugin depends on `glob 10.5.0`, which resolved `minimatch 9.0.9`. GitHub's [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249) includes versions `>=7.0.0 <11.0.1`, with a denial-of-service fix first in `11.0.1`.

A previous isolated attempt to **override only minimatch to 11.0.1 inside glob 10** installed cleanly but broke glob wildcard file matching. Therefore it was rejected. Independently overriding the plugin to `0.9.1` while retaining Storybook 9 also removed the vulnerable dependency path, but **the real Storybook preview failed** with `ERR_PACKAGE_PATH_NOT_EXPORTED` because Storybook 9 expected a CommonJS plugin entrypoint. A coherent Storybook 10 trial resolved a clean lockfile but updated hundreds of unrelated packages and failed an existing PDF.js TypeScript typecheck. **Neither rejected alternative was accepted.**

## Narrow, tested compatibility approach

The dependency changes are **scoped only to the actual docgen tree**, keeping Storybook `9.1.21` and the direct docgen plugin `0.6.1` unchanged:

- `@joshwooding/vite-plugin-react-docgen-typescript` overrides its nested `glob` dependency to `13.0.7`.
- `glob@13.0.7` overrides its nested `minimatch` dependency to **`11.0.1`**.

Both majors are outside the originating packages' declared semver ranges; this is a documented temporary compatibility bridge, **not an upstream-supported upgrade**. The actual docgen plugin's resolved dependency paths are asserted in the required regression test to prevent a false positive from a patched `minimatch` installed elsewhere.

The separate `read-package-json` development tooling still has `glob 7.2.3` / `minimatch 3.1.5`; the GHSA range cited above starts at `minimatch 7`. **That does not establish that the older packages have no other vulnerabilities.** The two changed packages identify their license as **BlueOak-1.0.0**, so third-party license texts and overall redistribution compliance need further legal review; no acceptance is inferred from a package metadata field.

## Evidence and acceptance

In an isolated disposable Node 24 checkout with no dependency lifecycle scripts:

1. `npm ci --ignore-scripts --no-audit --no-fund` passed with the lockfile.
2. The real Storybook docgen plugin resolved `glob 13.0.7` → `minimatch 11.0.1`. Existing wildcard tests over generated JSON, TSX and Markdown fixtures passed.
3. `tsc --noEmit --project tsconfig.core.vite.json` passed.
4. `vite build --mode core` passed.
5. An **actual Storybook 9 preview build** using the new limited **MIT-core-only** `frontend/.storybook-core/main.ts` (existing `Tokens.stories.tsx` story) passed.

The upstream full `frontend/.storybook` preview is **not** a supported core-only test: its configuration imports excluded commercial/processor/desktop modules. A full build failed on a missing `@processor/contexts/TierContext` path; this was reproduced separately and is **not** evidence the patched glob chain fails. The core-only Storybook build deliberately does not pretend all upstream stories or integrations are available; it is a bounded executable integration contract for the sanctioned core-only React docgen path.

The [required Node 24 workflow](../.github/workflows/core-build.yml) now requires both actual resolved-version/wildcard checks and the no-publish core-only Storybook preview, in addition to TypeScript, unit tests and the ordinary Vite core build. No generated Storybook artifacts are distributed, and no new CI credentials or privileged permissions are granted.

## Residual gates

- After protected merge, verify the **actual GitHub Dependabot alert** #29 state. Never manually dismiss an alert or claim remediation solely because a lockfile resolves the expected version.
- Alerts #9 and #24 (`@vitest/mocker`) and #30 (`glib`) / #32 (`rand`) remain separate and require compatible remediation with native and Storybook behavioral tests.
- Audit package tarball/source behavior, dependency licenses and retained license notices; review all third-party assets, Java JARs, Rust crates, privacy/security controls and supported installable runtime.
- Replace temporary major-version scoped overrides with a supported upstream versioned dependency update when compatible, keeping the integration smoke mandatory.

No deployment, signed release, protected-branch requirement change, proprietary module import, or license clearance follows from this test.
