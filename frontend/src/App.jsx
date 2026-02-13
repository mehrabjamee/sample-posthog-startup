import { useMemo, useState } from "react";
import { LegacyBilling } from "./components/LegacyBilling";
import { NewBilling } from "./components/NewBilling";
import { OnboardingFlow } from "./components/OnboardingFlow";
import { SearchResults } from "./components/SearchResults";
import { isFeatureEnabled, setLocalFeatureFlag } from "./lib/posthog";

const demoResults = [
  { id: "p1", title: "Realtime Product Analytics", summary: "Track events" },
  { id: "p2", title: "Feature Flags for SaaS", summary: "Progressive rollout" },
  { id: "p3", title: "Session Replay", summary: "Understand friction" }
];

function rankFrontendResults(items, query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];

  if (isFeatureEnabled("exp-search-ranking")) {
    return [...items]
      .filter((item) => `${item.title} ${item.summary}`.toLowerCase().includes(q))
      .sort((a, b) => a.title.length - b.title.length);
  }

  return [...items]
    .filter((item) => `${item.title} ${item.summary}`.toLowerCase().includes(q))
    .sort((a, b) => a.id.localeCompare(b.id));
}

export default function App() {
  const [query, setQuery] = useState("re");
  const [refreshTick, setRefreshTick] = useState(0);
  const showNewBilling = isFeatureEnabled("new-billing-flow");

  const ranked = useMemo(() => {
    return rankFrontendResults(demoResults, query);
  }, [query, refreshTick]);

  return (
    <main style={{ fontFamily: "ui-sans-serif", padding: 20, maxWidth: 840 }}>
      <h1>SignalDesk</h1>
      <p>Sample early-stage startup app with PostHog feature flags.</p>

      <div style={{ display: "flex", gap: 12, marginBottom: 18 }}>
        <button
          onClick={() => {
            setLocalFeatureFlag("new-billing-flow", !isFeatureEnabled("new-billing-flow"));
            setRefreshTick((t) => t + 1);
          }}
        >
          Toggle new-billing-flow
        </button>
        <button
          onClick={() => {
            setLocalFeatureFlag("onboarding-v2", !isFeatureEnabled("onboarding-v2"));
            setRefreshTick((t) => t + 1);
          }}
        >
          Toggle onboarding-v2
        </button>
        <button
          onClick={() => {
            setLocalFeatureFlag("exp-search-ranking", !isFeatureEnabled("exp-search-ranking"));
            setRefreshTick((t) => t + 1);
          }}
        >
          Toggle exp-search-ranking
        </button>
      </div>

      {showNewBilling ? <NewBilling /> : <LegacyBilling />}
      <OnboardingFlow />

      <label htmlFor="search-input">Query</label>
      <input
        id="search-input"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ marginLeft: 8 }}
      />
      <SearchResults results={ranked} />
    </main>
  );
}
