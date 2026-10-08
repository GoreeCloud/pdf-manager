# User Manual — GoreeCloud PDF Manager

## Workspace

Drop PDFs, supported images, or supported office/text documents into the Workspace or choose files from the device. Use the up/down controls to define multi-file order and remove files when they are no longer needed. Each workflow validates that the files it will submit match its required input type before sending a request.

## Direct workflows

Tools marked **Workbench ready** currently include Merge PDFs, Split PDF, Rotate pages, Optimize & compress, Extract images, Crop pages, Rearrange pages, OCR scanned PDFs, Convert to PDF/A, PDF to Word, PDF to presentation, PDF to Excel, PDF to images, Images to PDF, PDF to EPUB / AZW3, Office to PDF, Document metadata, Page numbers, Text stamp & watermark, Image stamp & watermark, Sanitize PDF, Redact text, Add password, Remove password, Repair PDF, Flatten PDF, and Remove images.

1. Add required files.
2. Select a ready tool.
3. Review options.
4. Run the tool.
5. The browser downloads the returned result.

For crop, **Auto-detect content bounds** ignores manual coordinates and trims detected white space on the selected pages. Manual crop requires X, Y, width, and height. Removing data outside the crop uses the server Ghostscript path when that capability is enabled.

OCR accepts one or more Tesseract language codes and depends on OCR capabilities installed on the PDF Manager server. It exposes skip/force mode, text-layer, deskew, orientation, cleanup, image-removal, and sidecar controls. PDF/A conversion is limited in the core-only workbench to level-B PDF/A-1/2/3 profiles; strict mode fails rather than returning output that does not pass compliance validation.

For rearrangement, **Custom page order** accepts page/range expressions such as `3,1,2` or `1-4`; **Duplicate** uses the page-order field as the duplicate count.

Page numbering supports `{n}`, `{total}`, and `{filename}` in its text pattern. Text stamps support selected pages, opacity, rotation, grid position, margin, and optional X/Y overrides. Image stamps accept a PNG or JPEG selected from the device and use the same server stamp endpoint with explicit height, position, rotation, opacity, margin, and optional coordinate overrides.

PDF-to-Word supports DOCX, DOC, and ODT. PDF-to-presentation supports PPTX, PPT, and ODP. Both remain disabled when the server reports the required conversion capability unavailable. PDF-to-Excel accepts a page selection and extracts detected tabular data into an XLSX workbook.

PDF-to-images supports selected pages, PNG/JPEG/GIF, combined or per-page output, color mode, DPI, and optional annotation rendering. WebP remains outside the direct Glaze workflow because it has an additional Python dependency that is not represented by the general PDF-to-image capability state. Images-to-PDF uses all workspace images in visible order and exposes page fitting, color mode, and auto-rotation.

PDF-to-EPUB/AZW3 exposes reader profile and chapter-detection controls and remains unavailable unless the server reports its Calibre-backed conversion capability. Office-to-PDF accepts supported office/text documents and lets the server select its configured in-process, Unoconvert, or LibreOffice conversion path. Remove images strips embedded raster-image resources, including images nested in form XObjects.

Sanitization defaults to removing JavaScript actions and embedded files. More destructive options such as link, metadata, and embedded-font removal remain explicit opt-ins.

OCR remains unavailable when the server reports the required OCR dependency missing. Text redaction removes matching text content rather than applying only a visual overlay; review patterns and optional regular-expression matching carefully before running it.

Password protection is processed by the PDF Manager server. Password fields are rendered as password inputs and are not stored in PDF Manager application state; reopening a tool dialog reconstructs the controls.

Tools marked **API available** exist in the retained backend but do not yet have a dedicated GoreeCloud workflow; use the API documentation for their current request contract.

## Tool availability

PDF Manager asks the server for current endpoint availability before allowing execution. A tool may be shown as **Dependency unavailable** when a required processor is missing, **Disabled by server** when configuration turns it off, or **Checking server** when availability has not yet been verified. Unknown availability is fail-closed: PDF Manager does not enable execution until the server confirms the capability.

## First-use guide and hints

On first use, PDF Manager opens a concise three-step guide covering the workbench model, server-side document processing, privacy expectations, capability truth, and contextual hints.

Choose **Not now** to interrupt the guide; the current step is retained and offered again on a later visit. Completing the guide stops automatic replay. Choose **Guide** in the top bar to replay it voluntarily.

Ordinary contextual hints can be dismissed individually. The final Guide step also provides a global **Show contextual hints** control that can disable or re-enable ordinary hints. Turning hints off does not suppress errors, security warnings, confirmations, service state, or other required system truth.

## Appearance

The initial appearance follows the system preference. The top-bar appearance control toggles light and dark.

## Privacy expectation

Selected files are sent to the PDF Manager server in use so the requested server-side processing can occur. The GoreeCloud shell does not send those files to an analytics or third-party upload service.
