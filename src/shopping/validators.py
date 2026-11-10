"""Deterministic validation primitives for apparel shopping decisions.

LLM agents may propose values, but only these functions classify hard gates.
All timestamps must be timezone-aware ISO-8601 strings.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class GateResult:
    status: str
    code: str
    message: str
    evidence_refs: tuple[str, ...] = ()
    details: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["evidence_refs"] = list(self.evidence_refs)
        return value


def _parse_aware_datetime(value: str | datetime | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if value.tzinfo is None or value.utcoffset() is None:
        return None
    return value.astimezone(timezone.utc)


def evaluate_freshness(
    observed_at: str | datetime | None,
    ttl_seconds: int,
    *,
    now: str | datetime | None = None,
    allowed_clock_skew_seconds: int = 60,
) -> GateResult:
    """Check observation freshness; malformed/naive/future times fail closed."""
    if ttl_seconds < 0 or allowed_clock_skew_seconds < 0:
        raise ValueError("TTL and allowed clock skew must be non-negative")
    observed = _parse_aware_datetime(observed_at)
    current = _parse_aware_datetime(now) if now is not None else datetime.now(timezone.utc)
    if observed is None or current is None:
        return GateResult("UNKNOWN", "INVALID_TIMESTAMP", "Timestamp is missing, malformed, or timezone-naive.")
    age = (current - observed).total_seconds()
    if age < -allowed_clock_skew_seconds:
        return GateResult("UNKNOWN", "FUTURE_OBSERVATION", "Observation timestamp is in the future.")
    if age > ttl_seconds:
        return GateResult("STALE", "OBSERVATION_STALE", "Observation exceeds its configured TTL.",
                          details={"age_seconds": round(age), "ttl_seconds": ttl_seconds})
    return GateResult("PASS", "OBSERVATION_FRESH", "Observation is within its configured TTL.",
                      details={"age_seconds": max(0, round(age)), "ttl_seconds": ttl_seconds})


def evaluate_identity(
    expected_product_variant_id: str | None,
    observed_product_variant_id: str | None,
    identity_status: str,
    *,
    evidence_ref: str | None = None,
) -> GateResult:
    if not expected_product_variant_id or not observed_product_variant_id:
        return GateResult("UNKNOWN", "IDENTITY_MISSING", "Expected or observed product identity is missing.")
    if expected_product_variant_id != observed_product_variant_id:
        return GateResult("FAIL", "IDENTITY_MISMATCH", "Evidence belongs to a different product variant.")
    if identity_status != "VERIFIED":
        return GateResult("UNKNOWN", "IDENTITY_UNVERIFIED", "Product identity has not passed verification.")
    if not evidence_ref:
        return GateResult("UNKNOWN", "IDENTITY_EVIDENCE_MISSING", "Identity verification has no evidence reference.")
    return GateResult("PASS", "IDENTITY_VERIFIED", "Product variant identity matches.", (evidence_ref,))


def evaluate_size_match(
    requested_size: str,
    advertised_size: str | None,
    size_system: str | None,
    *,
    evidence_ref: str | None = None,
    expected_product_variant_id: str | None = None,
    chart_mapping: Mapping[str, Any] | None = None,
) -> GateResult:
    """Require an exact KR label or evidenced, product-specific chart mapping.

    Labels such as XXL are never assumed equivalent to KR 110 from naming alone.
    """
    if not requested_size or not advertised_size:
        return GateResult("UNKNOWN", "SIZE_MISSING", "Requested or advertised size is missing.")
    if size_system == "KR" and advertised_size.strip().upper() == requested_size.strip().upper():
        if not evidence_ref:
            return GateResult("UNKNOWN", "SIZE_EVIDENCE_MISSING", "Exact size option has no evidence reference.")
        return GateResult("PASS", "SIZE_EXACT_MATCH", "Advertised Korean size exactly matches the request.",
                          (evidence_ref,))
    if not chart_mapping:
        return GateResult("UNKNOWN", "SIZE_MAPPING_MISSING", "A verified brand size-chart mapping is required.")
    mapped = str(chart_mapping.get("normalized_size", "")).strip().upper()
    mapping_status = chart_mapping.get("verification_status")
    mapping_product = chart_mapping.get("product_variant_id")
    mapping_evidence = chart_mapping.get("evidence_ref")
    if not expected_product_variant_id or not mapping_product or not mapping_evidence:
        return GateResult("UNKNOWN", "SIZE_MAPPING_PROVENANCE_MISSING",
                          "Size mapping lacks exact product scope or evidence.")
    if mapping_product != expected_product_variant_id:
        return GateResult("FAIL", "SIZE_MAPPING_PRODUCT_MISMATCH", "Size chart applies to another product variant.")
    if mapping_status != "VERIFIED":
        return GateResult("UNKNOWN", "SIZE_MAPPING_UNVERIFIED", "Size-chart equivalence is not verified.")
    if mapped != requested_size.strip().upper():
        return GateResult("FAIL", "SIZE_MISMATCH", "Advertised size maps to a different requested size.",
                          (str(mapping_evidence),), {"mapped_size": mapped})
    return GateResult("PASS", "SIZE_CHART_MATCH", "Size is supported by a verified product-specific chart.",
                      (str(mapping_evidence),))


def evaluate_price_cap(
    sale_price: int | None,
    shipping_cost: int | None,
    max_total_price: int,
    *,
    mandatory_extra_cost: int = 0,
    currency: str = "KRW",
    evidence_ref: str | None = None,
) -> GateResult:
    """Compare known payable price (item + shipping + mandatory costs) to cap."""
    values = (sale_price, shipping_cost, max_total_price, mandatory_extra_cost)
    if any(v is not None and (not isinstance(v, int) or isinstance(v, bool)) for v in values):
        raise TypeError("Prices must be integer KRW amounts.")
    if currency != "KRW":
        return GateResult("UNKNOWN", "CURRENCY_UNSUPPORTED", "Price must be normalized to KRW.")
    if sale_price is None or shipping_cost is None:
        return GateResult("UNKNOWN", "PRICE_COMPONENT_MISSING", "Sale price and shipping cost must both be known.")
    if sale_price < 0 or shipping_cost < 0 or max_total_price < 0 or mandatory_extra_cost < 0:
        raise ValueError("Prices and price limits must be non-negative.")
    if not evidence_ref:
        return GateResult("UNKNOWN", "PRICE_EVIDENCE_MISSING", "Price observation has no evidence reference.")
    total = sale_price + shipping_cost + mandatory_extra_cost
    if total > max_total_price:
        return GateResult("FAIL", "PRICE_CAP_EXCEEDED", "Total payable price exceeds the user's price cap.",
                          (evidence_ref,), {"total_price": total, "max_total_price": max_total_price})
    return GateResult("PASS", "PRICE_WITHIN_CAP", "Total payable price is within the user's price cap.",
                      (evidence_ref,), {"total_price": total, "max_total_price": max_total_price})


def calculate_discount_percent(reference_price: int | None, sale_price: int | None) -> float | None:
    """Return arithmetic discount only when a positive reference price exceeds sale price."""
    for value in (reference_price, sale_price):
        if value is not None and (not isinstance(value, int) or isinstance(value, bool)):
            raise TypeError("Prices must be integer KRW amounts.")
    if reference_price is None or sale_price is None or reference_price <= 0 or sale_price < 0:
        return None
    if reference_price <= sale_price:
        return 0.0
    return round((reference_price - sale_price) / reference_price * 100, 1)


def evaluate_availability(
    availability: str,
    verification_method: str,
    selected_options: Mapping[str, str] | None,
    expected_options: Mapping[str, str],
    observed_at: str | datetime | None,
    ttl_seconds: int,
    *,
    now: str | datetime | None = None,
    evidence_ref: str | None = None,
) -> GateResult:
    """Require exact requested options, option-level proof, evidence, and fresh stock."""
    if availability in {"SOLD_OUT", "OPTION_MISSING"}:
        return GateResult("FAIL", "OPTION_UNAVAILABLE", "Requested option is sold out or missing.")
    if availability not in {"AVAILABLE", "LOW_STOCK"}:
        return GateResult("UNKNOWN", "AVAILABILITY_UNCONFIRMED", "Availability is not confirmed for immediate purchase.")
    if not selected_options or dict(selected_options) != dict(expected_options):
        return GateResult("UNKNOWN", "OPTION_NOT_SELECTED", "Exact requested color/size options were not verified.")
    allowed_methods = {"option_selection", "cart_step", "seller_api", "seller_confirmation"}
    if verification_method not in allowed_methods:
        return GateResult("UNKNOWN", "STOCK_PROOF_INSUFFICIENT", "Listing presence alone is not option-level stock proof.")
    if not evidence_ref:
        return GateResult("UNKNOWN", "STOCK_EVIDENCE_MISSING", "Option availability has no evidence reference.")
    fresh = evaluate_freshness(observed_at, ttl_seconds, now=now)
    if fresh.status != "PASS":
        return GateResult(fresh.status, fresh.code, fresh.message, details=fresh.details)
    return GateResult("PASS", "OPTION_AVAILABLE", "Exact requested option is available and observation is fresh.",
                      (evidence_ref,), {"availability": availability, "verification_method": verification_method})


def validate_evidence_coverage(
    required_field_keys: Sequence[str],
    evidence_records: Sequence[Mapping[str, Any]],
    product_variant_id: str,
) -> GateResult:
    """Ensure each critical field has identity-matched verified provenance."""
    missing: list[str] = []
    refs: list[str] = []
    for field_key in required_field_keys:
        matches = [
            record for record in evidence_records
            if record.get("field_key") == field_key
            and record.get("product_variant_id") == product_variant_id
            and record.get("verification_status") == "VERIFIED"
            and record.get("source_id")
            and record.get("evidence_id")
            and record.get("url")
            and record.get("retrieved_at")
        ]
        if not matches:
            missing.append(field_key)
        else:
            refs.extend(str(record["evidence_id"]) for record in matches)
    if missing:
        return GateResult("UNKNOWN", "EVIDENCE_COVERAGE_INCOMPLETE",
                          "One or more required fields lack verified, product-scoped evidence.",
                          tuple(sorted(set(refs))), {"missing_fields": missing})
    return GateResult("PASS", "EVIDENCE_COVERAGE_COMPLETE",
                      "All required fields have verified, product-scoped evidence.",
                      tuple(sorted(set(refs))))
