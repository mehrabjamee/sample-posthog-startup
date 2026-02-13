from fastapi.testclient import TestClient

from app.deps import get_posthog_client
from app.flags import NEW_BILLING_FLOW
from app.main import app


class MockPostHogClient:
    def __init__(self, flags: dict[str, bool]) -> None:
        self.flags = flags

    def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
        return bool(self.flags.get(flag_key, False))


def test_billing_quote_legacy_flow():
    mock = MockPostHogClient(flags={NEW_BILLING_FLOW: False})
    app.dependency_overrides[get_posthog_client] = lambda: mock

    client = TestClient(app)
    res = client.post(
        "/billing/quote",
        json={
            "distinct_id": "u_legacy",
            "seats": 2,
            "usage_units": 1400,
            "is_enterprise": True,
            "annual_commit": True,
        },
    )

    assert res.status_code == 200
    body = res.json()
    assert body["flow"] == "legacy"
    assert body["total"] == 3200


def test_billing_quote_new_flow_with_discount():
    mock = MockPostHogClient(flags={NEW_BILLING_FLOW: True})
    app.dependency_overrides[get_posthog_client] = lambda: mock

    client = TestClient(app)
    res = client.post(
        "/billing/quote",
        json={
            "distinct_id": "u_new",
            "seats": 2,
            "usage_units": 1400,
            "is_enterprise": True,
            "annual_commit": True,
        },
    )

    assert res.status_code == 200
    body = res.json()
    assert body["flow"] == "new"
    assert body["subtotal"] == 2200
    assert body["discount"] == 440
    assert body["total"] == 1760
