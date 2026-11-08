/**
 * Optional policy links must be operator-provided, never synthesized from
 * the upstream publisher. Only HTTPS URLs or same-origin relative paths are
 * eligible for a link. This checks URL syntax, NOT legal policy ownership.
 */
export function serviceLegalHref(value?: string | null): string | undefined {
  // Check controls before trimming: a URL with embedded newlines is unsafe.
  if (value == null) return undefined;
  if (/[\u0000-\u001f\u007f\\]/.test(value)) return undefined;
  const link = value.trim();
  if (!link) return undefined;
  if (link.startsWith("//")) return undefined;
  if (link.startsWith("/")) return link;

  // Reject javascript:, data:, mailto:, file:, http: and credentials in URLs.
  if (/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(link)) {
    try {
      const parsed = new URL(link);
      return parsed.protocol === "https:" && !!parsed.hostname && !parsed.username && !parsed.password
        ? link
        : undefined;
    } catch {
      return undefined;
    }
  }
  // Filenames in the app's static folder are also supported as policy links.
  if (/^[a-zA-Z0-9_-][a-zA-Z0-9_./%-]*$/.test(link) && !link.includes("..")) {
    return link;
  }
  return undefined;
}
