# Glaze V1.7 Adoption — PDF Manager

## Shared identity

- Repository: `GoreeCloud/glaze`
- Source: `9ab08060d723b022cdf07d001e8c95bca626a764`
- Target: Glaze V1.7 / `1.7.0`
- Runtime entrypoint: `js/glaze-v1.7.0.mjs`
- Rollback baseline: `1.6.0`

## Source adoption

The PDF Manager candidate vendors the shared V1.7 entrypoint and its inherited V1.6 runtime/CSS dependencies under the GoreeCloud static-resource tree. The product applies PDF-specific tokens and composition on top of the shared runtime.

## Acceptance state

**Implemented in source; consumer acceptance incomplete.**

Open obligations include rendered browser review, keyboard/assistive-technology acceptance, increased-contrast/forced-color evaluation, reduced-motion checks, compact-through-wide layouts, representative performance evidence, authority-boundary validation, rollback validation, human visual acceptance, and exact-source consumer-registry evidence where required.

Glaze being Anchor/Stable does not make PDF Manager production-eligible.
