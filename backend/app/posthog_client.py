from __future__ import annotations

class PostHogClientProtocol:
    def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
        raise NotImplementedError
