# User Manual — GoreeCloud PDF Manager

## Add documents

Use the Workspace drop area to select PDFs or supported images. Files stay in the browser workspace until removed or the page is refreshed. For merge operations, the visible file order controls the merge order.

## Run a workbench-ready tool

1. Add the required file or files.
2. Choose a tool marked **Workbench ready**.
3. Review its options.
4. Select **Run tool**.
5. The browser downloads the result returned by the server.

Current direct workflows: merge, split, rotate, optimize/compress, and extract images.

## API-available tools

Cards marked **API available** identify retained processing capabilities without a finished dedicated GoreeCloud workflow. Use the API link to inspect the current request contract.

## Appearance

The first visit follows the operating-system appearance. The top-bar appearance control can switch light/dark.

## Privacy expectation

The GoreeCloud interface does not send files to an analytics or third-party upload service. Selected files are submitted to the PDF Manager server used for processing.

## Error behavior

Processing returns a new result rather than overwriting the browser-selected source file. An operation failure therefore does not itself modify the source file on the user's device.
