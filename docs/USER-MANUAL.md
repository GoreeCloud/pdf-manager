# User Manual — GoreeCloud PDF Manager

## Workspace

Drop PDFs or supported images into the Workspace or choose files from the device. Use the up/down controls to define merge order and remove files when they are no longer needed.

## Direct workflows

Tools marked **Workbench ready** currently include Merge PDFs, Split PDF, Rotate pages, Optimize & compress, Extract images, Rearrange pages, Document metadata, Page numbers, Text stamp & watermark, Sanitize PDF, Add password, Remove password, Repair PDF, and Flatten PDF.

1. Add required files.
2. Select a ready tool.
3. Review options.
4. Run the tool.
5. The browser downloads the returned result.

For rearrangement, **Custom page order** accepts page/range expressions such as `3,1,2` or `1-4`; **Duplicate** uses the page-order field as the duplicate count.

Page numbering supports `{n}`, `{total}`, and `{filename}` in its text pattern. Text stamps support selected pages, opacity, rotation, grid position, margin, and optional X/Y overrides.

Sanitization defaults to removing JavaScript actions and embedded files. More destructive options such as link, metadata, and embedded-font removal remain explicit opt-ins.

Password protection is processed by the PDF Manager server. Password fields are rendered as password inputs and are not stored in PDF Manager application state; reopening a tool dialog reconstructs the controls.

Tools marked **API available** exist in the retained backend but do not yet have a dedicated GoreeCloud workflow; use the API documentation for their current request contract.

## Appearance

The initial appearance follows the system preference. The top-bar appearance control toggles light and dark.

## Privacy expectation

Selected files are sent to the PDF Manager server in use so the requested server-side processing can occur. The GoreeCloud shell does not send those files to an analytics or third-party upload service.
