/**
 * Download names are display hints from HTTP responses, not filesystem paths.
 * Normalize them before setting HTMLAnchorElement.download.
 */
const SAFE_GENERIC_EXTENSIONS = new Set([
  "pdf", "zip",
  "png", "jpg", "jpeg", "gif", "webp", "bmp", "tif", "tiff",
  "txt", "rtf", "md", "html", "htm", "csv", "json", "xml",
  "doc", "docx", "odt", "ppt", "pptx", "odp", "xls", "xlsx", "ods",
  "epub", "azw3",
]);

const MIME_EXTENSIONS = new Map([
  ["application/pdf", ["pdf"]],
  ["application/zip", ["zip"]],
  ["application/x-zip-compressed", ["zip"]],
  ["image/png", ["png"]],
  ["image/jpeg", ["jpg", "jpeg"]],
  ["image/gif", ["gif"]],
  ["image/webp", ["webp"]],
  ["image/bmp", ["bmp"]],
  ["image/tiff", ["tif", "tiff"]],
  ["text/plain", ["txt"]],
  ["text/csv", ["csv"]],
  ["text/markdown", ["md"]],
  ["text/html", ["html", "htm"]],
  ["application/json", ["json"]],
  ["application/xml", ["xml"]],
  ["text/xml", ["xml"]],
  ["application/rtf", ["rtf"]],
  ["text/rtf", ["rtf"]],
  ["application/msword", ["doc"]],
  ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", ["docx"]],
  ["application/vnd.oasis.opendocument.text", ["odt"]],
  ["application/vnd.ms-powerpoint", ["ppt"]],
  ["application/vnd.openxmlformats-officedocument.presentationml.presentation", ["pptx"]],
  ["application/vnd.oasis.opendocument.presentation", ["odp"]],
  ["application/vnd.ms-excel", ["xls"]],
  ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ["xlsx"]],
  ["application/vnd.oasis.opendocument.spreadsheet", ["ods"]],
  ["application/epub+zip", ["epub"]],
  ["application/vnd.amazon.ebook", ["azw3"]],
]);

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

function filenameExtension(name) {
  const dot = name.lastIndexOf(".");
  if (dot <= 0 || dot === name.length - 1) return "";
  return name.slice(dot + 1).toLowerCase();
}

function constrainFilenameExtension(value, fallback, contentType = "") {
  const name = safeDownloadFilename(value, fallback);
  const normalizedType = String(contentType || "").split(";", 1)[0].trim().toLowerCase();
  const trustedExtensions = MIME_EXTENSIONS.get(normalizedType);
  const currentExtension = filenameExtension(name);

  if (trustedExtensions?.length) {
    if (trustedExtensions.includes(currentExtension)) return name;
    const base = currentExtension
      ? name.slice(0, -(currentExtension.length + 1))
      : name;
    return safeDownloadFilename(`${base || "download"}.${trustedExtensions[0]}`, fallback);
  }

  // Generic binary responses are used by several document converters. Keep only
  // extensions that PDF Manager itself can legitimately produce; executable or
  // script-like suffixes from an untrusted header are discarded.
  if (currentExtension && !SAFE_GENERIC_EXTENSIONS.has(currentExtension)) {
    return safeDownloadFilename(
      name.slice(0, -(currentExtension.length + 1)),
      fallback,
    );
  }
  return name;
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

export function filenameFromDisposition(disposition, fallback, contentType = "") {
  const params = dispositionParameters(disposition);
  if (!params) return constrainFilenameExtension(fallback, fallback, contentType);
  if (params.has("filename*")) {
    const match = /^UTF-8'[^']*'(.+)$/i.exec(params.get("filename*"));
    if (!match) return constrainFilenameExtension(fallback, fallback, contentType);
    try {
      return constrainFilenameExtension(
        decodeURIComponent(match[1]),
        fallback,
        contentType,
      );
    } catch {
      // Invalid percent-encoding or UTF-8 never becomes a suggested name.
      return constrainFilenameExtension(fallback, fallback, contentType);
    }
  }
  return constrainFilenameExtension(
    params.get("filename") ?? "",
    fallback,
    contentType,
  );
}
