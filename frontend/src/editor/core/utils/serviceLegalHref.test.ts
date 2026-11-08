import { describe, expect, it } from "vitest";
import { serviceLegalHref } from "./serviceLegalHref";

describe("serviceLegalHref - development preview legal links", () => {
  it("does not invent a link when no policy is configured", () => {
    expect(serviceLegalHref(undefined)).toBeUndefined();
    expect(serviceLegalHref(null)).toBeUndefined();
    expect(serviceLegalHref("")).toBeUndefined();
    expect(serviceLegalHref("   ")).toBeUndefined();
  });

  it("accepts explicitly configured HTTPS and local file paths", () => {
    expect(serviceLegalHref(" https://example.com/legal/terms ")).toBe(
      "https://example.com/legal/terms",
    );
    expect(serviceLegalHref("/legal/privacy")).toBe("/legal/privacy");
    expect(serviceLegalHref("custom-policy.html")).toBe("custom-policy.html");
  });

  it("rejects untrusted script/data/file protocols and credential-bearing URLs", () => {
    for (const candidate of [
      "javascript:alert(1)",
      "data:text/html,policy",
      "file:///tmp/policy.html",
      "http://example.com/terms",
      "https://user:secret@example.com/terms",
      "//example.com/terms",
      "../policy.html",
      "policy.html\\evil",
      "https://example.com/terms\n",
    ]) {
      expect(serviceLegalHref(candidate)).toBeUndefined();
    }
  });

  it("does not confuse arbitrary text or malformed URLs with legal links", () => {
    expect(serviceLegalHref("policy text with spaces")).toBeUndefined();
    expect(serviceLegalHref("https://")).toBeUndefined();
    expect(serviceLegalHref("mailto:support@example.com")).toBeUndefined();
  });
});
