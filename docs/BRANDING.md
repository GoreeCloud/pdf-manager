# Branding and Glaze — GoreeCloud PDF Manager

## Branding authority

`GoreeCloud/branding-assets` is authoritative. PDF Manager consumes `products/pdf-manager/app-icon.svg`; local copies must remain synchronized with that source.

The current icon uses a product-specific red-to-violet field with a document/edit symbol. This is PDF Manager identity, not a platform-wide default color palette.

## Glaze

Current shared target: **Glaze V1.7 / 1.7.0**.

The workbench uses Glaze material, control, focus, motion, responsive, and semantic-state foundations with PDF Manager-specific composition and color.

## Experience requirements

- Task-first navigation.
- Clear Canvas → Surface → Glaze hierarchy.
- Consistent high-quality icon grammar.
- Color never as the only critical signal.
- Light/dark/system appearance.
- Reduced motion support.
- Strong keyboard focus.
- Responsive layouts and touch-safe targets.
- Truthful lifecycle/privacy/security state.

Vendoring Glaze and using its classes does not by itself establish consumer acceptance.
