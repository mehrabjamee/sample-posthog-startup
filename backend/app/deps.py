from __future__ import annotations

from app.posthog_client import FakePostHogClient, PostHogClientProtocol

_posthog_singleton = FakePostHogClient()


def get_posthog_client() -> PostHogClientProtocol:
    """Dependency boundary where a real PostHog client can be injected later."""

    return _posthog_singleton
