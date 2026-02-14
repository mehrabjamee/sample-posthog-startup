import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { OnboardingFlow } from "../components/OnboardingFlow";

describe("OnboardingFlow", () => {
  it("shows v2 onboarding", () => {
    render(<OnboardingFlow />);
    expect(screen.getByText("Onboarding v2")).toBeInTheDocument();
  });
});
