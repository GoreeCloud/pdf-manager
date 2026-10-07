# Privacy — GoreeCloud PDF Manager

## Default behavior

The GoreeCloud shell contains no optional telemetry, behavioral analytics, advertising, remote font calls, or third-party file-upload integration. Core operations send selected documents only to the PDF Manager server the user is currently using.

This is a server-processing model; it is not a claim that all processing happens locally inside the browser.

## Data minimization

- Upload only data required for the selected operation.
- Do not collect optional profile or behavioral data without an approved purpose.
- Do not log full request/response bodies in normal operation.
- Keep temporary processing data bounded and clean it up when its lifecycle permits.
- Keep public sharing and external integrations disabled unless explicitly required and approved.

## Platform boundary

Privacy Shield integration is applicable but not accepted for this Forge candidate. No Privacy Shield protected state may be shown without authoritative evidence.

## Deployment responsibility

TLS, network exposure, account requirements, retention, storage, backups, logs, external processors, and data location are deployment controls and must be verified in the actual target environment before production privacy acceptance.
