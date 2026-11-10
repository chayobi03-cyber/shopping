from datetime import datetime, timedelta, timezone

import pytest

from shopping.validators import (
    calculate_discount_percent,
    evaluate_availability,
    evaluate_freshness,
    evaluate_identity,
    evaluate_price_cap,
    evaluate_size_match,
    validate_evidence_coverage,
)


NOW = "2026-11-10T09:00:00+09:00"
VARIANT = "topten-cardigan-black-110-2026fw"


def test_size_exact_korean_110_passes():
    assert evaluate_size_match("110", "110", "KR").status == "PASS"


def test_xxl_is_not_assumed_to_be_110():
    result = evaluate_size_match("110", "XXL", "INTL")
    assert result.status == "UNKNOWN"


def test_verified_product_specific_size_chart_passes():
    mapping = {
        "normalized_size": "110",
        "verification_status": "VERIFIED",
        "product_variant_id": VARIANT,
        "expected_product_variant_id": VARIANT,
        "evidence_ref": "ev-size-01",
    }
    assert evaluate_size_match("110", "XXL", "INTL", chart_mapping=mapping).status == "PASS"


def test_size_chart_for_another_product_fails():
    mapping = {
        "normalized_size": "110",
        "verification_status": "VERIFIED",
        "product_variant_id": "another-product",
        "expected_product_variant_id": VARIANT,
        "evidence_ref": "ev-size-01",
    }
    assert evaluate_size_match("110", "XXL", "INTL", chart_mapping=mapping).status == "FAIL"


def test_missing_shipping_prevents_price_pass():
    assert evaluate_price_cap(29900, None, 40000).status == "UNKNOWN"


def test_shipping_included_in_price_cap():
    assert evaluate_price_cap(37900, 3000, 40000).status == "FAIL"


def test_price_exactly_at_cap_passes():
    result = evaluate_price_cap(37900, 2100, 40000)
    assert result.status == "PASS"
    assert result.details["total_price"] == 40000


def test_negative_price_rejected_as_invalid_input():
    with pytest.raises(ValueError):
        evaluate_price_cap(-1, 0, 40000)


def test_discount_uses_reference_price():
    assert calculate_discount_percent(59900, 29900) == 50.1


def test_unknown_reference_price_has_no_discount_claim():
    assert calculate_discount_percent(None, 29900) is None


def test_future_timestamp_fails_closed():
    result = evaluate_freshness("2026-11-10T10:00:00+09:00", 7200, now=NOW)
    assert result.status == "UNKNOWN"


def test_stale_stock_fails():
    result = evaluate_availability(
        "AVAILABLE", "option_selection", {"size": "110", "color": "black"},
        {"size": "110", "color": "black"}, "2026-11-10T05:00:00+09:00", 7200, now=NOW
    )
    assert result.status == "STALE"


def test_listing_page_does_not_prove_stock():
    result = evaluate_availability(
        "AVAILABLE", "listing_only", {"size": "110", "color": "black"},
        {"size": "110", "color": "black"}, NOW, 7200, now=NOW
    )
    assert result.status == "UNKNOWN"


def test_wrong_option_selection_does_not_pass():
    result = evaluate_availability(
        "AVAILABLE", "cart_step", {"size": "105", "color": "black"},
        {"size": "110", "color": "black"}, NOW, 7200, now=NOW
    )
    assert result.status == "UNKNOWN"


def test_exact_fresh_option_stock_passes():
    result = evaluate_availability(
        "LOW_STOCK", "cart_step", {"size": "110", "color": "black"},
        {"size": "110", "color": "black"}, NOW, 7200, now=NOW
    )
    assert result.status == "PASS"


def test_identity_mismatch_fails():
    assert evaluate_identity(VARIANT, "other-variant", "VERIFIED", evidence_ref="ev-1").status == "FAIL"


def test_identity_requires_evidence_ref():
    assert evaluate_identity(VARIANT, VARIANT, "VERIFIED").status == "UNKNOWN"


def test_evidence_must_match_variant_and_field():
    records = [{
        "field_key": "fiber_composition", "product_variant_id": VARIANT,
        "verification_status": "VERIFIED", "source_id": "official",
        "evidence_id": "ev-1", "url": "https://example.com/spec",
        "retrieved_at": NOW,
    }]
    assert validate_evidence_coverage(["fiber_composition"], records, VARIANT).status == "PASS"
    assert validate_evidence_coverage(["size_chart"], records, VARIANT).status == "UNKNOWN"
