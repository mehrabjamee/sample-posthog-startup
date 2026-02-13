"""Canonical feature flag registry for backend services."""

from __future__ import annotations

NEW_BILLING_FLOW = "new-billing-flow"
ONBOARDING_V2 = "onboarding-v2"
DEBUG_ADMIN_PANEL = "debug-admin-panel"
EXP_SEARCH_RANKING = "exp-search-ranking"

FLAG_REGISTRY: dict[str, dict[str, str]] = {
    NEW_BILLING_FLOW: {
        "description": "Ship the invoice engine rewrite with new discount rules.",
        "owner": "payments@startup.dev",
        "intended_state": "temporary",
        "created_at": "2025-08-18",
    },
    ONBOARDING_V2: {
        "description": "New user onboarding experience used by frontend only.",
        "owner": "growth@startup.dev",
        "intended_state": "experiment",
        "created_at": "2025-09-01",
    },
    DEBUG_ADMIN_PANEL: {
        "description": "Gate access to the internal debug admin endpoint.",
        "owner": "platform@startup.dev",
        "intended_state": "kill-switch",
        "created_at": "2025-10-14",
    },
    EXP_SEARCH_RANKING: {
        "description": "Search ranking experiment prioritizing title matches.",
        "owner": "search@startup.dev",
        "intended_state": "experiment",
        "created_at": "2025-11-05",
    },
}
