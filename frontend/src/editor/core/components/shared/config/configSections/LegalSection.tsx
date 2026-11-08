import React from "react";
import { Anchor, Group, Paper, Stack, Text } from "@mantine/core";
import { Button } from "@editor/ui/Button";
import { useTranslation } from "react-i18next";
import { Icon } from "@editor/ui/Icon";
import { useAppConfig } from "@editor/contexts/AppConfigContext";
import { useFooterInfo } from "@editor/hooks/useFooterInfo";
import { useCookieConsent } from "@editor/hooks/useCookieConsent";
import { serviceLegalHref } from "@editor/utils/serviceLegalHref";

interface LegalLink {
  key: string;
  label: string;
  href: string;
}

const LegalSection: React.FC = () => {
  const { t } = useTranslation();
  const { config } = useAppConfig();
  const { footerInfo } = useFooterInfo();

  const analyticsEnabled =
    config?.enableAnalytics ?? footerInfo?.analyticsEnabled ?? false;
  const privacyPolicy = config?.privacyPolicy ?? footerInfo?.privacyPolicy;
  const termsAndConditions =
    config?.termsAndConditions ?? footerInfo?.termsAndConditions;
  const accessibilityStatement =
    config?.accessibilityStatement ?? footerInfo?.accessibilityStatement;
  const cookiePolicy = config?.cookiePolicy ?? footerInfo?.cookiePolicy;
  const impressum = config?.impressum ?? footerInfo?.impressum;

  const { showCookiePreferences } = useCookieConsent();

  // Do not silently fall back to the original publisher's legal policies.
  const privacyUrl = serviceLegalHref(privacyPolicy);
  const termsUrl = serviceLegalHref(termsAndConditions);
  const accessibilityUrl = serviceLegalHref(accessibilityStatement);
  const cookieUrl = serviceLegalHref(cookiePolicy);
  const imprintUrl = serviceLegalHref(impressum);

  const legalLinks: LegalLink[] = [
    ...(privacyUrl
      ? [{ key: "privacy", label: t("legal.privacy", "Privacy Policy"), href: privacyUrl }]
      : []),
    ...(termsUrl
      ? [{ key: "terms", label: t("legal.terms", "Terms and Conditions"), href: termsUrl }]
      : []),
    ...(accessibilityUrl
      ? [{ key: "accessibility", label: t("legal.accessibility", "Accessibility"), href: accessibilityUrl }]
      : []),
    ...(cookieUrl
      ? [{ key: "cookie", label: t("legal.cookie", "Cookie Policy"), href: cookieUrl }]
      : []),
    ...(imprintUrl
      ? [{ key: "impressum", label: t("legal.impressum", "Impressum"), href: imprintUrl }]
      : []),
  ];

  const renderLink = (link: LegalLink) => (
    <Anchor
      key={link.key}
      href={link.href}
      target="_blank"
      rel="noopener noreferrer"
      size="sm"
    >
      <Group gap={6} wrap="nowrap">
        {link.label}
        <Icon name="external-link" size="0.9rem" />
      </Group>
    </Anchor>
  );

  return (
    <Stack gap="lg">
      <Paper withBorder p="md" radius="md">
        <Stack gap="md">
          <div>
            <Text fw={600} size="sm">
              {t("settings.legal.documents.title", "Legal Documents")}
            </Text>
            <Text size="xs" c="dimmed" mt={4}>
              {t(
                "settings.legal.documents.description",
                "Policies and legal information for this service.",
              )}
            </Text>
          </div>
          <Stack gap="sm">
            {legalLinks.length > 0 ? (
              legalLinks.map(renderLink)
            ) : (
              <Text size="xs" c="dimmed">
                {t(
                  "settings.legal.documents.unconfigured",
                  "No service legal policy links have been configured for this development preview.",
                )}
              </Text>
            )}
          </Stack>
        </Stack>
      </Paper>

      {analyticsEnabled === true && (
        <Paper withBorder p="md" radius="md">
          <Group justify="space-between" align="center">
            <div>
              <Text fw={600} size="sm">
                {t("legal.showCookieBanner", "Cookie Preferences")}
              </Text>
              <Text size="xs" c="dimmed" mt={4}>
                {t(
                  "settings.legal.cookiePreferences.description",
                  "Review or change your cookie consent choices.",
                )}
              </Text>
            </div>
            <Button
              variant="secondary"
              size="sm"
              id="cookieBanner"
              onClick={showCookiePreferences}
            >
              {t("settings.legal.cookiePreferences.manage", "Manage")}
            </Button>
          </Group>
        </Paper>
      )}
    </Stack>
  );
};

export default LegalSection;
