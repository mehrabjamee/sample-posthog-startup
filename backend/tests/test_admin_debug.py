from fastapi.testclient import TestClient

from app.deps import get_posthog_client
from app.flags import DEBUG_ADMIN_PANEL
from app.main import app


class MockPostHogClient:
    def __init__(self, flags: dict[str, bool]) -> None:
        self.flags = flags
        self.events: list[dict[str, object]] = []

    def is_feature_enabled(self, flag_key: str, distinct_id: str) -> bool:
        return bool(self.flags.get(flag_key, False))

    def capture(self, distinct_id: str, event: str, properties: dict | None = None) -> None:
        self.events.append(
            {
                "distinct_id": distinct_id,
                "event": event,
                "properties": properties or {},
            }
        )


def test_admin_debug_forbidden_when_flag_off():
    mock = MockPostHogClient(flags={DEBUG_ADMIN_PANEL: False})
    app.dependency_overrides[get_posthog_client] = lambda: mock
    client = TestClient(app)

    res = client.get("/admin/debug", headers={"x-distinct-id": "u1"})

    assert res.status_code == 403
    assert res.json()["detail"] == "Debug panel disabled"


def test_admin_debug_allowed_when_flag_on():
    mock = MockPostHogClient(flags={DEBUG_ADMIN_PANEL: True})
    app.dependency_overrides[get_posthog_client] = lambda: mock
    client = TestClient(app)

    res = client.get("/admin/debug", headers={"x-distinct-id": "u2"})

    assert res.status_code == 200
    assert res.json()["status"] == "visible"
    assert mock.events[-1]["event"] == "admin_debug_viewed"
