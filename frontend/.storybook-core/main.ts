/** Nonpublishing MIT-core Storybook smoke; no excluded upstream modules. */
import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  // Exercise the real Storybook Vite + docgen transform with an existing,
  // core-only React/TypeScript story; never load restricted upstream stories.
  stories: ["../src/editor/core/tokens/Tokens.stories.tsx"],
  addons: [],
  framework: { name: "@storybook/react-vite", options: {} },
  typescript: { reactDocgen: "react-docgen-typescript" },
  staticDirs: [],
  viteFinal: async (viteConfig) => {
    // Storybook's output is disposable. Exclude app deployment hooks.
    viteConfig.publicDir = false;
    const appOnly = new Set(["prerender-og", "compress-static-copy"]);
    viteConfig.plugins = (viteConfig.plugins ?? []).filter((plugin) => {
      const name =
        plugin && typeof plugin === "object" && "name" in plugin
          ? (plugin as { name?: unknown }).name
          : undefined;
      return typeof name !== "string" || !appOnly.has(name);
    });
    return viteConfig;
  },
};
export default config;
