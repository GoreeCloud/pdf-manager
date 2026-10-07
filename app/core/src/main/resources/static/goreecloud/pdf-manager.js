import { glazeV170 } from "./glaze/js/glaze-v1.7.0.mjs";

const state = {
  files: [],
  category: "all",
  query: "",
  activeTool: null,
  busy: false,
};

const icon = (name) => {
  const paths = {
    merge: '<path d="M7 5h6a2 2 0 0 1 2 2v10"/><path d="M11 9H5a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/><path d="m14 10 3 3 3-3"/>',
    split: '<path d="M12 3v18"/><path d="M5 7h4M5 12h4M5 17h4M15 7h4M15 12h4M15 17h4"/>',
    rotate: '<path d="M4.5 9a8 8 0 1 1 .8 7.5"/><path d="M4 4v5h5"/>',
    compress: '<path d="M8 3H3v5M16 3h5v5M8 21H3v-5M16 21h5v-5"/><path d="m3 8 5-5M21 8l-5-5M3 16l5 5M21 16l-5 5"/>',
    image: '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="8" cy="9" r="1.5"/><path d="m5 17 4-4 3 3 2-2 5 5"/>',
    crop: '<path d="M6 3v15a3 3 0 0 0 3 3h12M3 6h15a3 3 0 0 1 3 3v12"/>',
    convert: '<path d="M7 7h11l-3-3M18 7l-3 3M17 17H6l3 3M6 17l3-3"/>',
    ocr: '<path d="M4 7V4h3M17 4h3v3M20 17v3h-3M7 20H4v-3"/><path d="M7 9h10M7 12h7M7 15h10"/>',
    shield: '<path d="M12 3 5 6v5c0 4.6 2.8 8.2 7 10 4.2-1.8 7-5.4 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',
    edit: '<path d="m4 20 4.2-1 9.9-9.9a2.1 2.1 0 0 0-3-3L5.2 16 4 20Z"/><path d="m13.8 7.4 2.8 2.8"/>',
    lock: '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    stamp: '<path d="M8 4h8l-1 7 3 3v2H6v-2l3-3-1-7Z"/><path d="M5 20h14"/>',
    automate: '<path d="M8 5H5v3M16 19h3v-3"/><path d="M5.5 8a7 7 0 0 1 11.7-2.8M18.5 16a7 7 0 0 1-11.7 2.8"/><path d="m10 9 5 3-5 3V9Z"/>',
    inspect: '<path d="M4 4h16v16H4z"/><path d="M8 8h8M8 12h8M8 16h5"/>',
  };
  return `<svg viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths.inspect}</svg>`;
};

