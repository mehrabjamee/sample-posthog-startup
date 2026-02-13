import { useEffect, useState } from "react";
import { isFeatureEnabled, subscribeToFlags } from "./posthog";

export function useFeatureFlag(flagKey) {
  const [enabled, setEnabled] = useState(() => isFeatureEnabled(flagKey));

  useEffect(() => {
    const unsub = subscribeToFlags(() => {
      setEnabled(isFeatureEnabled(flagKey));
    });
    return unsub;
  }, [flagKey]);

  return enabled;
}
