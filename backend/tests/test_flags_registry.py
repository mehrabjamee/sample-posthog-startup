from app.flags import (
    DEBUG_ADMIN_PANEL,
    EXP_SEARCH_RANKING,
    FLAG_REGISTRY,
    NEW_BILLING_FLOW,
)


def test_flag_registry_has_expected_keys():
    keys = set(FLAG_REGISTRY.keys())
    assert {
        NEW_BILLING_FLOW,
        DEBUG_ADMIN_PANEL,
        EXP_SEARCH_RANKING,
    }.issubset(keys)