const tools = [
  {
    id: "merge",
    name: "Merge PDFs",
    category: "organize",
    icon: "merge",
    ready: true,
    endpoint: "/api/v1/general/merge-pdfs",
    multi: true,
    description: "Combine PDFs and supported images in the order you choose.",
    fields: [
      { name: "sortType", label: "File order", type: "select", value: "orderProvided", options: [["orderProvided", "Workspace order"], ["byFileName", "File name"], ["byDateModified", "Modified date"], ["byDateCreated", "Created date"], ["byPDFTitle", "PDF title"]] },
      { name: "removeCertSign", label: "Remove certification signatures", type: "checkbox", value: true },
      { name: "generateToc", label: "Create bookmarks from filenames", type: "checkbox", value: false },
    ],
  },
  {
    id: "split",
    name: "Split PDF",
    category: "organize",
    icon: "split",
    ready: true,
    endpoint: "/api/v1/general/split-pages",
    description: "Split one PDF after selected pages, ranges, or every page.",
    fields: [
      { name: "pageNumbers", label: "Split after pages", type: "text", value: "all", help: "Examples: all, 2, 2,5, or 5-9." },
    ],
  },
  {
    id: "rotate",
    name: "Rotate pages",
    category: "organize",
    icon: "rotate",
    ready: true,
    endpoint: "/api/v1/general/rotate-pdf",
    description: "Rotate every page clockwise without rasterizing the document.",
    fields: [
      { name: "angle", label: "Angle", type: "select", value: "90", options: [["90", "90°"], ["180", "180°"], ["270", "270°"]] },
    ],
  },
  {
    id: "compress",
    name: "Optimize & compress",
    category: "optimize",
    icon: "compress",
    ready: true,
    endpoint: "/api/v1/misc/compress-pdf",
    description: "Reduce PDF size with controllable optimization and output goals.",
    fields: [
      { name: "optimizeLevel", label: "Optimization level", type: "select", value: "5", options: [["1", "1 — gentle"], ["3", "3"], ["5", "5 — balanced"], ["7", "7"], ["9", "9 — strongest"]] },
      { name: "expectedOutputSize", label: "Target size", type: "text", value: "25KB", help: "Examples: 500KB or 5MB. This is a target, not a guarantee." },
      { name: "linearize", label: "Optimize for web viewing", type: "checkbox", value: false },
      { name: "normalize", label: "Normalize document structure", type: "checkbox", value: false },
      { name: "grayscale", label: "Convert to grayscale", type: "checkbox", value: false },
    ],
  },
  {
    id: "extract-images",
    name: "Extract images",
    category: "convert",
    icon: "image",
    ready: true,
    endpoint: "/api/v1/misc/extract-images",
    description: "Extract unique embedded images into a downloadable archive.",
    fields: [
      { name: "format", label: "Image format", type: "select", value: "png", options: [["png", "PNG"], ["jpeg", "JPEG"], ["gif", "GIF"]] },
    ],
  },
  { id: "crop", name: "Crop pages", category: "edit", icon: "crop", description: "Adjust visible page boundaries and content framing." },
  {
    id: "rearrange",
    name: "Rearrange pages",
    category: "organize",
    icon: "merge",
    ready: true,
    endpoint: "/api/v1/general/rearrange-pages",
    description: "Reorder, reverse, duplicate, booklet-sort, or remove edge pages without rasterizing the document.",
    fields: [
      { name: "customMode", label: "Arrangement", type: "select", value: "CUSTOM", options: [["CUSTOM", "Custom page order"], ["REVERSE_ORDER", "Reverse all pages"], ["DUPLEX_SORT", "Duplex scan order"], ["BOOKLET_SORT", "Booklet order"], ["ODD_EVEN_SPLIT", "Odd pages then even pages"], ["DUPLICATE", "Duplicate each page"], ["REMOVE_FIRST", "Remove first page"], ["REMOVE_LAST", "Remove last page"], ["REMOVE_FIRST_AND_LAST", "Remove first and last pages"]] },
      { name: "pageNumbers", label: "Page order / duplicate count", type: "text", value: "all", help: "For Custom use values such as 3,1,2 or 1-4. Use all to preserve the current order. For Duplicate enter the number of copies." },
    ],
  },
  { id: "ocr", name: "OCR scanned PDFs", category: "convert", icon: "ocr", description: "Make scanned documents searchable with server-side OCR." },
  { id: "pdfa", name: "Convert to PDF/A", category: "convert", icon: "convert", description: "Prepare archival PDF/A output through the conversion API." },
  { id: "office", name: "Office conversion", category: "convert", icon: "convert", description: "Convert supported office formats where dependencies are available." },
  {
    id: "metadata",
    name: "Document metadata",
    category: "edit",
    icon: "inspect",
    ready: true,
    endpoint: "/api/v1/misc/update-metadata",
    description: "Update standard PDF metadata fields or deliberately remove all document metadata.",
    fields: [
      { name: "deleteAll", label: "Remove all metadata", type: "checkbox", value: false },
      { name: "title", label: "Title", type: "text", value: "" },
      { name: "author", label: "Author", type: "text", value: "" },
      { name: "subject", label: "Subject", type: "text", value: "" },
      { name: "keywords", label: "Keywords", type: "text", value: "" },
      { name: "creator", label: "Creator", type: "text", value: "" },
      { name: "producer", label: "Producer", type: "text", value: "" },
      { name: "trapped", label: "Trapped status", type: "select", value: "Unknown", options: [["Unknown", "Unknown"], ["False", "False"], ["True", "True"]] },
      { name: "creationDate", label: "Creation date", type: "text", value: "", help: "Optional. Format: yyyy/MM/dd HH:mm:ss" },
      { name: "modificationDate", label: "Modification date", type: "text", value: "", help: "Optional. Format: yyyy/MM/dd HH:mm:ss" },
    ],
  },
  {
    id: "page-numbers",
    name: "Page numbers",
    category: "edit",
    icon: "edit",
    ready: true,
    endpoint: "/api/v1/misc/add-page-numbers",
    description: "Add page numbers or Bates-style numbering with explicit page, position, type, and formatting controls.",
    fields: [
      { name: "pagesToNumber", label: "Pages to number", type: "text", value: "all", help: "Examples: all, 1,3-5,7" },
      { name: "startingNumber", label: "Starting number", type: "text", value: "1" },
      { name: "customText", label: "Text pattern", type: "text", value: "{n}", help: "Variables: {n}, {total}, {filename}" },
      { name: "zeroPad", label: "Zero-padding width", type: "text", value: "0", help: "Use 0 to disable Bates-style zero padding." },
      { name: "position", label: "Position", type: "select", value: "8", options: [["1", "Top left"], ["2", "Top center"], ["3", "Top right"], ["4", "Middle left"], ["5", "Middle center"], ["6", "Middle right"], ["7", "Bottom left"], ["8", "Bottom center"], ["9", "Bottom right"]] },
      { name: "customMargin", label: "Margin", type: "select", value: "medium", options: [["small", "Small"], ["medium", "Medium"], ["large", "Large"], ["x-large", "Extra large"]] },
      { name: "fontType", label: "Font", type: "select", value: "helvetica", options: [["helvetica", "Helvetica"], ["courier", "Courier"], ["times", "Times"]] },
      { name: "fontSize", label: "Font size", type: "text", value: "12" },
      { name: "fontColor", label: "Font color", type: "text", value: "#000000", help: "Hex color, for example #000000." },
    ],
  },
  {
    id: "stamp",
    name: "Text stamp & watermark",
    category: "edit",
    icon: "stamp",
    ready: true,
    endpoint: "/api/v1/misc/add-stamp",
    description: "Add a text stamp or watermark to selected pages with position, opacity, rotation, and color controls.",
    fields: [
      { name: "stampType", label: "Stamp type", type: "select", value: "text", options: [["text", "Text"]] },
      { name: "stampText", label: "Stamp text", type: "text", value: "GoreeCloud" },
      { name: "pageNumbers", label: "Pages", type: "text", value: "all", help: "Examples: all, 1,3-5,7" },
      { name: "alphabet", label: "Alphabet", type: "select", value: "roman", options: [["roman", "Roman"], ["arabic", "Arabic"], ["japanese", "Japanese"], ["korean", "Korean"], ["chinese", "Chinese"], ["thai", "Thai"]] },
      { name: "fontSize", label: "Size", type: "text", value: "40" },
      { name: "rotation", label: "Rotation", type: "text", value: "0", help: "Degrees." },
      { name: "opacity", label: "Opacity", type: "text", value: "0.5", help: "0.0 to 1.0." },
      { name: "position", label: "Position", type: "select", value: "8", options: [["1", "Bottom left"], ["2", "Bottom center"], ["3", "Bottom right"], ["4", "Middle left"], ["5", "Middle center"], ["6", "Middle right"], ["7", "Top left"], ["8", "Top center"], ["9", "Top right"]] },
      { name: "customMargin", label: "Margin", type: "select", value: "medium", options: [["small", "Small"], ["medium", "Medium"], ["large", "Large"], ["x-large", "Extra large"]] },
      { name: "customColor", label: "Color", type: "text", value: "#d3d3d3", help: "Hex color." },
      { name: "overrideX", label: "Override X", type: "text", value: "-1", help: "Leave -1 to use the selected grid position." },
      { name: "overrideY", label: "Override Y", type: "text", value: "-1", help: "Leave -1 to use the selected grid position." },
    ],
  },
  {
    id: "sanitize",
    name: "Sanitize PDF",
    category: "protect",
    icon: "shield",
    ready: true,
    endpoint: "/api/v1/security/sanitize-pdf",
    description: "Remove selected active or embedded PDF content through the retained security-processing boundary.",
    fields: [
      { name: "removeJavaScript", label: "Remove JavaScript actions", type: "checkbox", value: true },
      { name: "removeEmbeddedFiles", label: "Remove embedded files", type: "checkbox", value: true },
      { name: "removeXMPMetadata", label: "Remove XMP metadata", type: "checkbox", value: false },
      { name: "removeMetadata", label: "Remove document metadata", type: "checkbox", value: false },
      { name: "removeLinks", label: "Remove links", type: "checkbox", value: false },
      { name: "removeFonts", label: "Remove embedded fonts", type: "checkbox", value: false },
    ],
  },
  { id: "redact", name: "Redact content", category: "protect", icon: "shield", description: "Apply actual PDF redaction rather than visual-only masking." },
  {
    id: "add-password",
    name: "Add password",
    category: "protect",
    icon: "lock",
    ready: true,
    endpoint: "/api/v1/security/add-password",
    description: "Encrypt a PDF with an opening password, owner password, and optional permission restrictions.",
    fields: [
      { name: "password", label: "Open password", type: "password", value: "", autocomplete: "new-password" },
      { name: "ownerPassword", label: "Owner password", type: "password", value: "", autocomplete: "new-password" },
      { name: "keyLength", label: "Encryption key", type: "select", value: "256", options: [["256", "256-bit"], ["128", "128-bit"], ["40", "40-bit (legacy compatibility)"]] },
      { name: "preventAssembly", label: "Prevent document assembly", type: "checkbox", value: false },
      { name: "preventExtractContent", label: "Prevent content extraction", type: "checkbox", value: false },
      { name: "preventExtractForAccessibility", label: "Prevent accessibility extraction", type: "checkbox", value: false },
      { name: "preventFillInForm", label: "Prevent form filling", type: "checkbox", value: false },
      { name: "preventModify", label: "Prevent document modification", type: "checkbox", value: false },
      { name: "preventModifyAnnotations", label: "Prevent annotation modification", type: "checkbox", value: false },
      { name: "preventPrinting", label: "Prevent printing", type: "checkbox", value: false },
      { name: "preventPrintingFaithful", label: "Prevent faithful/high-quality printing", type: "checkbox", value: false },
    ],
  },
  {
    id: "remove-password",
    name: "Remove password",
    category: "protect",
    icon: "lock",
    ready: true,
    endpoint: "/api/v1/security/remove-password",
    description: "Remove PDF password protection when you know the current opening password.",
    fields: [
      { name: "password", label: "Current password", type: "password", value: "", autocomplete: "current-password" },
    ],
  },
  {
    id: "repair",
    name: "Repair PDF",
    category: "optimize",
    icon: "inspect",
    ready: true,
    endpoint: "/api/v1/misc/repair",
    description: "Attempt structural repair using the server's available Ghostscript, qpdf, or PDFBox path.",
    fields: [],
  },
  {
    id: "flatten",
    name: "Flatten PDF",
    category: "optimize",
    icon: "compress",
    ready: true,
    endpoint: "/api/v1/misc/flatten",
    description: "Flatten form fields or rasterize full pages for compatibility and unselectable output.",
    fields: [
      { name: "flattenOnlyForms", label: "Flatten form fields only", type: "checkbox", value: true },
      { name: "renderDpi", label: "Full-page render DPI", type: "text", value: "300", help: "Used only when full-page flattening is selected. Minimum 72 DPI; server maximum still applies." },
    ],
  },
  { id: "pipeline", name: "Automation pipelines", category: "automate", icon: "automate", description: "Compose repeatable multi-step document-processing workflows." },
];

