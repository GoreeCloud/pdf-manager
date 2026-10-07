#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "app/core/src/main/resources/static/goreecloud/pdf-manager.js"
CONFIG_CONTROLLER = ROOT / "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/ConfigController.java"

BASES = {
    "general": (
        ROOT / "app/common/src/main/java/stirling/software/common/annotations/api/GeneralApi.java",
        "/api/v1/general",
    ),
    "misc": (
        ROOT / "app/common/src/main/java/stirling/software/common/annotations/api/MiscApi.java",
        "/api/v1/misc",
    ),
    "security": (
        ROOT / "app/common/src/main/java/stirling/software/common/annotations/api/SecurityApi.java",
        "/api/v1/security",
    ),
    "convert": (
        ROOT / "app/common/src/main/java/stirling/software/common/annotations/api/ConvertApi.java",
        "/api/v1/convert",
    ),
}

# tool id -> (API family, controller route, controller source, availability key)
TOOLS = {
    "merge": ("general", "/merge-pdfs", "app/core/src/main/java/stirling/software/SPDF/controller/api/MergeController.java", "merge-pdfs"),
    "split": ("general", "/split-pages", "app/core/src/main/java/stirling/software/SPDF/controller/api/SplitPDFController.java", "split-pages"),
    "rotate": ("general", "/rotate-pdf", "app/core/src/main/java/stirling/software/SPDF/controller/api/RotationController.java", "rotate-pdf"),
    "compress": ("misc", "/compress-pdf", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/CompressController.java", "compress-pdf"),
    "extract-images": ("misc", "/extract-images", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/ExtractImagesController.java", "extract-images"),
    "crop": ("general", "/crop", "app/core/src/main/java/stirling/software/SPDF/controller/api/CropController.java", "crop"),
    "rearrange": ("general", "/rearrange-pages", "app/core/src/main/java/stirling/software/SPDF/controller/api/RearrangePagesPDFController.java", "rearrange-pages"),
    "ocr": ("misc", "/ocr-pdf", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/OCRController.java", "ocr-pdf"),
    "pdfa": ("convert", "/pdf/pdfa", "app/core/src/main/java/stirling/software/SPDF/controller/api/converters/ConvertPDFToPDFA.java", "pdf-to-pdfa"),
    "metadata": ("misc", "/update-metadata", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/MetadataController.java", "update-metadata"),
    "page-numbers": ("misc", "/add-page-numbers", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/PageNumbersController.java", "add-page-numbers"),
    "stamp": ("misc", "/add-stamp", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/StampController.java", "add-stamp"),
    "sanitize": ("security", "/sanitize-pdf", "app/core/src/main/java/stirling/software/SPDF/controller/api/security/SanitizeController.java", "sanitize-pdf"),
    "redact": ("security", "/auto-redact", "app/core/src/main/java/stirling/software/SPDF/controller/api/security/RedactController.java", "auto-redact"),
    "add-password": ("security", "/add-password", "app/core/src/main/java/stirling/software/SPDF/controller/api/security/PasswordController.java", "add-password"),
    "remove-password": ("security", "/remove-password", "app/core/src/main/java/stirling/software/SPDF/controller/api/security/PasswordController.java", "remove-password"),
    "repair": ("misc", "/repair", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/RepairController.java", "repair"),
    "flatten": ("misc", "/flatten", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/FlattenController.java", "flatten"),
}


def fail(message: str) -> None:
    raise SystemExit(f"workbench-contract: {message}")


for family, (path, expected) in BASES.items():
    text = path.read_text(encoding="utf-8")
    if expected not in text:
        fail(f"{family} API annotation does not expose expected base {expected}")

config_text = CONFIG_CONTROLLER.read_text(encoding="utf-8")
if '@GetMapping("/endpoints-availability")' not in config_text:
    fail("server-authoritative endpoint availability API is missing")

js = JS.read_text(encoding="utf-8")
if "/api/v1/config/endpoints-availability" not in js:
    fail("workbench does not consume server-authoritative endpoint availability")

if 'state.activeTool.available === true' in js:
    fail("submit gating must not depend on deprecated per-tool availability state")
if 'availabilityState(state.activeTool) === "enabled"' not in js:
    fail("submit gating must use the unified server-authoritative availability state")

tool_blocks: dict[str, str] = {}
for match in re.finditer(r"(?ms)^  \{\n(.*?)^  \},?$", js):
    block = match.group(1)
    id_match = re.search(r'id:\s*"([^"]+)"', block)
    if id_match:
        tool_blocks[id_match.group(1)] = block

ready_ids = {
    tool_id
    for tool_id, block in tool_blocks.items()
    if re.search(r"^    ready:\s*true,", block, flags=re.MULTILINE)
}
expected_ids = set(TOOLS)

missing_ready = sorted(expected_ids - ready_ids)
if missing_ready:
    fail(f"expected workbench-ready tools are not marked ready: {', '.join(missing_ready)}")

unexpected_ready = sorted(ready_ids - expected_ids)
if unexpected_ready:
    fail(
        "new ready tools must be added to the backend contract map: "
        + ", ".join(unexpected_ready)
    )

for tool_id, (family, route, controller_rel, availability_key) in TOOLS.items():
    controller = ROOT / controller_rel
    controller_text = controller.read_text(encoding="utf-8")
    if route not in controller_text:
        fail(f"{tool_id} route {route} is not present in {controller_rel}")

    endpoint = BASES[family][1] + route
    block = tool_blocks.get(tool_id, "")
    if f'endpoint: "{endpoint}"' not in block:
        fail(f"{tool_id} is not wired to {endpoint}")

    availability_pattern = re.compile(
        rf'(?m)^\s*(?:"{re.escape(tool_id)}"|{re.escape(tool_id)}):\s*"{re.escape(availability_key)}",'
    )
    if not availability_pattern.search(js):
        fail(f"{tool_id} is not mapped to availability key {availability_key}")

if 'tool.id === "page-numbers"' not in js or 'data.append("pageNumbers"' not in js:
    fail("page-numbers must supply inherited PDFWithPageNums.pageNumbers")

if 'type: "password"' not in js:
    fail("password workflows must use password-type input definitions")

crop_block = tool_blocks.get("crop", "")
for marker in ('name: "autoCrop"', 'name: "x"', 'name: "y"', 'name: "width"', 'name: "height"'):
    if marker not in crop_block:
        fail(f"crop workflow must expose backend crop control {marker}")

ocr_block = tool_blocks.get("ocr", "")
if 'name: "languages"' not in ocr_block or "repeatValues: true" not in ocr_block:
    fail("OCR workflow must support repeated multipart language values")
if "data.append(field.name, item)" not in js:
    fail("OCR repeated language values must be appended individually")

pdfa_block = tool_blocks.get("pdfa", "")
if "pdfa-1a" in pdfa_block or "pdfa-2a" in pdfa_block or "pdfa-3a" in pdfa_block or "pdfUa" in pdfa_block:
    fail("core-only PDF/A workflow must not advertise unavailable level-A/PDF-UA tagging")

redact_block = tool_blocks.get("redact", "")
if 'type: "textarea"' not in redact_block or 'wholeWordSearch' not in redact_block:
    fail("text redaction workflow must expose explicit pattern and match controls")

print(f"workbench-contract: PASS ({len(TOOLS)} ready workflows, server-authoritative availability)")
