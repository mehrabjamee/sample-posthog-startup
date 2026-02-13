from fastapi.testclient import TestClient

from app.deps import get_posthog_client
from app.flags import EXP_SEARCH_RANKING
from app.main import app
from app.posthog_client import FakePostHogClient


def test_search_legacy_ranking_order():
    fake = FakePostHogClient(global_flags={EXP_SEARCH_RANKING: False})
    app.dependency_overrides[get_posthog_client] = lambda: fake
    client = TestClient(app)

    res = client.post("/search", json={"distinct_id": "u_search", "query": "class"})

    assert res.status_code == 200
    body = res.json()
    assert [item["id"] for item in body["results"]] == ["p1", "p2", "p3"]
    assert fake.events == []


def test_search_experiment_ranking_capture_and_order():
    fake = FakePostHogClient(global_flags={EXP_SEARCH_RANKING: True})
    app.dependency_overrides[get_posthog_client] = lambda: fake
    client = TestClient(app)

    res = client.post("/search", json={"distinct_id": "u_search", "query": "class"})

    assert res.status_code == 200
    body = res.json()
    assert [item["id"] for item in body["results"]] == ["p3", "p1", "p2"]
    assert fake.events[-1]["event"] == "search_ranking_experiment_seen"
