import { Flex } from "@mantine/core";
import { useTranslation } from "react-i18next";
import { useCookieConsent } from "@editor/hooks/useCookieConsent";
import { useFooterInfo } from "@editor/hooks/useFooterInfo";
import { Button } from "@editor/ui/Button";
import { serviceLegalHref } from "@editor/utils/serviceLegalHref";

interface FooterProps {
  privacyPolicy?: string;
  termsAndConditions?: string;
  accessibilityStatement?: string;
  cookiePolicy?: string;
  impressum?: string;
  analyticsEnabled?: boolean;
}

export default function Footer({
  privacyPolicy,
  termsAndConditions,
  accessibilityStatement,
  cookiePolicy,
  impressum,
  analyticsEnabled,
}: FooterProps) {
  const { t } = useTranslation();
  const { footerInfo } = useFooterInfo();

  // Use props if provided, otherwise fall back to fetched footer info
  const finalAnalyticsEnabled =
    analyticsEnabled ?? footerInfo?.analyticsEnabled ?? false;
  const finalPrivacyPolicy = privacyPolicy ?? footerInfo?.privacyPolicy;
  const finalTermsAndConditions =
    termsAndConditions ?? footerInfo?.termsAndConditions;
  const finalAccessibilityStatement =
    accessibilityStatement ?? footerInfo?.accessibilityStatement;
  const finalCookiePolicy = cookiePolicy ?? footerInfo?.cookiePolicy;
  const finalImpressum = impressum ?? footerInfo?.impressum;

  const { showCookiePreferences } = useCookieConsent();

  // Do not represent the upstream publisher's policies as GoreeCloud's.
  const finalPrivacyUrl = serviceLegalHref(finalPrivacyPolicy);
  const finalTermsUrl = serviceLegalHref(finalTermsAndConditions);
  const finalAccessibilityUrl = serviceLegalHref(finalAccessibilityStatement);
  const finalCookieUrl = serviceLegalHref(finalCookiePolicy);
  const finalImprintUrl = serviceLegalHref(finalImpressum);

  return (
    <div
      style={{
        height: "var(--footer-height)",
        backgroundColor: "var(--c-surface)",
        borderTop: "1px solid var(--c-border-subtle)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      <Flex
        gap="md"
        justify="center"
        align="center"
        direction="row"
        style={{
          fontSize: "0.75rem",
        }}
      >
        {finalPrivacyUrl && (
          <a className="footer-link px-3" target="_blank"
            rel="noopener noreferrer" href={finalPrivacyUrl}>
            {t("legal.privacy", "Privacy Policy")}
          </a>
        )}
        {finalTermsUrl && (
          <a className="footer-link px-3" target="_blank"
            rel="noopener noreferrer" href={finalTermsUrl}>
            {t("legal.terms", "Terms and Conditions")}
          </a>
        )}
        <a className="footer-link px-3" target="_blank"
          rel="noopener noreferrer"
          href="https://github.com/GoreeCloud/pdf-manager/issues">
          {t("footer.issues", "GitHub")}
        </a>
        {finalAccessibilityUrl && (
          <a
            className="footer-link px-3"
            target="_blank"
            rel="noopener noreferrer"
            href={finalAccessibilityUrl}
          >
            {t("legal.accessibility", "Accessibility")}
          </a>
        )}
        {finalCookieUrl && (
          <a
            className="footer-link px-3"
            target="_blank"
            rel="noopener noreferrer"
            href={finalCookieUrl}
          >
            {t("legal.cookie", "Cookie Policy")}
          </a>
        )}
        {finalImprintUrl && (
          <a
            className="footer-link px-3"
            target="_blank"
            rel="noopener noreferrer"
            href={finalImprintUrl}
          >
            {t("legal.impressum", "Impressum")}
          </a>
        )}
        {finalAnalyticsEnabled && (
          <Button
            variant="tertiary"
            className="footer-link px-3"
            id="cookieBanner"
            onClick={showCookiePreferences}
          >
            {t("legal.showCookieBanner", "Cookie Preferences")}
          </Button>
        )}
      </Flex>
    </div>
  );
}
