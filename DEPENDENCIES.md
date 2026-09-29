# Dependencies

## Current runtime dependency state

The initial GoreeCloud PDF Manager implementation foundation intentionally uses only the Rust standard library.

No third-party PDF parser, renderer, editor, OCR engine, office-conversion engine, database, queue, cache, web framework, desktop framework, or AI service is currently a product runtime dependency.

## Build and CI dependencies

| Dependency | Role | Current baseline | Product runtime dependency |
|---|---|---|---|
| Rust toolchain | Compile, test, lint, and format native source | 1.85.1 | No |
| GitHub Actions hosted runner | Pull-request and main-branch source validation | ubuntu-latest | No |
| actions/checkout | CI source checkout | v7 | No |

## Dependency-selection rules

Future material dependencies must be evaluated before adoption for:

- role and necessity;
- license compatibility with AGPL-3.0-or-later;
- security and maintenance posture;
- malformed and untrusted input behavior;
- network and external-service requirements;
- self-hosting and offline operation;
- portability and platform compatibility;
- persistent data responsibility;
- recovery and replacement;
- version pinning and upgrade testing.

## PDF engine status

No full PDF engine has been selected.

The first goreecloud-pdf-core slice performs only bounded structural preflight using the Rust standard library. It is not a substitute for a standards-compliant PDF parser and must not be represented as full validation or sanitization.

## Review trigger

Update this file whenever a material dependency is added, removed, replaced, version-pinned, or changes operational responsibility.
