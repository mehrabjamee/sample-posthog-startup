from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from posthog import Posthog

from app.posthog_client import PostHogClientProtocol

# Load local env files for developer convenience.
load_dotenv(".env.local")
load_dotenv(".env")


@lru_cache(maxsize=1)
def get_posthog_client() -> PostHogClientProtocol:
    """Dependency boundary for PostHog client injection."""

    api_key = os.getenv("POSTHOG_API_KEY")
    if not api_key:
        raise RuntimeError("POSTHOG_API_KEY is required")

    host = os.getenv("POSTHOG_HOST", "https://us.i.posthog.com")
    sdk_client = Posthog(project_api_key=api_key, host=host)

    class _SDKPostHogClient(PostHogClientProtocol):
        def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
            return bool(sdk_client.feature_enabled(flag_key, distinct_id))

    return _SDKPostHogClient()
