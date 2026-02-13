from __future__ import annotations

from app.flags import EXP_SEARCH_RANKING
from app.posthog_client import PostHogClientProtocol


CATALOG = [
    {
        "id": "p1",
        "title": "Pottery Basics: Wheel Throwing",
        "summary": "Hands-on class for first-time ceramicists",
    },
    {
        "id": "p2",
        "title": "Night Sky Sketching",
        "summary": "Guided drawing workshop for curious class-goers",
    },
    {
        "id": "p3",
        "title": "Bread Science Lab",
        "summary": "Weekend class on fermentation with take-home starter",
    },
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
        # Experimental rank: prioritize earlier term position across title+summary.
        def score(item: dict[str, str]) -> tuple[int, int, str]:
            text = f"{item['title']} {item['summary']}".lower()
            pos = text.find(query_l)
            if pos == -1:
                return (1, 999, item["id"])
            return (0, pos, item["id"])

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
