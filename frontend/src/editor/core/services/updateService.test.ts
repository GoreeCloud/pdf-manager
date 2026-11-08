import { afterEach, describe, expect, it, vi } from "vitest";
import { UpdateService } from "@editor/services/updateService";
import type { MachineInfo } from "@editor/services/updateService";

const machine: MachineInfo = {
  machineType: "Server-jar",
  activeSecurity: true,
  licenseType: "NORMAL",
};

describe("GoreeCloud update channel lockdown", () => {
  const service = new UpdateService();

  afterEach(() => vi.restoreAllMocks());

  it("preserves local semantic-version comparison", () => {
    expect(service.compareVersions("3.2.0", "3.1.9")).toBe(1);
    expect(service.compareVersions("3.2.0", "3.2.0")).toBe(0);
    expect(service.compareVersions("3.1.9", "3.2.0")).toBe(-1);
  });

  it("offers no unverified upstream installer", () => {
    expect(service.getDownloadUrl(machine)).toBeNull();
  });

  it("does not contact the Stirling server for release metadata", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    expect(await service.getUpdateSummary("3.3.0", machine)).toBeNull();
    expect(await service.getFullUpdateInfo("3.3.0", machine)).toBeNull();
    expect(await service.getCurrentVersionFromGitHub()).toBe("");
    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
