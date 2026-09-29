# GoreeCloud PDF Manager — Project Specifications

## 1. Document status

- **Project:** GoreeCloud PDF Manager
- **Repository:** `GoreeCloud/pdf-manager`
- **Project type:** Application and document-processing platform
- **Lifecycle status:** Seed
- **Authority:** This repository is the authoritative project-specification source.
- **Implementation state:** Pre-implementation; no application implementation is verified as of September 28, 2026.
- **Deployment model:** Privacy-focused and self-hosted by default, with optional governed integrations.
- **Primary role:** Standalone PDF application and shared PDF-processing foundation for the GoreeCloud ecosystem.

The requirements below define intended functionality. They are not claims of currently implemented or production-validated behavior.

### Repository specification boundary

[SPECIFICATIONS.md](SPECIFICATIONS.md) is the canonical repository-level technical specification and implementation contract. This file remains the detailed project-scope and normative product-requirements record. Current implementation state is controlled by evidence and the current-state records, including [CAPABILITIES.md](CAPABILITIES.md) and [IMPLEMENTED-FEATURES.md](IMPLEMENTED-FEATURES.md).

### Licensing

GoreeCloud PDF Manager is licensed under the **GNU Affero General Public License v3.0 or later** (`AGPL-3.0-or-later`). See [LICENSE](LICENSE).

The selection follows GoreeCloud's Software Licensing Policy and fits the planned combination of self-hosted network interaction, REST/MCP service surfaces, automation workers, multi-node processing, and standalone application workflows. Material dependencies must be checked for license compatibility and required third-party notices as implementation begins.

## 2. Product purpose

GoreeCloud PDF Manager is intended to provide comprehensive tools for reading, editing, converting, organizing, securing, signing, scanning, automating, storing, and processing PDF documents while preserving GoreeCloud privacy, security, accessibility, and self-hosting requirements.

## 3. Functional requirements

### 3.1 PDF editing

The product must be designed to:

- Edit existing PDF text.
- Add, move, resize, replace, and remove text and images.
- Add shapes, text boxes, stamps, and other page content.
- Edit document metadata.
- Modify colors and adjust brightness, contrast, and saturation where technically supported.
- Remove unwanted images or annotations.
- Inspect and remove embedded JavaScript.
- Sanitize document content.
- Repair damaged or malformed PDF files where recovery is technically possible.

### 3.2 Page management

The product must support:

- Merging multiple PDFs.
- Splitting PDFs by page, page range, chapter, bookmark, file size, page count, or document count.
- Extracting selected pages.
- Removing, duplicating, and reordering pages.
- Drag-and-drop page organization.
- Page rotation, cropping, resizing, scaling, and orientation changes.
- Inserting blank pages.
- Inserting pages from other documents.
- Detecting and removing blank pages.
- Booklet layout generation.
- N-up layouts.
- Combining pages into a continuous long page.
- PDF overlays.
- Bookmark and document-outline management.

### 3.3 PDF reader

The integrated reader must provide:

- Page navigation.
- Thumbnail navigation.
- Zoom controls.
- Single-page and spread views.
- Direct page jumps.
- Full-text search.
- Text selection and copying.
- Bookmark navigation.
- Attachment viewing.
- Printing.
- A dedicated reading mode.

### 3.4 Annotations and review

The product must support standard, interoperable PDF review workflows including:

- Highlight, underline, strike-through, and squiggly text markup.
- Freehand drawing and highlighter tools.
- Lines, rectangles, circles, polygons, sticky notes, text comments, and text boxes.
- Reviewer names and timestamps.
- Comment and annotation sidebars.
- Comment/reply threads.
- Undo and redo.
- Preservation of standard PDF annotations for compatibility with other readers.

### 3.5 PDF forms

The product must support:

- Filling text fields, checkboxes, radio buttons, dropdowns, and other PDF form controls.
- Creating new form fields.
- Editing and removing existing form fields.
- Detecting potential form fields automatically.
- Unlocking read-only forms where technically and legally permitted.
- Preserving editable form data.
- Flattening completed forms into permanent page content.

### 3.6 OCR and scanning

The product must support:

