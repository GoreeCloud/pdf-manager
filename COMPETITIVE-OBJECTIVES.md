# Competitive Objectives

## Status

This file defines benchmark objectives for a planned product. It does not claim that GoreeCloud PDF Manager currently matches or exceeds any benchmark.

Research snapshot: September 28, 2026.

## Primary benchmark: Stirling PDF

Stirling PDF is the closest broad benchmark because its current documentation describes a self-hosted PDF platform with editing, signing, redaction, conversion, OCR, a stateful multi-tool workspace, REST APIs, MCP integration, automation, and high-volume processing.

GoreeCloud objectives:

- Match the breadth expected from a modern self-hosted PDF toolbox.
- Match or exceed a one-upload multi-tool workspace with undo/redo.
- Provide a coherent REST API and governed MCP surface.
- Support local/self-hosted processing as a first-class operating model.
- Provide high-volume workflow processing without turning the interactive product into a separate incompatible system.
- Preserve clear boundaries when a capability is experimental or dependent on optional external components.

Source:
- https://docs.stirlingpdf.com/
- https://docs.stirlingpdf.com/functionality/

## Professional PDF benchmark: Adobe Acrobat

Adobe Acrobat is a benchmark for mature end-user PDF workflows including editing, conversion, organization, forms, e-signatures, collaboration, redaction, scan/OCR workflows, and document protection.

GoreeCloud objectives:

- Provide professional-quality editing and organization workflows.
- Support forms, review, signatures, redaction, and security without fragmenting them across unrelated products.
- Make advanced operations discoverable without requiring cloud-first document handling.
- Keep AI-assisted workflows optional, permission-scoped, and transparent rather than making them a prerequisite for core PDF functions.

Source:
- https://www.adobe.com/acrobat/features.html

## Desktop utility benchmark: PDF24 Tools

PDF24 is a benchmark for practical tool breadth and quick access to common PDF operations such as merge, split, compress, edit, OCR, redact, compare, repair, convert, page organization, forms, overlays, and page numbering.

GoreeCloud objectives:

- Keep routine PDF operations fast to discover and execute.
- Cover both common and advanced page/document operations.
- Preserve a coherent tool taxonomy and global search.
- Avoid making breadth come at the expense of accessibility, consistency, or maintainability.

Source:
- https://tools.pdf24.org/en/all-tools

## Professional alternative benchmark: Foxit PDF Editor

Foxit is a benchmark for professional editing, conversion, OCR, forms, comparison, signing, document management, and cross-platform workflows.

GoreeCloud objectives:

- Provide strong editing, OCR, forms, comparison, and signing workflows.
- Build equivalent administrative depth where GoreeCloud use cases justify it.
- Preserve interoperable PDF behavior rather than locking workflows to proprietary document services.

Source:
- https://www.foxit.com/pdf-editor/

## Document-management benchmark: Paperless-ngx

Paperless-ngx is a benchmark for self-hosted document ingestion, OCR, searchable archives, metadata organization, local storage, and workflow-driven document classification.

GoreeCloud objectives:

- Provide strong searchable document-library behavior in addition to one-off PDF tools.
- Support OCR-aware ingestion and local document ownership.
- Support rules/workflows for classification, routing, permissions, and retention.
- Preserve originals and archival-quality derivatives where the workflow requires them.

Source:
- https://docs.paperless-ngx.com/

## Signing benchmark: Documenso

Documenso is a benchmark for open-source, self-hosted document signing, recipient workflows, API/webhook integration, certificates, and deployable signing infrastructure.

GoreeCloud objectives:

- Support self-hosted signing workflows with clear certificate requirements.
- Support standards-based cryptographic signatures and validation.
- Keep signing infrastructure independently operable.
- Integrate signing into the broader PDF workflow without weakening certificate or audit boundaries.

Source:
- https://docs.documenso.com/docs
- https://docs.documenso.com/docs/self-hosting

## Lightweight online-tool benchmark: iLovePDF

iLovePDF is a benchmark for simple, approachable access to common merge, split, compress, convert, organize, edit, and security tasks.

GoreeCloud objectives:

- Make routine operations understandable to non-specialist users.
- Provide fast task entry points and sensible defaults.
- Preserve advanced controls without forcing them into every simple workflow.

Source:
- https://www.ilovepdf.com/

## Capabilities GoreeCloud intends to exceed

Where implementation evidence eventually supports it, GoreeCloud PDF Manager should aim to exceed common alternatives in:

- Privacy transparency.
- Self-hosted and local-first processing.
- Administrator control over external services.
- Integration across interactive, API, workflow, and GoreeCloud application use.
- Data portability and recoverability.
- Explicit capability-state documentation.
- Security-policy integration and auditability.
- Air-gapped and LAN-only operation where dependencies permit.
- Cross-application reuse as a GoreeCloud document-processing foundation.

These are objectives, not current superiority claims.

## Approaches intentionally rejected

The project should not adopt the following as core product requirements:

- Mandatory third-party cloud upload for core PDF operations.
- Silent remote processing.
- Advertising or sponsorship-driven workflow design.
- A required proprietary control plane for core self-hosted operation.
- Vendor-locked document storage without practical export.
- Visual-only redaction presented as permanent redaction.
- Undisclosed AI processing of document content.
- Feature claims that exceed implementation evidence.
- Copying proprietary source code, protected assets, trade dress, or product-specific branding.

## Review rule

Competitive objectives should be revisited when:

- Major PDF platforms materially change their capabilities.
- A benchmark introduces a relevant privacy, security, automation, accessibility, or document-processing pattern.
- GoreeCloud implements a major capability family.
- A planned objective becomes obsolete or conflicts with GoreeCloud architecture or governance.
