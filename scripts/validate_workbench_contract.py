#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "app/core/src/main/resources/static/goreecloud/pdf-manager.js"

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
}

TOOLS = {
    "merge": ("general", "/merge-pdfs", "app/core/src/main/java/stirling/software/SPDF/controller/api/MergeController.java"),
    "split": ("general", "/split-pages", "app/core/src/main/java/stirling/software/SPDF/controller/api/SplitPDFController.java"),
    "rotate": ("general", "/rotate-pdf", "app/core/src/main/java/stirling/software/SPDF/controller/api/RotationController.java"),
    "compress": ("misc", "/compress-pdf", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/CompressController.java"),
    "extract-images": ("misc", "/extract-images", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/ExtractImagesController.java"),
    "rearrange": ("general", "/rearrange-pages", "app/core/src/main/java/stirling/software/SPDF/controller/api/RearrangePagesPDFController.java"),
    "metadata": ("misc", "/update-metadata", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/MetadataController.java"),
    "page-numbers": ("misc", "/add-page-numbers", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/PageNumbersController.java"),
    "stamp": ("misc", "/add-stamp", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/StampController.java"),
    "sanitize": ("security", "/sanitize-pdf", "app/core/src/main/java/stirling/software/SPDF/controller/api/security/SanitizeController.java"),
    "add-password": ("security", "/add-password", "app/core/src/main/java/stirling/software/SPDF/controller/api/security/PasswordController.java"),
    "remove-password": ("security", "/remove-password", "app/core/src/main/java/stirling/software/SPDF/controller/api/security/PasswordController.java"),
    "repair": ("misc", "/repair", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/RepairController.java"),
    "flatten": ("misc", "/flatten", "app/core/src/main/java/stirling/software/SPDF/controller/api/misc/FlattenController.java"),
}


def fail(message: str) -> None:
    raise SystemExit(f"workbench-contract: {message}")


for family, (path, expected) in BASES.items():
    text = path.read_text(encoding="utf-8")
    if expected not in text:
        fail(f"{family} API annotation does not expose expected base {expected}")

js = JS.read_text(encoding="utf-8")

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

for tool_id, (family, route, controller_rel) in TOOLS.items():
    controller = ROOT / controller_rel
    controller_text = controller.read_text(encoding="utf-8")
    if route not in controller_text:
        fail(f"{tool_id} route {route} is not present in {controller_rel}")

    endpoint = BASES[family][1] + route
    block = tool_blocks.get(tool_id, "")
    if f'endpoint: "{endpoint}"' not in block:
        fail(f"{tool_id} is not wired to {endpoint}")

if 'tool.id === "page-numbers"' not in js or 'data.append("pageNumbers"' not in js:
    fail("page-numbers must supply inherited PDFWithPageNums.pageNumbers")

if 'type: "password"' not in js:
    fail("password workflows must use password-type input definitions")

print(f"workbench-contract: PASS ({len(TOOLS)} ready workflows)")