const $ = (selector) => document.querySelector(selector);
const toolGrid = $("#toolGrid");
const fileInput = $("#fileInput");
const fileQueue = $("#fileQueue");
const clearFiles = $("#clearFiles");
const dropZone = $("#dropZone");
const dialog = $("#toolDialog");
const toolFields = $("#toolFields");
const toolForm = $("#toolForm");
const runTool = $("#runTool");
const toast = $("#toast");

function setTheme(theme) {
  if (theme === "system") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.dataset.theme = theme;
  localStorage.setItem("goreecloud-pdf-theme", theme);
}

function toggleTheme() {
  const current = document.documentElement.dataset.theme || "system";
  const prefersDark = matchMedia("(prefers-color-scheme: dark)").matches;
  const effectiveDark = current === "dark" || (current === "system" && prefersDark);
  setTheme(effectiveDark ? "light" : "dark");
}

function formatBytes(bytes) {
  const units = ["B", "KB", "MB", "GB"];
  let value = bytes;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value >= 10 || unit === 0 ? value.toFixed(0) : value.toFixed(1)} ${units[unit]}`;
}

function renderFiles() {
  clearFiles.disabled = state.files.length === 0;
  if (!state.files.length) {
    fileQueue.innerHTML = "";
    return;
  }
  fileQueue.innerHTML = state.files.map((file, index) => `
    <div class="file-row">
      <div>
        <div class="file-name">${escapeHtml(file.name)}</div>
        <div class="file-size">${formatBytes(file.size)}</div>
      </div>
      <div class="file-actions" aria-label="Actions for ${escapeHtml(file.name)}">
        <button class="glaze-icon-button" type="button" data-file-action="up" data-index="${index}" aria-label="Move ${escapeHtml(file.name)} up" ${index === 0 ? "disabled" : ""}>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 14 5-5 5 5"/></svg>
        </button>
        <button class="glaze-icon-button" type="button" data-file-action="down" data-index="${index}" aria-label="Move ${escapeHtml(file.name)} down" ${index === state.files.length - 1 ? "disabled" : ""}>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 10 5 5 5-5"/></svg>
        </button>
        <button class="glaze-icon-button" type="button" data-file-action="remove" data-index="${index}" aria-label="Remove ${escapeHtml(file.name)}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>
        </button>
      </div>
    </div>
  `).join("");
}

function addFiles(incoming) {
  const next = [...state.files];
  for (const file of incoming) {
    const duplicate = next.some((item) => item.name === file.name && item.size === file.size && item.lastModified === file.lastModified);
    if (!duplicate) next.push(file);
  }
  state.files = next;
  renderFiles();
}

function renderTools() {
  const query = state.query.trim().toLowerCase();
  const filtered = tools.filter((tool) => {
    const categoryMatch = state.category === "all" || tool.category === state.category;
    const queryMatch = !query || `${tool.name} ${tool.description} ${tool.category}`.toLowerCase().includes(query);
    return categoryMatch && queryMatch;
  });

  if (!filtered.length) {
    toolGrid.innerHTML = '<div class="empty-state">No tools match this view.</div>';
    return;
  }

  toolGrid.innerHTML = filtered.map((tool) => `
    <button class="tool-card" type="button" data-tool="${tool.id}" data-ready="${tool.ready === true}">
      <span>
        <span class="tool-card-top">
          <span class="tool-icon">${icon(tool.icon)}</span>
          <span class="tool-kind">${tool.ready ? "Workbench ready" : "API available"}</span>
        </span>
        <h3>${tool.name}</h3>
        <p>${tool.description}</p>
      </span>
    </button>
  `).join("");
}

function fieldMarkup(field) {
  const id = `field-${field.name}`;
  if (field.type === "checkbox") {
    return `<label class="check-field" for="${id}"><input id="${id}" name="${field.name}" type="checkbox" ${field.value ? "checked" : ""}><span>${field.label}</span></label>`;
  }
  if (field.type === "select") {
    return `<div class="field"><label for="${id}">${field.label}</label><select class="glaze-select" id="${id}" name="${field.name}">${field.options.map(([value, label]) => `<option value="${value}" ${String(value) === String(field.value) ? "selected" : ""}>${label}</option>`).join("")}</select>${field.help ? `<small>${field.help}</small>` : ""}</div>`;
  }
  const inputType = field.type === "password" ? "password" : "text";
  const autocomplete = field.autocomplete ? ` autocomplete="${field.autocomplete}"` : "";
  return `<div class="field"><label for="${id}">${field.label}</label><input class="glaze-input" id="${id}" name="${field.name}" type="${inputType}" value="${escapeHtml(String(field.value ?? ""))}"${autocomplete}>${field.help ? `<small>${field.help}</small>` : ""}</div>`;
}

function openTool(tool) {
  state.activeTool = tool;
  $("#toolDialogCategory").textContent = tool.category;
  $("#toolDialogTitle").textContent = tool.name;
  $("#toolDialogDescription").textContent = tool.description;

  if (tool.ready) {
    toolFields.innerHTML = `
      <div class="field">
        <label>Input</label>
        <small>${tool.multi ? "Uses all files in the workspace, in the order shown." : "Uses the first file in the workspace."}</small>
      </div>
      ${(tool.fields || []).map(fieldMarkup).join("")}
    `;
    runTool.hidden = false;
    runTool.disabled = false;
    runTool.textContent = "Run tool";
  } else {
    toolFields.innerHTML = '<div class="empty-state">This capability is present in the retained processing API. A dedicated Glaze workflow is planned; use API details for the current interface.</div>';
    runTool.hidden = true;
  }

  dialog.showModal();
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[character]);
}

function showToast(message, type = "success") {
  toast.textContent = message;
  toast.dataset.state = type;
  toast.hidden = false;
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => { toast.hidden = true; }, 5000);
}

function buildFormData(tool) {
  if (!state.files.length) throw new Error("Add at least one document to the workspace first.");
  const data = new FormData();
  const files = tool.multi ? state.files : [state.files[0]];
  for (const file of files) data.append("fileInput", file, file.name);

  const form = new FormData(toolForm);
  for (const field of tool.fields || []) {
    if (field.type === "checkbox") data.append(field.name, form.has(field.name) ? "true" : "false");
    else {
      const value = form.get(field.name);
      if (value !== null && String(value).length) data.append(field.name, String(value));
    }
  }
  if (tool.id === "merge") data.append("fileOrder", state.files.map((file) => file.name).join("\n"));
  if (tool.id === "page-numbers") data.append("pageNumbers", String(form.get("pagesToNumber") || "all"));
  return data;
}

function filenameFromResponse(response, fallback) {
  const disposition = response.headers.get("content-disposition") || "";
  const encoded = disposition.match(/filename\*=UTF-8''([^;]+)/i);
  if (encoded) {
    try { return decodeURIComponent(encoded[1]); }
    catch { return encoded[1]; }
  }
  const plain = disposition.match(/filename="?([^";]+)"?/i);
  return plain?.[1] || fallback;
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function executeTool(tool) {
  if (state.busy) return;
  const original = runTool.textContent;
  state.busy = true;
  runTool.disabled = true;
  runTool.textContent = "Processing…";
  document.documentElement.dataset.processing = "true";

  try {
    const response = await fetch(tool.endpoint, {
      method: "POST",
      body: buildFormData(tool),
      credentials: "same-origin",
      headers: { "X-GoreeCloud-Client": "pdf-manager-glaze-v1" },
    });

    if (!response.ok) {
      const contentType = response.headers.get("content-type") || "";
      const detail = contentType.includes("json") ? JSON.stringify(await response.json()) : await response.text();
      throw new Error(detail || `Request failed with status ${response.status}.`);
    }

    const blob = await response.blob();
    downloadBlob(blob, filenameFromResponse(response, `${tool.id}-result`));
    showToast(`${tool.name} completed. The result is ready.`);
    dialog.close();
  } catch (error) {
    console.error(error);
    showToast(error instanceof Error ? error.message : "The PDF operation could not be completed.", "error");
  } finally {
    state.busy = false;
    runTool.disabled = false;
    runTool.textContent = original;
    delete document.documentElement.dataset.processing;
  }
}

async function checkService() {
  const status = $("#serviceState");
  const detail = $("#serviceDetail");
  try {
    const response = await fetch("/api/v1/info/status", { credentials: "same-origin", cache: "no-store" });
    if (!response.ok) throw new Error(String(response.status));
    status.textContent = "Available";
    detail.textContent = "The PDF processing service responded successfully.";
  } catch {
    status.textContent = "Unavailable";
    detail.textContent = "The interface loaded, but the status endpoint did not confirm service readiness.";
  }
}

$("#themeToggle").addEventListener("click", toggleTheme);
setTheme(localStorage.getItem("goreecloud-pdf-theme") || "system");

fileInput.addEventListener("change", () => {
  addFiles([...fileInput.files]);
  fileInput.value = "";
});

clearFiles.addEventListener("click", () => {
  state.files = [];
  renderFiles();
});

fileQueue.addEventListener("click", (event) => {
  const button = event.target.closest("[data-file-action]");
  if (!button) return;
  const index = Number(button.dataset.index);
  if (button.dataset.fileAction === "remove") state.files.splice(index, 1);
  else if (button.dataset.fileAction === "up" && index > 0) [state.files[index - 1], state.files[index]] = [state.files[index], state.files[index - 1]];
  else if (button.dataset.fileAction === "down" && index < state.files.length - 1) [state.files[index + 1], state.files[index]] = [state.files[index], state.files[index + 1]];
  renderFiles();
});

for (const type of ["dragenter", "dragover"]) {
  dropZone.addEventListener(type, (event) => {
    event.preventDefault();
    dropZone.dataset.dragging = "true";
  });
}
for (const type of ["dragleave", "drop"]) {
  dropZone.addEventListener(type, (event) => {
    event.preventDefault();
    dropZone.dataset.dragging = "false";
  });
}
dropZone.addEventListener("drop", (event) => addFiles([...event.dataTransfer.files]));

$("#categoryNav").addEventListener("click", (event) => {
  const button = event.target.closest("[data-category]");
  if (!button) return;
  state.category = button.dataset.category;
  document.querySelectorAll("[data-category]").forEach((item) => item.removeAttribute("aria-current"));
  button.setAttribute("aria-current", "page");
  renderTools();
});

$("#toolSearch").addEventListener("input", (event) => {
  state.query = event.target.value;
  renderTools();
});

toolGrid.addEventListener("click", (event) => {
  const card = event.target.closest("[data-tool]");
  if (!card) return;
  const tool = tools.find((item) => item.id === card.dataset.tool);
  if (tool) openTool(tool);
});

toolForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (state.activeTool?.ready) await executeTool(state.activeTool);
});

dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});

if (glazeV170.version !== "1.7.0" || glazeV170.consumerEligible !== true) {
  console.warn("Unexpected Glaze runtime identity.", glazeV170);
}

renderFiles();
renderTools();
checkService();
