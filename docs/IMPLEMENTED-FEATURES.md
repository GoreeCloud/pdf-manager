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

## Direct workbench workflows

- Merge PDFs and supported images.
- Split PDF by page split-points, ranges, functions, or every page.
- Rotate pages by 90, 180, or 270 degrees.
- Optimize/compress with optimization, size target, linearization, normalization, and grayscale options.
- Extract embedded images to PNG, JPEG, or GIF archive output.
- Rearrange pages with custom order, reverse, duplex, booklet, odd/even, duplicate, and edge-removal modes.
- Update or deliberately remove standard document metadata.
- Add page numbers or Bates-style numbering with page, position, font, color, text-pattern, and zero-padding controls.
- Add text stamps/watermarks with page selection, alphabet, size, rotation, opacity, position, margin, color, and coordinate overrides.
- Sanitize PDFs by removing selected JavaScript, embedded files, metadata, links, or embedded fonts.
- Add PDF password protection with encryption-key and permission controls.
- Remove password protection when the current password is known.
- Attempt structural PDF repair through the server's available Ghostscript, qpdf, or PDFBox path.
- Flatten form fields or full pages with configurable render DPI.

## Retained processing API

The adopted open-source core exposes substantially broader PDF/page organization, conversion, OCR, cropping, overlays, redaction, signatures, forms, pipeline, and related endpoints. Dedicated Glaze workflows and environment-specific acceptance remain open where not listed above.
