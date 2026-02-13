from __future__ import annotations

import os
from typing import Any


class PostHogClientProtocol:
    def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
        raise NotImplementedError

    def capture(
        self, distinct_id: str, event: str, properties: dict[str, Any] | None = None
    ) -> None:
        raise NotImplementedError


class RealPostHogClient(PostHogClientProtocol):
    """Thin adapter around the official PostHog Python SDK."""

    def __init__(self, *, api_key: str, host: str) -> None:
        from posthog import Posthog

        self._client = Posthog(project_api_key=api_key, host=host)

    def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
        return bool(self._client.feature_enabled(flag_key, distinct_id))

    def capture(
        self, distinct_id: str, event: str, properties: dict[str, Any] | None = None
    ) -> None:
        self._client.capture(distinct_id=distinct_id, event=event, properties=properties or {})


def create_posthog_client_from_env() -> PostHogClientProtocol:
    """Factory used by FastAPI dependency injection."""

    api_key = os.getenv("POSTHOG_API_KEY")
    if not api_key:
        raise RuntimeError("POSTHOG_API_KEY is required")

    host = os.getenv("POSTHOG_HOST", "https://us.i.posthog.com")
    return RealPostHogClient(api_key=api_key, host=host)
