from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any


class PostHogClientProtocol:
    def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
        raise NotImplementedError

    def capture(
        self, distinct_id: str, event: str, properties: dict[str, Any] | None = None
    ) -> None:
        raise NotImplementedError


class FakePostHogClient(PostHogClientProtocol):
    """Local fake PostHog client used for development and tests."""

    def __init__(
        self,
        global_flags: dict[str, bool] | None = None,
        per_user_flags: dict[str, dict[str, bool]] | None = None,
        sink: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        self._global_flags = global_flags or {}
        self._per_user_flags = per_user_flags or {}
        self._sink = sink
        self.events: list[dict[str, Any]] = []

    def set_flag(self, flag_key: str, enabled: bool, distinct_id: str | None = None) -> None:
        if distinct_id:
            user_flags = self._per_user_flags.setdefault(distinct_id, {})
            user_flags[flag_key] = enabled
            return
        self._global_flags[flag_key] = enabled

    def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
        user_flags = self._per_user_flags.get(distinct_id, {})
        if flag_key in user_flags:
            return user_flags[flag_key]
        if flag_key in self._global_flags:
            return self._global_flags[flag_key]
        env_key = f"FLAG_{flag_key.replace('-', '_').upper()}"
        return os.getenv(env_key, "false").lower() == "true"

    def capture(
        self, distinct_id: str, event: str, properties: dict[str, Any] | None = None
    ) -> None:
        payload = {
            "distinct_id": distinct_id,
            "event": event,
            "properties": properties or {},
        }
        self.events.append(payload)
        if self._sink:
            self._sink(payload)
