# Architecture

## Current lifecycle

GoreeCloud PDF Manager is in the **Seed** lifecycle stage while the first native implementation foundation is being established.

This document describes the current source architecture and near-term boundaries. It does not claim the planned PDF Manager product is complete, released, deployed, or production-accepted.

## Native implementation direction

The implementation is original GoreeCloud-owned software.

The initial codebase uses a Rust workspace aligned with other native GoreeCloud document tooling:

- Rust edition: 2024.
- Minimum pinned toolchain for the current baseline: Rust 1.85.1.
- Unsafe Rust: forbidden by workspace policy.
- External runtime crates in the first slice: none.
- Project license: AGPL-3.0-or-later.

The absence of an external PDF engine in the first slice is deliberate. Engine selection remains a separate architecture and dependency decision that must account for licensing, malformed-document behavior, standards coverage, process isolation, portability, and replaceability.

## Workspace

Current source layout:

- apps/pdf-manager-cli — development-only CLI for exercising bounded core operations.
- crates/pdf-core — reusable PDF-domain and security-preflight primitives.

Future web, desktop, worker, API, storage, and integration components should consume reusable core operations rather than duplicate document logic.

## First implementation slice: bounded PDF preflight

The first source capability performs a small, dependency-free inspection before any future full PDF parser is invoked.

It currently:

- checks a configured maximum input size before parsing;
- scans at most the first 1024 bytes for a PDF header;
- parses the three-character PDF version token;
- scans at most the final 2048 bytes for an EOF marker hint;
- exposes the operation through a reusable Rust library;
- exposes a development CLI for manual invocation.

This is intentionally **not** full PDF validation, document repair, malware scanning, sanitization, password or permission handling, JavaScript inspection, proof that a file is safe, or an end-user PDF Manager application.

The bounded preflight exists to establish safe input-gating patterns before a larger parser or engine dependency is selected.

## Security boundary

PDF and document inputs are untrusted.

Future parser and conversion integrations must remain behind explicit adapters so they can be isolated, resource-bounded, replaced, and tested independently. Expensive or high-risk operations should move to worker or process boundaries appropriate to their failure and attack surface.

No current source code establishes sandboxing, malware detection, sanitization, or production security acceptance.

## Dependency policy

The initial runtime foundation has no third-party Rust crate dependency.

Future dependencies must be narrowly scoped foundations rather than complete third-party product shells. Each material dependency must be evaluated for license compatibility, maintenance and security posture, standards coverage, malformed-input behavior, self-hosting and offline implications, replacement strategy, and recovery requirements.

## Platform systems

All nine Integral Platform Systems remain applicable for evaluation. The current first slice does not establish runtime conformance with any of them.

Glaze UI remains required when the first user-facing runtime surface is implemented.

## Next architecture gates

Before the product advances beyond exploratory implementation, the project must define and validate:

- the full PDF parser, editor, and rendering engine boundary;
- process isolation and resource enforcement;
- OCR and office-conversion foundations;
- persistent document, job, and temporary-file models;
- REST and asynchronous job contracts;
- web and desktop client boundaries;
- representative malformed and adversarial fixtures;
- applicable Platform System adapters and evidence;
- deployment, backup and restore, privacy, and observability behavior.
