# Features

## Current Features

No end-user GoreeCloud PDF Manager product feature is currently verified as complete.

The repository does contain an exploratory native development foundation: bounded PDF preflight implemented in Rust and exposed through a development-only CLI. See [CAPABILITIES.md](CAPABILITIES.md) and [IMPLEMENTED-FEATURES.md](IMPLEMENTED-FEATURES.md).

## Experimental or Partial Features

### Bounded PDF preflight foundation

The current exploratory implementation can size-gate an input, identify a PDF header within a bounded prefix, parse its version token, and report an EOF-marker hint from a bounded tail scan.

It must not be represented as full validation, sanitization, security scanning, repair, or a user-facing document inspection feature.

## Planned Features

The planned product scope is organized into these capability families:

### Create, edit, and organize

- PDF text and image editing.
- Page merge, split, extraction, deletion, duplication, reordering, rotation, crop, resize, and layout operations.
- Watermarks, stamps, headers, footers, and page numbering.
- Metadata editing, inspection, repair, and document comparison.

### Read, review, and collaborate

- Integrated PDF reading.
- Search, navigation, attachments, and printing.
- Standard PDF annotations and threaded review.
- PDF forms.
- Sharing, permissions, and collaborative review.

### Scan, OCR, and convert

- OCR and scan preprocessing.
- Camera-assisted and network scanning.
- Broad document-to-PDF conversion.
- Broad PDF export/conversion.
- Compression and optimization.

### Protect and sign

- Passwords and PDF permissions.
- Sanitization and unsafe-content inspection.
- Permanent redaction.
- Handwritten, typed, image, and certificate-based signing.
- Signature validation and trusted timestamps.

### Store and automate

- Persistent personal and shared document libraries.
- Search across content and metadata.
- Reusable workflows and batch processing.
- Watched folders, schedules, conditions, events, and webhooks.
- High-volume GoreeCloud PDF Processor queues and routing.

### Integrate and extend

- Local and network storage providers.
- S3-compatible storage and transfer protocols.
- REST API.
- MCP integration.
- Optional AI-assisted document workflows.
- GoreeCloud platform and application integrations.

### Operate at scale

- Centralized administration.
- Accounts, SSO, roles, teams, limits, and audit controls.
- Self-hosted, containerized, desktop, headless, LAN-only, and air-gapped-capable deployments where dependencies permit.
- Multi-node workers, shared storage, shared databases, load balancing, policy management, monitoring, and bulk processing.

The authoritative detailed planned inventory is [PLANNED-FEATURES.md](PLANNED-FEATURES.md). Normative requirements are in [PROJECT-SPECIFICATIONS.md](PROJECT-SPECIFICATIONS.md).

## Deprecated or Removed Features

None.

## Feature-state rule

A capability must not move into Current Features merely because it is designed, documented, prototyped, present on an unmerged branch, or referenced by a benchmark.

Feature promotion requires implementation evidence appropriate to the claimed state.
