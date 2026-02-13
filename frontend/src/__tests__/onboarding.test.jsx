import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { OnboardingFlow } from "../components/OnboardingFlow";
import { initializePostHogClient } from "../lib/posthog";


describe("OnboardingFlow", () => {
  let onboardingEnabled = false;

  beforeEach(() => {
    onboardingEnabled = false;
    initializePostHogClient({
      isFeatureEnabled: (flagKey) => {
        if (flagKey === "onboarding-v2") return onboardingEnabled;
        return false;
      },
      subscribe: () => () => {},
    });
  });

  it("shows v1 when onboarding-v2 is disabled", () => {
    onboardingEnabled = false;
    render(<OnboardingFlow />);

    expect(screen.getByText("Onboarding")).toBeInTheDocument();
    expect(screen.queryByText("Onboarding v2")).not.toBeInTheDocument();
  });

  it("shows v2 when onboarding-v2 is enabled", () => {
    onboardingEnabled = true;
    render(<OnboardingFlow />);

    expect(screen.getByText("Onboarding v2")).toBeInTheDocument();
  });
});
