# GoreeShield PDF chapter and rearrangement log minimization

**Status:** narrow proposed source patch on a draft pull request; no production traffic, real personal PDF content, deployment or full application-wide log audit.

The source review identified application logging of upload-provided original filenames, PDF bookmark titles (document content), filenames derived from chapter titles, and a temporary ZIP file path in SplitPdfByChaptersController. RearrangePagesPDFController also logged exception objects including a stack or parser message potentially derived from client input. These are not necessary for ordinary operational diagnostics.

This patch replaces those log emissions with fixed event categories, a non-identifying bookmark count, or the Java exception **class name**. It leaves generated HTTP download/ZIP filenames and actual PDF/ZIP operations unchanged. A new read-only Python regression suite runs in the pinned core-build workflow; the existing Java smoke/build gates remain in place.

The tests establish a **static source contract**, not proof of privacy for other controllers, global error handling, PDF libraries, server access logs, reverse proxies, hosted infrastructure, or production. Additional source scans and real staging tests remain necessary before release. Never use private documents as test fixtures without consent.
