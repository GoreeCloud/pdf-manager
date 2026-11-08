# Nonpublishing loopback Java core smoke

**Development evidence only.** This test does not deploy a server, enable remote access, publish binaries, or validate application security in production.

The existing branch-protected [Java 25 core CI job](../.github/workflows/core-build.yml) builds the MIT-core-only Spring Boot JAR using Java 25 and the pinned Gradle version. It runs the [core JAR structure verifier](../scripts/verify_core_jar.py) and [loopback HTTP smoke](../scripts/smoke_core_http.py) on a disposable CI runner.

## Test contract

- Starts the real Java application in a temporary working directory, bound to **127.0.0.1** on a dynamically allocated port. The sandbox process gets a minimal environment with **no GitHub token, provider credentials or owner data forwarded explicitly**.
- Restricts the test client to numeric IPv4 loopback, ignores proxy environment configuration, and refuses redirects. No calls to third-party websites are initiated by the test client.
- Uses Java headless mode with a bounded heap; startup has a deadline. The application is terminated and reaped even after a failed check, and temporary fixture and log files are discarded.
- Disables login **only in this disposable loopback test**; it is not a production authentication recommendation or a modification to the application defaults.
- Verifies the real GET `/api/v1/info/health` returns HTTP 200 and JSON status `UP`, then sends two small **synthetic** one-page PDF documents to POST `/api/v1/general/merge-pdfs`.
- Requires HTTP 200, an application/pdf response and bounded PDF bytes.
- The CI-only, separately installed Poppler pdfinfo and pdftotext utilities parse the **actual merged response** from standard input. The gate requires **exactly two readable pages containing Alpha then Beta**, in their original order. Incorrect count, text, order or parsing failures reject the run; no response bytes or extracted text are published.
- Tools run as subprocesses without a shell or proxy configuration; verifier output and timeout are bounded, executable paths are checked and conversion errors never echo document contents. Poppler is a testing utility, not shipped with GoreeCloud. If absent on the disposable runner, the workflow installs the signed Ubuntu poppler-utils package.

Twenty offline regression tests cover synthetic PDF construction, multipart upload, loopback-only HTTP, bounded diagnostics and rejection of malformed, missing, reversed or oversized merged-PDF results. An independent local experiment merged two synthetic PDFs using pdfunite, then verified pages and content with pdfinfo and pdftotext.

## Missing upstream pipeline presets

The sanitized core-only source tree lacks the upstream static/pipeline/defaultWebUIConfigs assets. Its previous unconditional extraction aborted JVM startup. The preview now **skips only optional automatic pipeline preset extraction when the complete resource set is absent**. Explicit extraction is still strict and fails for incomplete/bad resources; the missing preset functionality is **not** declared restored or licensed. Java startup regression tests cover both branches.

## Security and release boundaries

The app itself is **not** network-sandboxed by the workflow. Although it binds only to loopback and nonessential integrations are disabled, this test does not prove the JVM never makes outbound connections, that unknown PDFs can be safely parsed, or that temporary documents and logs meet the final GoreeShield retention policy. The test does not expose a network listener to the user's VPS or LAN. The job grants GitHub Actions **read-only** repository permissions, runs without deployment secrets, and publishes no JAR or generated PDF artifact.

It remains insufficient for authentication, policy, multi-tenant isolation, malware resistance, all real-world PDF formats, cross-platform compatibility, licensing, or Stable release certification. A passing run demonstrates only **isolated startup plus an ordered two-page, synthetic merge**.
