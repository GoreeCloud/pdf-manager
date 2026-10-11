import test from "node:test";
import assert from "node:assert/strict";
import {
  filenameFromDisposition,
  safeDownloadFilename,
} from "../app/core/src/main/resources/static/goreecloud/download-filename.mjs";

test("plain and RFC 5987 UTF-8 filenames remain usable", () => {
  assert.equal(filenameFromDisposition('attachment; filename="notes.pdf"', "fallback.pdf"), "notes.pdf");
  assert.equal(
    filenameFromDisposition("attachment; filename*=UTF-8''caf%C3%A9%20scan.pdf", "fallback.pdf"),
    "café scan.pdf",
  );
  assert.equal(
    filenameFromDisposition('attachment; filename="semi;colon.pdf"', "fallback.pdf"),
    "semi;colon.pdf",
  );
});

test("path-like response names cannot supply directory segments", () => {
  assert.equal(filenameFromDisposition('attachment; filename="../../home/report.pdf"', "safe.pdf"), "report.pdf");
  assert.equal(
    filenameFromDisposition("attachment; filename*=UTF-8''..%5C..%5Cinvoice.pdf", "safe.pdf"),
    "invoice.pdf",
  );
});

test("control and bidi override characters are stripped from file labels", () => {
  assert.equal(safeDownloadFilename("report\r\n2026.pdf"), "report2026.pdf");
  assert.equal(safeDownloadFilename("invoice\u202Efdp.exe"), "invoicefdp.exe");
  assert.equal(safeDownloadFilename("safe\u0000name.pdf"), "safename.pdf");
});

test("empty and malformed extended names fall back safely", () => {
  assert.equal(filenameFromDisposition(null, "../safe.pdf"), "safe.pdf");
  assert.equal(filenameFromDisposition("attachment; filename*=UTF-8''%ZZ", "../safe.pdf"), "safe.pdf");
  assert.equal(filenameFromDisposition('attachment; filename=".."', "safe.pdf"), "safe.pdf");
  assert.equal(safeDownloadFilename(".", "."), "download");
});

test("hostile platform names and punctuation become ordinary safe labels", () => {
  assert.equal(safeDownloadFilename("CON.pdf"), "file-CON.pdf");
  assert.equal(safeDownloadFilename("report:final?.pdf"), "report_final_.pdf");
  assert.equal(safeDownloadFilename("   "), "download");
});

test("long response names remain bounded while preserving short extension", () => {
  const result = safeDownloadFilename("x".repeat(260) + ".pdf");
  assert.equal(result.length, 180);
  assert.ok(result.endsWith(".pdf"));
  assert.equal(safeDownloadFilename("x".repeat(260)).length, 180);
});
