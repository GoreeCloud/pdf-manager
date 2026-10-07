# GoreeCloud PDF Manager

GoreeCloud PDF Manager is a self-hosted PDF workbench for organizing, converting, optimizing, editing, inspecting, and protecting PDF documents.

This repository is a **GoreeCloud-maintained fork/rebuild** derived from the MIT-licensed core of Stirling-PDF. The current upstream baseline is `Stirling-Tools/Stirling-PDF@973bff865cc19fbc268859e1fb13103c66c1f5a5`.

## Current lifecycle

**Forge** — active product construction. This repository is not yet Anchor-qualified or production-approved.

## Current foundation

- License-safe core-only Stirling processing source.
- Restricted Stirling proprietary/SaaS/engine/desktop/cloud/portal trees excluded.
- Independently owned GoreeCloud browser shell.
- Glaze V1.7 / `1.7.0` runtime pinned from `GoreeCloud/glaze@9ab08060d723b022cdf07d001e8c95bca626a764`.
- Canonical PDF Manager icon synchronized from `GoreeCloud/branding-assets`.
- Fourteen direct Glaze workbench workflows spanning organization, optimization, editing, sanitization, and password protection.
- Server-authoritative capability availability with fail-closed execution when a tool is disabled or cannot be verified.
- First-use onboarding plus replayable, user-controlled contextual guidance.
- No analytics, advertising, remote fonts, or third-party file-upload service in the GoreeCloud shell.
- Source-boundary and CI controls to prevent restricted upstream code from entering this repository.

## Build

The project requires a full JDK compatible with the Gradle build.

```bash
./gradlew :stirling-pdf:bootJar
```

Development server:

```bash
./gradlew :stirling-pdf:bootRun
```

## Documentation

- [Documentation index](docs/README.md)
- [Project specifications](docs/PROJECT-SPECIFICATIONS.md)
- [Project record](docs/PROJECT-RECORD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Implemented features](docs/IMPLEMENTED-FEATURES.md)
- [Planned features](docs/PLANNED-FEATURES.md)
- [Changelogs](docs/CHANGELOGS.md)
- [Validation](docs/VALIDATION.md)
- [Security](docs/SECURITY.md)
- [Privacy](docs/PRIVACY.md)
- [Branding and Glaze](docs/BRANDING.md)
- [Glaze adoption](docs/GLAZE-ADOPTION.md)
- [Upstream maintenance](docs/UPSTREAM.md)
- [User manual](docs/USER-MANUAL.md)
- [Competitive objectives](docs/COMPETITIVE-OBJECTIVES.md)

## Licensing

See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md). GoreeCloud intentionally excludes source that upstream marks as subject to the Stirling PDF User License.
