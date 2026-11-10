from shopping.validators import (
    calculate_discount_percent,
    evaluate_discount_claim,
    evaluate_availability,
    evaluate_freshness,
    evaluate_gender_match,
    evaluate_condition,
    evaluate_identity,
    evaluate_price_cap,
    evaluate_size_match,
    validate_evidence_coverage,
    validate_independent_review,
)

NOW = "2026-11-10T09:00:00+09:00"
VARIANT = "topten-cardigan-black-110-2026fw"
EV = "ev-validated-01"


def test_size_exact_korean_110_requires_evidence():
    assert evaluate_size_match("110", "110", "KR").status == "UNKNOWN"
    assert evaluate_size_match("110", "110", "KR", evidence_ref=EV).status == "PASS"


def test_xxl_is_not_assumed_to_be_110():
    assert evaluate_size_match("110", "XXL", "INTL").status == "UNKNOWN"


def test_verified_product_specific_size_chart_passes():
    mapping = {"normalized_size": "110", "verification_status": "VERIFIED",
               "product_variant_id": VARIANT, "advertised_size": "XXL", "evidence_ref": EV}
    result = evaluate_size_match("110", "XXL", "INTL",
                                 expected_product_variant_id=VARIANT, chart_mapping=mapping)
    assert result.status == "PASS"


def test_size_chart_for_another_product_fails():
    mapping = {"normalized_size": "110", "verification_status": "VERIFIED",
               "product_variant_id": "another-product", "advertised_size": "XXL", "evidence_ref": EV}
    assert evaluate_size_match("110", "XXL", "INTL",
                               expected_product_variant_id=VARIANT, chart_mapping=mapping).status == "FAIL"


def test_missing_shipping_prevents_price_pass():
    assert evaluate_price_cap(29900, None, 40000, mandatory_extra_cost=0, evidence_ref=EV).status == "UNKNOWN"


def test_shipping_included_in_price_cap():
    assert evaluate_price_cap(37900, 3000, 40000, mandatory_extra_cost=0, evidence_ref=EV).status == "FAIL"


def test_price_exactly_at_cap_passes():
    result = evaluate_price_cap(37900, 2100, 40000, mandatory_extra_cost=0, evidence_ref=EV)
    assert result.status == "PASS"
    assert result.details["total_price"] == 40000


def test_price_without_provenance_does_not_pass():
    assert evaluate_price_cap(29900, 0, 40000, mandatory_extra_cost=0).status == "UNKNOWN"


def test_negative_price_rejected_as_invalid_input():
    import pytest
    with pytest.raises(ValueError):
        evaluate_price_cap(-1, 0, 40000, mandatory_extra_cost=0, evidence_ref=EV)


def test_discount_uses_reference_price():
    assert calculate_discount_percent(59900, 29900) == 50.1


def test_unknown_reference_price_has_no_discount_claim():
    assert calculate_discount_percent(None, 29900) is None


def test_seller_list_price_is_not_a_verified_discount_baseline():
    result = evaluate_discount_claim(
        59900, 29900, reference_basis="SELLER_LIST_PRICE",
        reference_verified=True, reference_evidence_ref=EV,
        reference_product_variant_id=VARIANT, sale_product_variant_id=VARIANT
    )
    assert result.status == "UNKNOWN"


def test_official_msrp_with_evidence_can_support_discount_claim():
    result = evaluate_discount_claim(
        59900, 29900, reference_basis="OFFICIAL_MSRP",
        reference_verified=True, reference_evidence_ref=EV,
        reference_product_variant_id=VARIANT, sale_product_variant_id=VARIANT
    )
    assert result.status == "PASS"
    assert result.details["discount_percent"] == 50.1


def test_future_timestamp_fails_closed():
    assert evaluate_freshness("2026-11-10T10:00:00+09:00", 7200, now=NOW).status == "UNKNOWN"


def test_naive_timestamp_fails_closed():
    assert evaluate_freshness("2026-11-10T08:00:00", 7200, now=NOW).status == "UNKNOWN"


def test_stale_stock_fails():
    result = evaluate_availability(
        "AVAILABLE", "option_selection", {"size": "110", "color": "black"},
        {"size": "110", "color": "black"}, "2026-11-10T05:00:00+09:00",
        7200, now=NOW, evidence_ref=EV
    )
    assert result.status == "STALE"


def test_listing_page_does_not_prove_stock():
    result = evaluate_availability(
        "AVAILABLE", "listing_only", {"size": "110", "color": "black"},
        {"size": "110", "color": "black"}, NOW, 7200, now=NOW, evidence_ref=EV
    )
    assert result.status == "UNKNOWN"


def test_wrong_option_selection_does_not_pass():
    result = evaluate_availability(
        "AVAILABLE", "cart_step", {"size": "105", "color": "black"},
        {"size": "110", "color": "black"}, NOW, 7200, now=NOW, evidence_ref=EV
    )
    assert result.status == "UNKNOWN"


