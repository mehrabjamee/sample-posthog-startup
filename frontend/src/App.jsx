import { useMemo, useState } from "react";
import { LegacyBilling } from "./components/LegacyBilling";
import { NewBilling } from "./components/NewBilling";
import { OnboardingFlow } from "./components/OnboardingFlow";
import { SearchResults } from "./components/SearchResults";
import { useFeatureFlagEnabled } from "@posthog/react";

const demoResults = [
  {
    id: "p1",
    title: "Pottery Basics: Wheel Throwing",
    summary: "Hands-on class for first-time ceramicists",
  },
  {
    id: "p2",
    title: "Night Sky Sketching",
    summary: "Guided drawing workshop for curious class-goers",
  },
  {
    id: "p3",
    title: "Bread Science Lab",
    summary: "Weekend class on fermentation with take-home starter",
  },
];

function rankFrontendResults(items, query, useExperimentalRanking) {
  const q = query.trim().toLowerCase();
  if (!q) return [];

  if (useExperimentalRanking) {
    return [...items]
      .filter((item) =>
        `${item.title} ${item.summary}`.toLowerCase().includes(q),
      )
      .sort((a, b) => {
        const aText = `${a.title} ${a.summary}`.toLowerCase();
        const bText = `${b.title} ${b.summary}`.toLowerCase();
        const aPos = aText.indexOf(q);
        const bPos = bText.indexOf(q);
        if (aPos !== bPos) return aPos - bPos;
        return a.id.localeCompare(b.id);
      });
  }

  return [...items]
    .filter((item) => `${item.title} ${item.summary}`.toLowerCase().includes(q))
    .sort((a, b) => a.id.localeCompare(b.id));
}

export default function App() {
  const [query, setQuery] = useState("class");
  const showNewBilling = useFeatureFlagEnabled("new-billing-flow");
  const useExperimentalRanking = useFeatureFlagEnabled("exp-search-ranking");

  const ranked = useMemo(() => {
    return rankFrontendResults(demoResults, query, useExperimentalRanking);
  }, [query, useExperimentalRanking]);

  return (
    <main style={{ fontFamily: "ui-sans-serif", padding: 20, maxWidth: 840 }}>
      <h1>HandsDirty</h1>
      <p>Discover and book small-group hobby workshops near you.</p>

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
