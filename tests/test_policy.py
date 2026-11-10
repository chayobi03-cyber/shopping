import json

import pytest

from shopping.policy import load_freshness_policy, validate_freshness_policy


def test_repository_freshness_policy_loads():
    policy = load_freshness_policy()
    assert policy["price"] == 86400
    assert policy["availability"] == 7200


def test_freshness_policy_rejects_missing_category():
    with pytest.raises(ValueError):
        validate_freshness_policy({"ttl_seconds": {"price": 60}})


def test_freshness_policy_rejects_negative_ttl():
    policy = {"ttl_seconds": {
        "price": -1, "availability": 60, "review_aggregate": 60,
        "official_product_specification": 60
    }}
    with pytest.raises(ValueError):
        validate_freshness_policy(policy)


def test_freshness_policy_rejects_boolean_ttl():
    policy = {"ttl_seconds": {
        "price": True, "availability": 60, "review_aggregate": 60,
        "official_product_specification": 60
    }}
    with pytest.raises(ValueError):
        validate_freshness_policy(policy)
