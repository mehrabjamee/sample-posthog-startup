from fastapi.testclient import TestClient

from app.deps import get_posthog_client
from app.flags import EXP_SEARCH_RANKING
from app.main import app


class MockPostHogClient:
    def __init__(self, flags: dict[str, bool]) -> None:
        self.flags = flags

    def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
        return bool(self.flags.get(flag_key, False))


def test_search_legacy_ranking_order():
    mock = MockPostHogClient(flags={EXP_SEARCH_RANKING: False})
    app.dependency_overrides[get_posthog_client] = lambda: mock
    client = TestClient(app)

    res = client.post("/search", json={"distinct_id": "u_search", "query": "class"})

    assert res.status_code == 200
    body = res.json()
    assert [item["id"] for item in body["results"]] == ["p1", "p2", "p3"]


def test_search_experiment_ranking_order():
    mock = MockPostHogClient(flags={EXP_SEARCH_RANKING: True})
    app.dependency_overrides[get_posthog_client] = lambda: mock
    client = TestClient(app)

    res = client.post("/search", json={"distinct_id": "u_search", "query": "class"})

    assert res.status_code == 200
    body = res.json()
    assert [item["id"] for item in body["results"]] == ["p3", "p1", "p2"]
