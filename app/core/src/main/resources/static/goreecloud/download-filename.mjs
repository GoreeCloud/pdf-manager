/**
 * Download names are display hints from HTTP responses, not filesystem paths.
 * Normalize them before setting HTMLAnchorElement.download.
 */
export function safeDownloadFilename(value, fallback = "download") {
  const clean = (input) => {
    if (typeof input !== "string") return "";
    const leaf = input
      .replace(/[\u0000-\u001f\u007f-\u009f\u202a-\u202e\u2066-\u2069]/g, "")
      .split(/[\\/]/)
      .pop()
      .replace(/\s+/g, " ")
      .replace(/[<>:"|?*]/g, "_")
      .replace(/^[. ]+|[. ]+$/g, "");
    if (!leaf) return "";
    // Limit download labels without silently discarding a short extension.
    const dot = leaf.lastIndexOf(".");
    const suffix = dot > 0 && leaf.length - dot <= 20 ? leaf.slice(dot) : "";
    const shortened = leaf.length <= 180 ? leaf : leaf.slice(0, 180 - suffix.length) + suffix;
    return /^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(shortened)
      ? `file-${shortened}`
      : shortened;
  };
  return clean(value) || clean(fallback) || "download";
}

export function filenameFromDisposition(disposition, fallback) {
  if (typeof disposition !== "string") return safeDownloadFilename(fallback);
  const encoded = disposition.match(/(?:^|;)\s*filename\*\s*=\s*UTF-8''([^;]+)/i);
  if (encoded) {
    let name = encoded[1].trim().replace(/^"|"$/g, "");
    try {
      name = decodeURIComponent(name);
    } catch {
      // Malformed extended values are untrusted: prefer a safe fallback.
      return safeDownloadFilename(fallback);
    }
    return safeDownloadFilename(name, fallback);
  }
  const plain = disposition.match(/(?:^|;)\s*filename\s*=\s*(?:"([^"]*)"|([^;]*))/i);
  return safeDownloadFilename(plain ? (plain[1] ?? plain[2]).trim() : "", fallback);
}
