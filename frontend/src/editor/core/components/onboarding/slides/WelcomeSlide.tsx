import React from "react";
import { useTranslation, Trans } from "react-i18next";
import { SlideConfig } from "@editor/types/types";
import styles from "@editor/components/onboarding/InitialOnboardingModal/InitialOnboardingModal.module.css";
import { UNIFIED_CIRCLE_CONFIG } from "@editor/components/onboarding/slides/unifiedBackgroundConfig";

function WelcomeSlideTitle() {
  const { t } = useTranslation();

  return (
    <span className={styles.welcomeTitleContainer}>
      {t("onboarding.welcomeSlide.title", "Welcome to GoreeCloud PDF Manager")}
    </span>
  );
}

const WelcomeSlideBody = () => (
  <span>
    <Trans
      i18nKey="onboarding.welcomeSlide.body"
      components={{ strong: <strong /> }}
      defaults="GoreeCloud PDF Manager is an open-core development preview. Start with available PDF tools; some upstream commercial capabilities are not included."
    />
  </span>
);

export default function WelcomeSlide(): SlideConfig {
  return {
    key: "welcome",
    title: <WelcomeSlideTitle />,
    body: <WelcomeSlideBody />,
    background: {
      gradientStops: ["#7C3AED", "#EC4899"],
      circles: UNIFIED_CIRCLE_CONFIG,
    },
  };
}
