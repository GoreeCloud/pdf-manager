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

Thirty offline regression tests cover synthetic PDF construction, multipart upload, loopback-only HTTP, bounded diagnostics and rejection of malformed, missing, reversed or oversized merged-PDF results. An independent local experiment merged two synthetic PDFs using pdfunite, then verified pages and content with pdfinfo and pdftotext.

## Synthetic malformed-input resilience

After the successful two-page merge, the same isolated test also submits a valid generated PDF followed by a deliberately truncated PDF without page objects. The controller now acts on its existing prevalidation failures *before* native merging and raises its typed corrupted-PDF client exception; two targeted Java tests guard this behavior. The upload must be rejected with HTTP 400 rather than returning a document or a server error. The test then checks that the already-running JVM still reports HTTP 200 and status UP. Response bodies, uploaded bytes and stack traces are never printed. This covers only one deterministic malformed input, not denial-of-service resilience, parser fuzzing, resource exhaustion or general hostile-PDF acceptance.

## Empty-upload input validation

A second negative case submits a correctly terminated multipart/form-data body with **zero file parts**. The core merge endpoint must reject missing inputs with HTTP 400 using its existing typed file validation exception, rather than producing an invalid zero-byte document or consuming native resources. Focused Java tests cover both null and empty file arrays; the real loopback test verifies the HTTP response. The original two-page success and corrupted-input health tests remain mandatory. After both negative cases, the **same still-running JVM** must process another freshly generated synthetic two-file merge whose returned PDF is independently inspected for exactly two pages with ordered Alpha/Beta content. This checks functional recovery, not merely liveness.

## Bounded multipart uploads and HTTP 413 recovery

The inherited Spring Boot defaults permitted an individual multipart file
and an aggregate request up to 2,000 MB each, a high resource-exhaustion risk
for a development-only preview. The core now uses a **128 MiB per-file and
256 MiB total-request default**, independently enforced by the multipart
parser and still configurable by explicit environment variables after resource
and authorization review. This does **not** provide CPU, page-count, image
decompression, network isolation or tenant quota protection.

To verify the actual servlet parser rather than just configuration metadata,
the nonpublishing Java smoke temporarily sets **32 KiB per file / 64 KiB per
request** for its single ephemeral loopback JVM. It sends an in-memory **about
40 KiB synthetic PDF part** in a request below 64 KiB and requires HTTP 413.
Another request uses two **individually under-32 KiB** PDF parts whose
combined multipart body exceeds the independent 64 KiB request cap; this
must also return **HTTP 413**. A valid merge then follows both errors on
the **same** Java process. The custom Spring MultipartConfigElement honors
the independent file and aggregate defaults, explicit SPRING_* environment
limits and legacy settings.yml fileUploadLimit, and rejects malformed
limits at startup instead of falling back to 2,000 MB. No user PDF,
payload/error body, file or secrets are uploaded to CI logs. All defaults and
environment overrides are limited to this source build/runtime; a signed
desktop app and network-facing operation remain unapproved.

## Missing upstream pipeline presets

The sanitized core-only source tree lacks the upstream static/pipeline/defaultWebUIConfigs assets. Its previous unconditional extraction aborted JVM startup. The preview now **skips only optional automatic pipeline preset extraction when the complete resource set is absent**. Explicit extraction is still strict and fails for incomplete/bad resources; the missing preset functionality is **not** declared restored or licensed. Java startup regression tests cover both branches.

## Security and release boundaries

The app itself is **not** network-sandboxed by the workflow. Although it binds only to loopback and nonessential integrations are disabled, this test does not prove the JVM never makes outbound connections, that unknown PDFs can be safely parsed, or that temporary documents and logs meet the final GoreeShield retention policy. The test does not expose a network listener to the user's VPS or LAN. The job grants GitHub Actions **read-only** repository permissions, runs without deployment secrets, and publishes no JAR or generated PDF artifact.

It remains insufficient for authentication, policy, multi-tenant isolation, malware resistance, all real-world PDF formats, cross-platform compatibility, licensing, or Stable release certification. A passing run demonstrates only **isolated startup plus an ordered two-page, synthetic merge**.
