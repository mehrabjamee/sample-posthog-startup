class BrowserPostHogClient {
  constructor(posthogInstance) {
    this.posthog = posthogInstance;
  }

  isFeatureEnabled(flagKey) {
    if (!this.posthog || typeof this.posthog.isFeatureEnabled !== "function") {
      return false;
    }
    return Boolean(this.posthog.isFeatureEnabled(flagKey));
  }

  subscribe(callback) {
    if (!this.posthog || typeof this.posthog.onFeatureFlags !== "function") {
      return () => {};
    }

    this.posthog.onFeatureFlags(() => {
      callback();
    });

    return () => {};
  }
}

function createClient() {
  return new BrowserPostHogClient(window.posthog);
}

let activeClient;

export function initializePostHogClient(client = createClient()) {
  activeClient = client;
  return activeClient;
}

function getClient() {
  if (!activeClient) {
    activeClient = createClient();
  }
  return activeClient;
}

export function isFeatureEnabled(flagKey) {
  return getClient().isFeatureEnabled(flagKey);
}

export function subscribeToFlags(callback) {
  return getClient().subscribe(callback);
}
