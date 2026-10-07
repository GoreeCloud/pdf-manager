# Architecture — GoreeCloud PDF Manager

```text
Browser / future GoreeCloud clients
             |
             v
GoreeCloud Glaze workbench
             |
      same-origin API
             |
             v
Spring Boot processing service
   |        |        |        |
 pages   convert   security   jobs
             |
             v
temporary/configured application storage
```

## Maintained-fork boundary

The repository retains upstream `app/common` and `app/core` plus required Gradle/build support. It excludes restricted Stirling proprietary, SaaS, engine, desktop, cloud, portal, and current frontend-workspace code.

The retained Java package namespace remains `stirling.software` for upstream compatibility in this Forge stage. Public product identity is GoreeCloud PDF Manager.

## UI boundary

The packaged entry source is `app/core/src/main/resources/static/api-landing.html`. The core-only build copies it to `index.html`.

GoreeCloud UI assets live under `static/goreecloud/`; the exact Glaze runtime snapshot is under `static/goreecloud/glaze/`.

## Trust boundaries

Browser-selected files, PDF structures, images, metadata, archives, fonts, URLs, and conversion content are untrusted. External processing executables remain separate deployment dependencies. UI state never grants authentication, authorization, privacy, security, recovery, or compliance authority.

## Data flow

Synchronous processing accepts multipart input and returns a new result. Temporary processing state is server-side. Asynchronous jobs may retain bounded job/file state through the retained job framework. Deployment-specific retention, backup, multi-user authorization, network exposure, and storage controls require separate acceptance.
