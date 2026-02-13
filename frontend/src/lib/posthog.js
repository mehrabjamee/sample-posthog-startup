const localFlags = {
  "new-billing-flow": false,
  "onboarding-v2": false,
  "exp-search-ranking": false
};

const listeners = new Set();

export function setLocalFeatureFlag(flagKey, enabled) {
  localFlags[flagKey] = Boolean(enabled);
  listeners.forEach((listener) => listener());
}

export function isFeatureEnabled(flagKey) {
  return Boolean(localFlags[flagKey]);
}

export function subscribeToFlags(callback) {
  listeners.add(callback);
  return () => listeners.delete(callback);
}
