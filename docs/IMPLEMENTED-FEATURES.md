# Implemented Features

This file records source implemented in the current candidate; it does not convert unverified runtime behavior into a production claim.

## Foundation

- Core-only Stirling processing source boundary.
- Restricted upstream trees absent.
- GoreeCloud-owned responsive Glaze workbench.
- Glaze V1.7 exact-source snapshot.
- Canonical GoreeCloud PDF Manager icon.
- Light/dark/system appearance behavior.
- Keyboard-visible controls, reduced-motion handling, responsive navigation, and Glaze-sized controls.
- Workspace file queue with duplicate suppression, deterministic ordering, removal, and reordering.
- Real backend readiness check rather than decorative status.
- No analytics, advertising, remote fonts, or third-party upload logic in the GoreeCloud shell.
- Server-authoritative tool availability sourced from `/api/v1/config/endpoints-availability`, with execution blocked when availability is disabled or cannot be verified.
- First-use three-step onboarding with resumable progress, voluntary replay through the Guide control, privacy/server-boundary education, and user-controlled contextual hints.
- Contextual hints for file setup, merge ordering, protection workflows, and dependency-backed conversion availability, with per-hint dismissal and a global preference.

## Direct workbench workflows

- Merge PDFs and supported images.
- Split PDF by page split-points, ranges, functions, or every page.
- Rotate pages by 90, 180, or 270 degrees.
- Optimize/compress with optimization, size target, linearization, normalization, and grayscale options.
- Extract embedded images to PNG, JPEG, or GIF archive output.
- Crop selected pages manually or auto-detect content bounds to trim white space.
- Rearrange pages with custom order, reverse, duplex, booklet, odd/even, duplicate, and edge-removal modes.
- Run OCR with explicit language, mode, render-layer, deskew, rotation, cleanup, sidecar, and image-removal controls.
- Convert PDFs to PDF/A-1B/2B/3B profiles with optional strict compliance when the server reports the conversion capability available.
- Convert PDFs to DOC/DOCX/ODT when the server reports the Word conversion capability available.
- Convert PDFs to PPT/PPTX/ODP when the server reports the presentation conversion capability available.
- Extract tables from selected PDF pages into XLSX workbooks through the retained PDF-to-Excel endpoint.
- Render selected PDF pages to PNG, JPEG, or GIF as a combined image or separate page images.
- Combine ordered workspace images into a PDF with explicit page-fit, color, and auto-rotation controls.
- Convert PDFs to EPUB or AZW3 with tablet/phone or Kindle-oriented profiles and optional chapter detection.
- Convert supported office/text documents to PDF through the server's available conversion path.
- Update or deliberately remove standard document metadata.
- Add page numbers or Bates-style numbering with page, position, font, color, text-pattern, and zero-padding controls.
- Add text stamps/watermarks with page selection, alphabet, size, rotation, opacity, position, margin, color, and coordinate overrides.
- Add PNG/JPEG image stamps or watermarks with page selection, physical height, rotation, opacity, position, margin, and coordinate overrides.
- Unlock supported read-only PDF form fields so they can be filled again.
- Add one or more embedded attachments with server-enforced per-file and aggregate size limits.
- Extract all embedded PDF attachments into a ZIP archive.
- Sanitize PDFs by removing selected JavaScript, embedded files, metadata, links, or embedded fonts.
- Permanently redact matching text or regular-expression patterns with whole-word, padding, color, and optional final rasterization controls.
- Add PDF password protection with encryption-key and permission controls.
- Remove password protection when the current password is known.
- Remove PDF digital-signature fields and return a new unsigned document.
- Attempt structural PDF repair through the server's available Ghostscript, qpdf, or PDFBox path.
- Flatten form fields or full pages with configurable render DPI.
- Remove embedded raster images, including images nested in PDF form XObjects.
- Validate workspace input compatibility before submission so PDF-only, image-only, mixed PDF/image, and office/text workflows fail locally on incompatible file types.

## Retained processing API

The adopted open-source core exposes substantially broader conversion, overlays, redaction, signatures, forms, pipeline, and related endpoints. Dedicated Glaze workflows and environment-specific acceptance remain open where not listed above.