- Converting scanned PDFs into searchable documents.
- Extracting text from scanned pages.
- Multiple OCR languages.
- Detection of pages requiring OCR.
- Skipping pages that already contain searchable text.
- Forced OCR when required.
- Scan preprocessing.
- Detection of scanned photographs.
- Phone-camera scanning through QR-assisted upload.
- Conversion of captured images into PDFs.
- Desktop or network scanning workflows.
- Separator-page handling for large scanning jobs.

### 3.7 Document-to-PDF conversion

The conversion system must support, where the selected conversion engine can do so reliably:

- DOCX, DOC, ODT.
- XLSX, XLS, ODS.
- PPTX, PPT, ODP.
- TXT and RTF.
- JPG, JPEG, PNG, GIF, BMP, TIFF, WebP, and SVG.
- HTML, websites, and URLs.
- Markdown.
- Email files.
- EPUB and other supported e-book formats.
- Comic-book archives.
- JSON and other supported structured data.
- Supported PostScript and vector formats.

### 3.8 PDF export and conversion

The product must support exporting PDF content to supported forms of:

- DOCX and ODT.
- PPTX and ODP.
- XLSX.
- TXT and RTF.
- Markdown.
- PNG, JPEG, GIF, TIFF, BMP, and WebP.
- CSV.
- HTML, XML, and JSON.
- EPUB and supported e-book formats.
- Comic-book archives.
- PDF/A and PDF/X.
- Supported print or vector formats.

### 3.9 Compression and optimization

The product must provide:

- PDF file-size reduction.
- Optimization of embedded images and resources.
- Configurable image resolution and quality.
- Removal of unnecessary document objects.
- Optimization profiles for storage, transfer, email, web delivery, and archival use.
- Configurable compression settings.

### 3.10 Security and permissions

The product must support:

- Password protection.
- Authorized password removal.
- Separate user and owner passwords where supported by the PDF standard.
- Printing, copying, editing, and form permissions.
- Flattening of sensitive content where appropriate.
- Removal of JavaScript, embedded files, external links, fonts, metadata, and other unwanted document elements.
- Detection of potentially unsafe PDF content.
- Document-sanitization workflows.

### 3.11 Redaction

Redaction must be designed to permanently remove sensitive information, not merely cover it visually. The product must support:

- Manual redaction selection.
- Automatic text or pattern discovery.
- Search-and-redact workflows.
- Pattern-based redaction.
- Pre-finalization review.
- Permanent removal of redacted information from the resulting document.

### 3.12 Digital signatures

The product must support:

- Drawn handwritten signatures.
- Typed signatures.
- Uploaded signature images.
- Signature placement on document pages.
- Certificate-based digital signatures.
- X.509, PKCS#12/PFX, and related certificate formats where compatible.
- Validation of existing signatures and certificates.
- Detection of document modification after signing.
- Trusted timestamps.
- QR-assisted phone signing.
- Authorized signature removal when technically appropriate.

### 3.13 Watermarks, stamps, headers, footers, and page numbers

The product must support:

- Text and image watermarks.
- Opacity, rotation, spacing, repetition, and placement controls.
- Custom stamps.
- Page numbers.
- Configurable headers and footers.

### 3.14 Document comparison and inspection

The product must support:

- Comparing two PDF documents.
- Identifying textual differences.
- Inspecting metadata.
- Inspecting attachments and embedded objects.
- Inspecting JavaScript.
- Inspecting page dimensions and document properties.
- Exporting PDF information as structured data.
- Generating filenames from detected document content.

### 3.15 Multi-tool workspace

The user interface must provide a unified workspace that allows a document to be uploaded once and processed through multiple operations. The workspace must support:

- Visual page thumbnails.
- Rotation, removal, duplication, and reordering.
- Insertion of additional documents or blank pages.
- Page-range selection.
- Split-point definition.
- Undo and redo.
- Export of selected pages or the completed document.

### 3.16 Document library

The product must provide persistent document storage with:

- Personal and shared file areas.
- Folders and nested folders.
- File previews.
- Rename, move, and delete operations.
- Search.
- Folder customization where applicable.
- File history.
- Per-user or system storage limits.
- Configurable cleanup and retention policies.

