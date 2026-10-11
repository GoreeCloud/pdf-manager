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
    // Count Unicode code points so truncation cannot split a surrogate pair.
    const codepoints = Array.from(leaf);
    const dot = leaf.lastIndexOf(".");
    const extension = dot > 0 && leaf.length - dot <= 20 ? Array.from(leaf.slice(dot)) : [];
    const shortened = codepoints.length <= 180
      ? leaf
      : codepoints.slice(0, 180 - extension.length).concat(extension).join("");
    // Windows devices remain reserved even when followed by a space and extension.
    return /^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])[ .]/i.test(shortened + ".")
      ? "file-" + shortened
      : shortened;
  };
  return clean(value) || clean(fallback) || "download";
}

/** Split Content-Disposition parameters without treating quoted semicolons as delimiters. */
function dispositionParameters(header) {
  if (typeof header !== "string" || header.length > 4096) return null;
  const parts = [];
  let part = "";
  let quoted = false;
  let escaped = false;
  for (const char of header) {
    if (escaped) {
      part += char;
      escaped = false;
    } else if (quoted && char === "\\") {
      escaped = true;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === ";" && !quoted) {
      parts.push(part.trim());
      part = "";
    } else {
      part += char;
    }
  }
  if (quoted || escaped) return null;
  parts.push(part.trim());
  const params = new Map();
  for (const field of parts.slice(1)) {
    const index = field.indexOf("=");
    if (index < 1) continue;
    const key = field.slice(0, index).trim().toLowerCase();
    if (key !== "filename" && key !== "filename*") continue;
    // Reject ambiguous duplicate names instead of choosing a guessed authority.
    if (params.has(key)) return null;
    params.set(key, field.slice(index + 1).trim());
  }
  return params;
}

export function filenameFromDisposition(disposition, fallback) {
  const params = dispositionParameters(disposition);
  if (!params) return safeDownloadFilename(fallback);
  if (params.has("filename*")) {
    const match = /^UTF-8'[^']*'(.+)$/i.exec(params.get("filename*"));
    if (!match) return safeDownloadFilename(fallback);
    try {
      return safeDownloadFilename(decodeURIComponent(match[1]), fallback);
    } catch {
      // Invalid percent-encoding or UTF-8 never becomes a suggested name.
      return safeDownloadFilename(fallback);
    }
  }
  return safeDownloadFilename(params.get("filename") ?? "", fallback);
}
