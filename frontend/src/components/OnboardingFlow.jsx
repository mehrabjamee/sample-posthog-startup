import { useFeatureFlag } from "../lib/useFeatureFlag";

export function OnboardingFlow() {
  const enabled = useFeatureFlag("onboarding-v2");

  if (!enabled) {
    return (
      <section>
        <h3>Onboarding</h3>
        <ol>
          <li>Connect data source</li>
          <li>Install JS snippet</li>
          <li>Invite team</li>
        </ol>
      </section>
    );
  }

  return (
    <section>
      <h3>Onboarding v2</h3>
      <ol>
        <li>Start from a template workspace</li>
        <li>Enable product analytics + replay in one click</li>
        <li>Launch first feature flag experiment</li>
      </ol>
    </section>
  );
}