### 3.17 File sharing and collaboration

The product must support:

- Direct sharing with other users.
- Share links.
- Viewer, Commenter, and Editor permission levels.
- Link expiration.
- Link revocation.
- Access-history tracking.
- Collaborative annotation and document-review workflows.

### 3.18 Workflow automation

The product must support reusable document-processing workflows that can:

- Chain multiple PDF operations.
- Be saved, loaded, imported, and exported.
- Run against individual files or batches.
- Process files placed into watched folders.
- Branch conditionally based on text, images, page count, page size, file size, or orientation.
- Run on schedules.
- Process events automatically.
- Be triggered by webhooks.

### 3.19 GoreeCloud PDF Processor

A high-volume processing subsystem must support a source-to-processing-to-destination model with:

- Processing queues.
- Job history.
- Failure review.
- Retry handling.
- Ingestion, security, classification, compliance, and routing policies.
- Batch-processing jobs.
- Continuous processing of incoming documents.

### 3.20 Storage and service integrations

The integration layer must be designed to support:

- Local filesystem storage.
- S3-compatible object storage.
- SFTP.
- FTP/FTPS.
- SMB/network shares.
- Nextcloud-compatible storage.
- Webhooks.
- Custom HTTP APIs.
- External automation systems.
- Notification services.
- Malware and security scanners.
- Search systems.
- Optional vector-database integrations.

External integrations must be explicitly configurable and must not undermine the product's self-hosted and privacy-focused operating model.

### 3.21 REST API

The product must provide programmatic access to supported PDF operations, including:

- File upload and download.
- Conversion.
- Page management.
- OCR.
- Security operations.
- Metadata operations.
- Compression.
- Repair.
- Workflow execution.
- Asynchronous job execution and job-status polling.
- Monitoring and health endpoints.
- API-key authentication.
- Interactive API documentation.

### 3.22 MCP and AI integration

The product must support governed Model Context Protocol integration so approved AI assistants can invoke permitted PDF operations. The integration must support:

- API-key or OAuth authentication for MCP clients.
- Per-operation access controls.
- Upload and download handling.
- Conversion, editing, security, and document-processing operations.
- Optional document question answering.
- Optional summarization.
- Optional classification and review.
- Optional retrieval.
- Optional comment generation.
- Optional AI-assisted document creation or modification.

AI functionality must remain permission-scoped and privacy-aware. External model use, if any, must be clearly disclosed and administratively controllable.

### 3.23 Search and discovery

The product must support:

- Searching available PDF tools.
- Searching stored documents.
- Searching text within PDFs.
- Searching metadata, comments, annotations, and library content.
- Surfacing recently used documents and operations.
- Global application search.

### 3.24 User accounts and access control

The product must support:

- Local accounts.
- Optional authentication modes where appropriate.
- OAuth 2.0 and OpenID Connect SSO.
- Account invitations.
- User roles.
- Team-based permissions.
- Administrator controls.
- Registration policies.
- Account-lockout protections.
- Per-user feature permissions.
- Per-user storage limits.

### 3.25 Privacy

The product must:

- Support self-hosted deployment.
- Keep document processing local where possible.
- Avoid requiring documents to be uploaded to third-party cloud providers.
- Allow administrators to disable unnecessary external integrations.
- Clean temporary files automatically.
- Provide retention controls.
- Clearly expose which external services are enabled.
- Integrate with applicable GoreeCloud privacy requirements.

### 3.26 Administration

The product must provide centralized administration for:

- Configuration.
- User administration.
- Storage management.
- Authentication settings.
- Feature controls.
- Dependency controls.
- File-size and processing limits.
- Audit logging.
- Database backup and restoration.
- Scheduled backups.
- Diagnostics.
- Monitoring.
- Performance tuning.
- System-health information.

### 3.27 Deployment

The project must support, where technically applicable:

- Self-hosted server operation.
- Docker.
- Container orchestration.
- Linux.
- Windows.
- macOS.
- Desktop applications.
- Browser-based access.
- Headless/API-focused deployments.
- LAN-only installations.
- Reverse-proxy configurations.
- Air-gapped environments where dependency requirements permit.

### 3.28 Interface and accessibility

