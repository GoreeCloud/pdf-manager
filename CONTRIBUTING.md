# Contributing

## Scope

GoreeCloud PDF Manager is native GoreeCloud software. Changes must preserve the project specifications, security and privacy boundaries, evidence-backed lifecycle state, and the distinction between implemented and planned capabilities.

## Toolchain

Current Rust baseline:

- Rust 1.85.1.
- Edition 2024.
- rustfmt.
- clippy.

## Local validation

From the repository root, run:

1. cargo fmt --all --check
2. cargo build --workspace --all-targets
3. cargo test --workspace --all-targets
4. cargo clippy --workspace --all-targets -- -D warnings

## Change workflow

Material work should use a short-lived purpose branch and pull request.

Before merge:

- refresh against the authoritative target branch;
- validate the exact candidate head;
- run applicable required checks;
- resolve blocking review comments;
- preserve a rollback or recovery path proportional to the change;
- update repository documentation when capability or lifecycle facts change.

## Security

Treat all document inputs as untrusted.

Do not add unrestricted parser, converter, shell, filesystem, network, or process-execution behavior without an explicit security boundary and tests appropriate to the risk.

Do not commit private documents, credentials, certificates containing private keys, or reusable secrets.

## Dependencies

Do not add a dependency merely for convenience.

A material dependency must have a clear role, compatible license, bounded responsibility, maintenance rationale, and replacement or recovery story. Complete third-party PDF applications are not acceptable as the GoreeCloud application foundation.

## Documentation truthfulness

Do not mark a planned feature as implemented unless source and validation evidence support the claimed state.

A passing source-level CI run does not establish production readiness, deployment acceptance, or Anchor lifecycle qualification.
