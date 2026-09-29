# Capabilities

## Overview

GoreeCloud PDF Manager is currently in the **Lab** lifecycle stage with an exploratory native implementation foundation.

As of September 28, 2026, the verified source capability is intentionally narrow: bounded structural PDF preflight implemented in Rust and exposed through a development-only CLI. The broader PDF Manager application remains unimplemented.

## Core Capabilities

### Bounded PDF input preflight

The `goreecloud-pdf-core` library can:

- enforce a caller-configured maximum input size before structural inspection;
- scan at most the first 1024 bytes for a PDF header marker;
- parse a three-character PDF version token such as `1.7` or `2.0`;
- scan at most the final 2048 bytes for an EOF marker hint;
- return structured observations without retaining the document bytes.

This is not full PDF validation, sanitization, malware scanning, repair, JavaScript inspection, or proof that a document is safe.

### Development CLI

The `pdf-manager-cli` development binary exposes the bounded preflight operation for engineering validation. It is not an end-user application or supported product interface.

## User Capabilities

No end-user PDF reading, editing, conversion, scanning, OCR, annotation, form, signing, redaction, storage, sharing, or workflow capability is currently verified.

## Administrative Capabilities

No application administration surface is currently verified.

## Platform Integrations

### Glaze UI

Planned; no user-facing runtime exists and no integration is implemented or validated.

### Wardveil Security

Planned; the local bounded preflight does not constitute Wardveil integration, malware scanning, sanitization, or a sandbox.

### Privacy Shield

Planned; not implemented or validated.

### Everkeep

No implementation evidence is present.

### GoreeCloud Mesh

No implementation evidence is present.

### GoreeCloud Identity

Planned; not implemented or validated.

### GoreeCloud Policy

No implementation evidence is present.

### GoreeCloud Observability

No implementation evidence is present.

### GoreeCloud Manager

No implementation evidence is present.

## Data and Interoperability

No persistent document storage, conversion engine, API protocol, or product interoperability implementation is currently verified.

## Supported Platforms and Interfaces

The Rust workspace is source-validated by GitHub Actions on an Ubuntu runner. That validation does not establish a supported product platform.

No supported web interface, desktop client, REST API, container image, server deployment, or end-user CLI currently exists.

## Security and Privacy Capabilities

The bounded preflight establishes a small input-gating primitive with size limits and bounded header/tail reads. It does not establish application security hardening, sandboxing, malware detection, privacy-policy enforcement, or production acceptance.

## Resilience, Backup, and Recovery Capabilities

No application persistence, backup, restore, recovery, or resilience implementation is currently verified.

## Accessibility Capabilities

No user interface exists to validate accessibility behavior.

## Automation and API Capabilities

No workflow engine, REST API, MCP server, asynchronous processing system, or automation runtime is currently verified.

## Current Limitations

- No full PDF parser, editor, or renderer has been selected or integrated.
- No representative PDF fixture corpus, malformed-document corpus, or adversarial corpus is yet committed.
- No user-facing application runtime exists.
- No supported product platform or deployment artifact exists.
- No Integral Platform System runtime integration is accepted.
- No release or production acceptance evidence exists.

## Capability Validation

The native foundation is validated by repository source review and the Rust Foundation CI workflow, which runs formatting, workspace build, unit tests, and clippy with warnings denied.

Planned product functionality is documented separately in [PLANNED-FEATURES.md](PLANNED-FEATURES.md) and [PROJECT-SPECIFICATIONS.md](PROJECT-SPECIFICATIONS.md).