The product must provide:

- A responsive web interface.
- Desktop-oriented workflows.
- Mobile-friendly document access.
- Light and dark appearance modes.
- Keyboard shortcuts.
- Quick-access tools.
- Global search.
- Recent-tool suggestions.
- Multilingual UI support.
- Accessible navigation and controls.
- Configurable GoreeCloud branding.

Glaze UI should provide the consistent GoreeCloud visual and accessibility foundation when implementation begins.

### 3.29 Enterprise and large-scale processing

The architecture must be capable of supporting:

- Multi-node deployments.
- Shared databases.
- Shared object storage.
- Load balancing.
- Scalable document-processing workers.
- Centralized auditing.
- Centralized policy management.
- Compliance workflows.
- Monitoring and metrics.
- Large document libraries.
- Bulk document processing.

### 3.30 GoreeCloud ecosystem integration

The project is intended to integrate with:

- **GoreeCloud Identity** for authentication and account management.
- **GoreeCloud Drive and document storage** for file access and persistence.
- **GoreeCloud Office Suite** for PDF export, preview, print, conversion, and document workflows.
- **Wardveil Security** for document scanning and security boundaries.
- **GoreeCloud Privacy Shield** for privacy controls.
- **Glaze UI** for consistent design and accessibility.
- **GoreeCloud APIs** for cross-application document processing.
- **Future GoreeCloud automation systems** for coordinated document workflows.

These are planned integration requirements, not current implementation claims.

## 4. Architecture and implementation boundaries

The implementation should separate interactive application concerns from reusable document-processing services so that the same processing foundation can serve the web interface, desktop clients, APIs, workflows, and other GoreeCloud applications.

The architecture should keep document operations composable, job-oriented where processing is expensive, and suitable for both single-document interactive use and high-volume automated workloads.

## 5. Security requirements

Implementation must apply GoreeCloud security governance, including least privilege, safe parsing of untrusted documents, dependency security, secure temporary-file handling, protected secrets, strong authentication and authorization, auditable administrative operations, and fail-closed handling for unsafe document content.

Security-sensitive operations such as password removal, permission changes, redaction finalization, signature operations, and sanitization must make authorization and destructive effects explicit.

## 6. Privacy requirements

Privacy is a primary product boundary. The implementation must prefer local processing, minimize unnecessary disclosure, provide administrator control over external services, support retention and cleanup controls, and avoid silent transmission of document content to third parties.

## 7. Data, storage, and retention

Persistent document-library features must define authoritative storage, metadata, history, retention, cleanup, backup, restore, quota, and deletion behavior. Temporary processing artifacts must have bounded lifetimes and reliable cleanup.

## 8. Interface requirements

The user experience must remain accessible, responsive, keyboard-operable, and consistent with GoreeCloud design conventions. Complex tools should be available in a unified workspace without forcing repeated uploads.

## 9. API and automation requirements

Interactive UI actions and automation should converge on reusable processing primitives rather than separate incompatible implementations. Long-running work should use asynchronous jobs with observable state, retry behavior, and bounded resource consumption.

## 10. Testing and acceptance

A planned item may be moved to implemented documentation only when evidence supports the claimed level of implementation.

Acceptance evidence should include, as applicable:

- Source implementation.
- Automated tests.
- Representative document fixtures.
- Security and malformed-document tests.
- Data-loss and corruption checks.
- Accessibility validation.
- API contract validation.
- Cross-format conversion validation.
- Target-platform validation.
- Runtime and deployment verification.
- Upgrade, backup, restore, and rollback validation where applicable.

Repository presence, a merged pull request, or passing source-level tests alone must not be represented as production validation.

## 11. Product summary

GoreeCloud PDF Manager is planned as GoreeCloud's comprehensive PDF and document-processing platform, combining PDF reading, editing, page management, conversion, OCR, scanning, forms, annotations, digital signatures, redaction, security, compression, storage, sharing, automation, APIs, MCP/AI integration, and large-scale document processing in a privacy-focused, self-hosted environment.

It is intended to function both as a standalone GoreeCloud PDF application and as a shared PDF-processing foundation for the wider GoreeCloud ecosystem.
