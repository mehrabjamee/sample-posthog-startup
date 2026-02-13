import { useFeatureFlag } from "../lib/useFeatureFlag";

export function OnboardingFlow() {
  const enabled = useFeatureFlag("onboarding-v2");

  if (!enabled) {
    return (
      <section>
        <h3>Onboarding</h3>
        <ol>
          <li>Choose your top class interests</li>
          <li>Set your weekly availability</li>
          <li>Pick a home neighborhood</li>
        </ol>
      </section>
    );
  }

  return (
    <section>
      <h3>Onboarding v2</h3>
      <ol>
        <li>Select your learning goal for this month</li>
        <li>Get a personalized class track in one click</li>
        <li>Book your first workshop with a new-member credit</li>
      </ol>
    </section>
  );
}
