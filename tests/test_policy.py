from shopping.policy import (
    evaluate_policy_freshness,
    load_freshness_policy,
    validate_freshness_policy,
)

NOW = "2026-11-10T09:00:00+09:00"


def test_repository_freshness_policy_loads():
    policy = load_freshness_policy()
    assert policy["price"] == 86400
    assert policy["availability"] == 7200
    assert policy["clock_skew_tolerance_seconds"] == 60


def test_freshness_policy_rejects_missing_category():
    import pytest
    with pytest.raises(ValueError):
        validate_freshness_policy({"ttl_seconds": {"price": 60}})


def test_freshness_policy_rejects_negative_ttl():
    import pytest
    policy = {"ttl_seconds": {
        "price": -1, "availability": 60, "review_aggregate": 60,
        "official_product_specification": 60
    }}
    with pytest.raises(ValueError):
        validate_freshness_policy(policy)


def test_freshness_policy_rejects_boolean_ttl():
    import pytest
    policy = {"ttl_seconds": {
        "price": True, "availability": 60, "review_aggregate": 60,
        "official_product_specification": 60
    }}
    with pytest.raises(ValueError):
        validate_freshness_policy(policy)


def test_policy_freshness_uses_configured_ttl():
    assert evaluate_policy_freshness(
        "2026-11-10T08:30:00+09:00", "availability", now=NOW
    ).status == "PASS"


def test_policy_freshness_rejects_stale_stock():
    assert evaluate_policy_freshness(
        "2026-11-10T06:00:00+09:00", "availability", now=NOW
    ).status == "STALE"


def test_policy_freshness_unknown_class_fails_closed():
    assert evaluate_policy_freshness(NOW, "unknown", now=NOW).status == "UNKNOWN"
