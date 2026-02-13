from __future__ import annotations

from app.flags import EXP_SEARCH_RANKING
from app.posthog_client import PostHogClientProtocol


CATALOG = [
    {"id": "p1", "title": "Realtime Product Analytics", "summary": "Track events"},
    {"id": "p2", "title": "Feature Flags for SaaS", "summary": "Progressive rollout"},
    {"id": "p3", "title": "Session Replay", "summary": "Understand friction"},
]


def rank_results(
    *,
    query: str,
    distinct_id: str,
    posthog_client: PostHogClientProtocol,
) -> list[dict[str, str]]:
    if not query.strip():
        return []

    query_l = query.lower()

    if posthog_client.is_feature_enabled(EXP_SEARCH_RANKING, distinct_id):
        # Experimental rank: title prefix matches > title contains > summary contains.
        def score(item: dict[str, str]) -> tuple[int, int]:
            title = item["title"].lower()
            summary = item["summary"].lower()
            if title.startswith(query_l):
                return (0, len(title))
            if query_l in title:
                return (1, len(title))
            if query_l in summary:
                return (2, len(summary))
            return (3, 999)

        ranked = sorted(CATALOG, key=score)
        posthog_client.capture(
            distinct_id,
            "search_ranking_experiment_seen",
            {"query": query, "algorithm": "exp-v2"},
        )
        return [item for item in ranked if query_l in (item["title"] + item["summary"]).lower()]

    # Legacy rank: stable id order with simple query filter.
    filtered = [
        item for item in CATALOG if query_l in (item["title"] + item["summary"]).lower()
    ]
    return sorted(filtered, key=lambda item: item["id"])
