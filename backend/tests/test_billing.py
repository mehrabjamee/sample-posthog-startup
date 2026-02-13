from fastapi.testclient import TestClient

from app.deps import get_posthog_client
from app.flags import NEW_BILLING_FLOW
from app.main import app
from app.posthog_client import FakePostHogClient


def test_billing_quote_legacy_flow():
    fake = FakePostHogClient(global_flags={NEW_BILLING_FLOW: False})
    app.dependency_overrides[get_posthog_client] = lambda: fake

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
    assert fake.events == []


def test_billing_quote_new_flow_with_discount_and_capture():
    fake = FakePostHogClient(global_flags={NEW_BILLING_FLOW: True})
    app.dependency_overrides[get_posthog_client] = lambda: fake

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
    assert fake.events[0]["event"] == "billing_new_flow_quote_created"
