# Implemented Features

## Current state

**Lifecycle:** Lab  
**Implementation state:** Exploratory native foundation

The repository contains one evidence-backed development foundation. It does not yet contain a usable end-user PDF Manager application.

## Implemented foundation

### Bounded PDF input preflight

**State:** Implemented for exploratory development use.

Evidence:

- `crates/pdf-core/src/lib.rs` provides a standard-library-only preflight library.
- Input size is checked against a caller-configured limit.
- Header inspection is bounded to the first 1024 bytes.
- The three-character PDF version token is parsed.
- EOF-marker discovery is bounded to the final 2048 bytes and is reported only as a hint.
- `apps/pdf-manager-cli` exposes the operation through a development-only command.
- Unit tests cover valid and invalid headers, version parsing, size limits, EOF-hint behavior, and bounded header scanning.
- Rust Foundation CI validates formatting, build, unit tests, and clippy.

This foundation is **not** full PDF validation, sanitization, document repair, malware scanning, editing, rendering, conversion, or a supported user feature.

## Product feature boundary

All 30 user-facing and system-level product capability areas remain planned in [PLANNED-FEATURES.md](PLANNED-FEATURES.md). The bounded preflight foundation does not promote any complete product capability area to implemented status.

## Promotion rule

A capability may be added here only when implementation evidence supports the claimed state. Where production or target-environment validation is required, source code or a merged pull request alone is insufficient.
