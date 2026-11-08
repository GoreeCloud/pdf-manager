import React from "react";
import { Trans } from "react-i18next";
import i18n from "@editor/i18n";
import { SlideConfig } from "@editor/types/types";
import { UNIFIED_CIRCLE_CONFIG } from "@editor/components/onboarding/slides/unifiedBackgroundConfig";
import styles from "@editor/components/onboarding/InitialOnboardingModal/InitialOnboardingModal.module.css";

export default function TourOverviewSlide(): SlideConfig {
  return {
    key: "tour-overview",
    title: i18n.t("onboarding.tourOverview.title", "Tour Overview"),
    body: (
      <span className={styles.bodyCopyInner}>
        <Trans
          i18nKey="onboarding.tourOverview.body"
          defaults="Explore the available PDF tools and learn where to find the options included in this development preview."
          components={{ strong: <strong /> }}
        />
      </span>
    ),
    background: {
      gradientStops: ["#2563EB", "#7C3AED"],
      circles: UNIFIED_CIRCLE_CONFIG,
    },
  };
}
