# User Manual

## Current availability

GoreeCloud PDF Manager is in the **Lab** lifecycle stage.

There is currently no usable end-user PDF Manager application, installable release, hosted service, REST API, MCP service, or production deployment.

A **development-only command-line tool** now exists for exercising bounded PDF preflight. It is an engineering surface, not a supported user product. The preflight operation checks an input-size limit, looks for a PDF header in a bounded prefix, parses the version token, and reports whether an EOF marker is visible in a bounded tail scan. It does not validate, sanitize, repair, render, edit, or prove the safety of the document.

This manual therefore continues to document the user-availability boundary and intended product workflow rather than presenting planned functionality as available.

## Intended product model

PDF Manager is planned as a self-hosted, privacy-focused workspace for PDF and document operations.

The planned interaction model centers on:

1. Open, upload, scan, or select a document.
2. Review the document in an integrated reader.
3. Choose one or more document operations.
4. Preview material or destructive changes where appropriate.
5. Apply changes locally or through the configured GoreeCloud-controlled processing environment.
6. Export, save, share, or store the resulting document.

## Planned workflow areas

### Read and navigate

Planned reader functionality includes page navigation, thumbnails, zoom, search, direct page jumps, text selection, bookmarks, attachments, printing, and reading mode.

### Edit and organize

Planned tools include text/image editing, page merge/split/reorder/rotate/crop/resize, page insertion, blank-page handling, booklet and N-up layouts, overlays, bookmarks, and document outlines.

### Review and forms

Planned workflows include annotations, comments, review threads, form filling, form-field creation/editing, and form flattening.

### Scan and OCR

Planned scanning workflows include image-to-PDF capture, OCR, multilingual text extraction, scan preprocessing, QR-assisted phone capture, and large scanning-job separation.

### Convert and optimize

Planned conversion covers common office, text, image, web, structured-data, e-book, archival, and print formats where selected open-source conversion engines can provide reliable behavior.

Planned optimization includes configurable image/resource compression and delivery/archival profiles.

### Protect, redact, and sign

Planned security workflows include passwords, permissions, sanitization, unsafe-content inspection, permanent redaction, and certificate-based digital signatures.

Redaction must remove sensitive content from the resulting document rather than merely cover it visually.

### Store, share, and automate

Planned document-library capabilities include personal/shared storage, folders, search, history, sharing, permissions, retention, and collaboration.

Planned automation includes reusable workflows, batch processing, watched folders, conditions, schedules, events, webhooks, REST APIs, and governed MCP integration.

## Privacy expectations

The intended default is local or self-hosted processing where technically possible.

Future versions must clearly identify when an optional external service would receive document content. Remote or AI-assisted processing must not occur silently.

## Security expectations

Document inputs must be treated as untrusted. The current development preflight is only an initial bounded input gate and does not replace parser isolation, malware inspection, sanitization, or other planned security controls.

Future releases must make high-risk operations such as password removal, destructive redaction, sanitization, permission changes, and signature removal explicit.

## Account and deployment expectations

No account, deployment, storage, SSO, or server workflow is currently implemented.

The planned product supports local/self-hosted use and optional GoreeCloud Identity, storage, administration, and collaboration integrations.

## Support status

No supported software release currently exists.

For product scope, see [SPECIFICATIONS.md](SPECIFICATIONS.md). For current verified capability state, see [CAPABILITIES.md](CAPABILITIES.md). For planned work, see [PLANNED-FEATURES.md](PLANNED-FEATURES.md).
