import { MantineProvider } from "@mantine/core";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import Footer from "@editor/components/shared/Footer";
import LegalSection from "@editor/components/shared/config/configSections/LegalSection";

vi.mock("@editor/hooks/useFooterInfo", () => ({
  useFooterInfo: () => ({ footerInfo: undefined }),
}));
vi.mock("@editor/hooks/useCookieConsent", () => ({
  useCookieConsent: () => ({ showCookiePreferences: vi.fn() }),
}));
vi.mock("@editor/contexts/AppConfigContext", () => ({
  useAppConfig: () => ({ config: { enableAnalytics: false } }),
}));

describe("GoreeCloud legal policy surfaces", () => {
  it("does not show fabricated legal policies or upstream support links in the footer", () => {
    const { container } = render(
      <MantineProvider env="test">
        <Footer />
      </MantineProvider>,
    );
    const hrefs = [...container.querySelectorAll("a")].map((a) => a.href);
    expect(hrefs).toEqual(["https://github.com/GoreeCloud/pdf-manager/issues"]);
    expect(hrefs.every((url) => !url.includes("stirling.com"))).toBe(true);
  });

  it("shows only explicitly configured secure policy URLs", () => {
    const { container } = render(
      <MantineProvider env="test">
        <Footer
          privacyPolicy="https://example.com/privacy"
          termsAndConditions="javascript:alert(1)"
          accessibilityStatement="/accessibility"
        />
      </MantineProvider>,
    );
    const hrefs = [...container.querySelectorAll("a")].map((a) => a.getAttribute("href"));
    expect(hrefs).toContain("https://example.com/privacy");
    expect(hrefs).toContain("/accessibility");
    expect(hrefs).not.toContain("javascript:alert(1)");
    expect(hrefs).not.toContain("https://www.stirling.com/terms");
  });

  it("shows an unconfigured-policy notice rather than upstream links in settings", () => {
    const { container } = render(
      <MantineProvider env="test">
        <LegalSection />
      </MantineProvider>,
    );
    expect(container.querySelector("a")).toBeNull();
    expect(screen.getByText("settings.legal.documents.unconfigured")).toBeTruthy();
  });
});
