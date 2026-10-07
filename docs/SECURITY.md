# Security — GoreeCloud PDF Manager

PDF Manager is in Forge; this document is not a production-security certification.

## Implemented boundaries

- Restricted upstream source is excluded and checked by repository validation.
- The GoreeCloud shell loads only same-origin scripts, styles, fonts, images, and API requests.
- A Content Security Policy is declared by the workbench source.
- The UI does not manufacture protected, safe, sanitized, authenticated, or encrypted states.
- The retained core includes the security-oriented dependency pins present at the recorded upstream baseline.

## Threat priorities

Hostile PDFs, images, archives, metadata, fonts, embedded objects, URLs, and conversion inputs are untrusted. Production hardening must cover upload limits, parser resource limits, timeouts, archive/path traversal, SSRF, command injection, process isolation, dependency CVEs, temporary-file cleanup, least privilege, private admin exposure, authorization, and secret separation.

Normal logs must avoid full document bodies and unnecessary user behavior data.

## Platform boundary

Wardveil Security integration is applicable but not accepted for this Forge candidate. The UI must not claim Wardveil protection until authoritative runtime evidence exists.

## Release blockers

Critical/high unresolved security defects, unreviewed vulnerable dependencies, insecure public exposure, missing required authorization, or material hostile-file failures block lifecycle promotion.
