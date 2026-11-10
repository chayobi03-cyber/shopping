import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_DIR = Path(__file__).parents[1] / "schemas"


@pytest.mark.parametrize("schema_path", sorted(SCHEMA_DIR.glob("*.schema.json")))
def test_schema_is_valid_json_schema(schema_path):
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)


def test_request_schema_accepts_mens_110_budget_request():
    schema = json.loads((SCHEMA_DIR / "request.schema.json").read_text(encoding="utf-8"))
    sample = {
        "request_id": "req-001",
        "category": ["cardigan", "zip_hoodie"],
        "gender": "men",
        "condition": "NEW",
        "currency": "KRW",
        "max_total_price": 40000,
        "required_options": {"size": "110"},
        "preferred_brands": ["TOPTEN", "POLHAM"],
        "preferences": ["quality_material", "high_discount"],
        "created_at": "2026-11-10T09:00:00+09:00",
    }
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(sample)


def test_offer_schema_rejects_missing_availability_check_time():
    schema = json.loads((SCHEMA_DIR / "offer.schema.json").read_text(encoding="utf-8"))
    sample = {
        "offer_id": "off-001", "product_variant_id": "prod-001",
        "seller": "official shop", "url": "https://example.com/p/1",
        "currency": "KRW", "sale_price": 29900, "checked_at": "2026-11-10T09:00:00+09:00",
        "availability": "AVAILABLE", "size_option": "110", "color_option": "black",
    }
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(sample))
    assert any(error.validator == "required" for error in errors)


def test_decision_schema_rejects_buy_with_unknown_hard_gate():
    schema = json.loads((SCHEMA_DIR / "decision.schema.json").read_text(encoding="utf-8"))
    sample = {
        "decision_id": "dec-001",
        "product_variant_id": "prod-001",
        "as_of": "2026-11-10T09:00:00+09:00",
        "hard_gates": {
            "gender": "PASS", "size_110": "UNKNOWN", "new": "PASS",
            "price_cap": "PASS", "identity": "PASS", "stock": "PASS"
        },
        "decision": "BUY",
        "evidence_refs": ["ev-001"],
        "review_status": "PASS"
    }
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(sample))
    assert errors


def test_decision_schema_accepts_fully_verified_buy_snapshot():
    schema = json.loads((SCHEMA_DIR / "decision.schema.json").read_text(encoding="utf-8"))
    sample = {
        "decision_id": "dec-002",
        "product_variant_id": "prod-001",
        "as_of": "2026-11-10T09:00:00+09:00",
        "hard_gates": {
            "gender": "PASS", "size_110": "PASS", "new": "PASS",
            "price_cap": "PASS", "identity": "PASS", "stock": "PASS"
        },
        "decision": "BUY",
        "evidence_refs": ["ev-001", "ev-002"],
        "review_status": "PASS"
    }
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(sample)