def test_exact_fresh_option_stock_passes():
    result = evaluate_availability(
        "LOW_STOCK", "cart_step", {"size": "110", "color": "black"},
        {"size": "110", "color": "black"}, NOW, 7200, now=NOW, evidence_ref=EV
    )
    assert result.status == "PASS"


def test_stock_without_evidence_does_not_pass():
    result = evaluate_availability(
        "AVAILABLE", "cart_step", {"size": "110", "color": "black"},
        {"size": "110", "color": "black"}, NOW, 7200, now=NOW
    )
    assert result.status == "UNKNOWN"


def test_identity_mismatch_fails():
    assert evaluate_identity(VARIANT, "other-variant", "VERIFIED", evidence_ref=EV).status == "FAIL"


def test_identity_requires_evidence_ref():
    assert evaluate_identity(VARIANT, VARIANT, "VERIFIED").status == "UNKNOWN"


def test_evidence_must_match_variant_and_field():
    records = [{
        "field_key": "fiber_composition", "product_variant_id": VARIANT,
        "verification_status": "VERIFIED", "source_id": "official",
        "evidence_id": EV, "url": "https://example.com/spec",
        "retrieved_at": NOW, "identity_match": "VERIFIED", "locator": "spec table / fiber row",
    }]
    assert validate_evidence_coverage(["fiber_composition"], records, VARIANT).status == "PASS"
    assert validate_evidence_coverage(["size_chart"], records, VARIANT).status == "UNKNOWN"
    assert validate_evidence_coverage(["fiber_composition"], records, "wrong-product").status == "UNKNOWN"


def test_explicit_wrong_korean_size_fails():
    assert evaluate_size_match("110", "105", "KR", evidence_ref=EV).status == "FAIL"


def test_gender_and_condition_require_matching_evidence():
    assert evaluate_gender_match("men", "men", evidence_ref=EV).status == "PASS"
    assert evaluate_gender_match("men", "women", evidence_ref=EV).status == "FAIL"
    assert evaluate_gender_match("men", "men").status == "UNKNOWN"
    assert evaluate_condition("NEW", "NEW", evidence_ref=EV).status == "PASS"
    assert evaluate_condition("NEW", "USED", evidence_ref=EV).status == "FAIL"
    assert evaluate_condition("NEW", "NEW").status == "UNKNOWN"


def test_independent_review_must_use_distinct_run():
    result = validate_independent_review("run-primary", "run-primary", "PASS", ["PASS"], [], [[EV]])
    assert result.status == "FAIL"


def test_review_cannot_pass_with_high_severity_finding():
    result = validate_independent_review("run-primary", "run-review", "PASS", ["PASS"], ["HIGH"], [[EV]])
    assert result.status == "FAIL"


def test_incomplete_review_does_not_pass():
    result = validate_independent_review("run-primary", "run-review", "PASS", ["UNKNOWN"], [], [[]])
    assert result.status == "UNKNOWN"


def test_independent_review_passes_when_clean():
    result = validate_independent_review(
        "run-primary", "run-review", "PASS_WITH_WARNINGS", ["PASS", "NOT_APPLICABLE"], ["LOW"], [[EV], []]
    )
    assert result.status == "PASS"


def test_unknown_gender_and_condition_remain_unknown():
    assert evaluate_gender_match("men", "unknown", evidence_ref=EV).status == "UNKNOWN"
    assert evaluate_condition("NEW", "UNKNOWN", evidence_ref=EV).status == "UNKNOWN"


def test_freshness_rejects_boolean_ttl():
    import pytest
    with pytest.raises(TypeError):
        evaluate_freshness(NOW, True, now=NOW)


def test_passed_size_mapping_must_target_exact_advertised_label():
    mapping = {"normalized_size": "110", "verification_status": "VERIFIED",
               "product_variant_id": VARIANT, "advertised_size": "XL", "evidence_ref": EV}
    result = evaluate_size_match("110", "XXL", "INTL",
                                 expected_product_variant_id=VARIANT, chart_mapping=mapping)
    assert result.status == "FAIL"


def test_passed_review_check_requires_its_own_evidence():
    result = validate_independent_review("run-primary", "run-review", "PASS", ["PASS"], [], [[]])
    assert result.status == "UNKNOWN"


def test_unknown_mandatory_costs_block_price_pass():
    assert evaluate_price_cap(29900, 0, 40000, evidence_ref=EV).status == "UNKNOWN"


def test_discount_baseline_must_match_same_variant():
    result = evaluate_discount_claim(
        59900, 29900, reference_basis="OFFICIAL_MSRP",
        reference_verified=True, reference_evidence_ref=EV,
        reference_product_variant_id=VARIANT,
        sale_product_variant_id="different-season-variant"
    )
    assert result.status == "UNKNOWN"


def test_discount_claim_requires_variant_identity():
    result = evaluate_discount_claim(
        59900, 29900, reference_basis="OFFICIAL_MSRP",
        reference_verified=True, reference_evidence_ref=EV,
        reference_product_variant_id=None, sale_product_variant_id=VARIANT
    )
    assert result.status == "UNKNOWN"
