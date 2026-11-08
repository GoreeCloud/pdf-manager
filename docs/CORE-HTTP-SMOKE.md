# Nonpublishing loopback Java core smoke

**Development evidence only.** This test does not deploy a server, enable remote access, publish binaries, or validate application security in production.

The dedicated [core HTTP smoke workflow](../.github/workflows/core-http-smoke.yml) builds the MIT-core-only Spring Boot JAR using Java 25 and the pinned Gradle version. It runs the [core JAR structure verifier](../scripts/verify_core_jar.py) and [loopback HTTP smoke](../scripts/smoke_core_http.py) on a disposable CI runner.

## Test contract

- Starts the real Java application in a temporary working directory, bound to **127.0.0.1** on a dynamically allocated port. The sandbox process gets a minimal environment with **no GitHub token, provider credentials or owner data forwarded explicitly**.
- Restricts the test client to numeric IPv4 loopback, ignores proxy environment configuration, and refuses redirects. No calls to third-party websites are initiated by the test client.
- Uses Java headless mode with a bounded heap; startup has a deadline. The application is terminated and reaped even after a failed check, and temporary fixture and log files are discarded.
- Disables login **only in this disposable loopback test**; it is not a production authentication recommendation or a modification to the application defaults.
- Verifies the real GET `/api/v1/info/health` returns HTTP 200 and JSON status `UP`, then sends two small **synthetic** one-page PDF documents to POST `/api/v1/general/merge-pdfs`.
- Requires HTTP 200, an application/pdf response and plausible bounded PDF bytes. The two input fixtures were separately verified with `pdfinfo` locally; a comprehensive semantic output-page-count test is a later gate.

Eight offline regression tests cover syntactically valid synthetic PDF construction, multipart input, label restrictions, invalid remote/credential-bearing request URLs, missing JAR refusal, and ephemeral port selection.

## Security and release boundaries

The app itself is **not** network-sandboxed by the workflow. Although it binds only to loopback and nonessential integrations are disabled, this test does not prove the JVM never makes outbound connections, that unknown PDFs can be safely parsed, or that temporary documents and logs meet the final GoreeShield retention policy. The test does not expose a network listener to the user's VPS or LAN. The job grants GitHub Actions **read-only** repository permissions, runs without deployment secrets, and publishes no JAR or generated PDF artifact.

It is insufficient for authentication, policy, multi-tenant access, malware isolation, full merge correctness, page/content preservation, supported-platform testing, licensing or stable release certification. A failure is a legitimate development blocker; a pass is only evidence of **isolated boot and one synthetic PDF merge**.
