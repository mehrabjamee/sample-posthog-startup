from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from app.posthog_client import PostHogClientProtocol

T = TypeVar("T")


def with_flag(
    *,
    posthog_client: PostHogClientProtocol,
    flag_key: str,
    distinct_id: str,
    on_fn: Callable[[], T],
    off_fn: Callable[[], T],
) -> T:
    """Helper wrapper used when feature branches are non-trivial."""

    if posthog_client.is_feature_enabled(flag_key, distinct_id):
        return on_fn()
    return off_fn()
