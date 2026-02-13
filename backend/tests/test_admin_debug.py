from fastapi.testclient import TestClient

from app.deps import get_posthog_client
from app.flags import DEBUG_ADMIN_PANEL
from app.main import app
from app.posthog_client import FakePostHogClient


def test_admin_debug_forbidden_when_flag_off():
    fake = FakePostHogClient(global_flags={DEBUG_ADMIN_PANEL: False})
    app.dependency_overrides[get_posthog_client] = lambda: fake
    client = TestClient(app)

    res = client.get("/admin/debug", headers={"x-distinct-id": "u1"})

    assert res.status_code == 403
    assert res.json()["detail"] == "Debug panel disabled"


def test_admin_debug_allowed_when_flag_on():
    fake = FakePostHogClient(global_flags={DEBUG_ADMIN_PANEL: True})
    app.dependency_overrides[get_posthog_client] = lambda: fake
    client = TestClient(app)

    res = client.get("/admin/debug", headers={"x-distinct-id": "u2"})

    assert res.status_code == 200
    assert res.json()["status"] == "visible"
    assert fake.events[-1]["event"] == "admin_debug_viewed"

    app.dependency_overrides.clear()
