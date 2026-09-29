# Security Policy

## Current security status

GoreeCloud PDF Manager is in the **Seed** lifecycle stage and has no verified application runtime.

No claim is made that the planned PDF parsing, editing, conversion, OCR, signing, redaction, storage, API, or automation surfaces are currently security-hardened because those surfaces do not yet exist.

## Reporting a vulnerability

Do **not** open a public issue, discussion, or pull request for a vulnerability that could expose users, documents, credentials, systems, or infrastructure.

Use this repository's **Security** tab and private vulnerability-reporting flow when available.

If a private GitHub reporting flow is not available, use the official GoreeCloud contact page and identify `GoreeCloud/pdf-manager`. Do not send reusable credentials, private keys, access tokens, private user documents, or other secrets unless an explicitly authorized secure channel has been established.

The organization-level guidance is maintained in `GoreeCloud/.github/SECURITY.md`.

## Planned security boundaries

Implementation must treat PDFs and converted document formats as untrusted content. Required security concerns include:

- bounded parsing and resource use;
- malformed and adversarial document handling;
- embedded JavaScript and attachment inspection;
- unsafe external-link handling;
- decompression-bomb and oversized-resource resistance;
- secure temporary-file lifecycle;
- process isolation where appropriate;
- dependency and supply-chain security;
- least-privilege storage and worker access;
- strict authorization for sensitive document operations;
- permanent redaction verification;
- signature and certificate validation;
- malware/security-scanner integration hooks;
- auditable administrative and high-risk actions;
- safe API/MCP file transfer and operation permissions.

## Secrets

Do not commit passwords, API keys, private keys, certificates containing private key material, production tokens, session secrets, signing secrets, or private user documents.

Sanitized examples may be added only when they contain no reusable secret.

## Supported versions

No supported software version currently exists.

Security-support scope must be updated when the first release is created.

## Disclosure

Please allow time for triage and remediation before public disclosure. Disclosure timing should reflect severity, available mitigations, affected release state, and user impact.
