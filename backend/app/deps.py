from __future__ import annotations

from functools import lru_cache

from app.posthog_client import PostHogClientProtocol, create_posthog_client_from_env


@lru_cache(maxsize=1)
def get_posthog_client() -> PostHogClientProtocol:
    """Dependency boundary for PostHog client injection."""

    return create_posthog_client_from_env()
