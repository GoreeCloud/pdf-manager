import test from "node:test";
import assert from "node:assert/strict";
import { filenameFromDisposition } from "../app/core/src/main/resources/static/goreecloud/download-filename.mjs";

test("known media type overrides a conflicting response suffix", () => {
  assert.equal(
    filenameFromDisposition('attachment; filename="archive.zip"', "result", "application/pdf"),
    "archive.pdf",
  );
});

test("known media type supplies a suffix when the header is absent", () => {
  assert.equal(
    filenameFromDisposition(null, "result", "application/zip"),
    "result.zip",
  );
});

test("generic binary keeps an approved document suffix", () => {
  assert.equal(
    filenameFromDisposition('attachment; filename="document.docx"', "result", "application/octet-stream"),
    "document.docx",
  );
});

test("generic binary discards an unapproved suffix", () => {
  assert.equal(
    filenameFromDisposition('attachment; filename="document.unknown"', "result", "application/octet-stream"),
    "document",
  );
});
