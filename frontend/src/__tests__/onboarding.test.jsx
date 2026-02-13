import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { OnboardingFlow } from "../components/OnboardingFlow";
import { setLocalFeatureFlag } from "../lib/posthog";


describe("OnboardingFlow", () => {
  it("shows v1 when onboarding-v2 is disabled", () => {
    setLocalFeatureFlag("onboarding-v2", false);
    render(<OnboardingFlow />);

    expect(screen.getByText("Onboarding")).toBeInTheDocument();
    expect(screen.queryByText("Onboarding v2")).not.toBeInTheDocument();
  });

  it("shows v2 when onboarding-v2 is enabled", () => {
    setLocalFeatureFlag("onboarding-v2", true);
    render(<OnboardingFlow />);

    expect(screen.getByText("Onboarding v2")).toBeInTheDocument();
  });
});
