"""Deterministic safety tests for shopping recommendation gates."""
from datetime import datetime, timedelta, timezone

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
STALE = "STALE"


def decide(gates, reviewer_status, evidence_refs):
    if any(v == FAIL for v in gates.values()):
        return "REJECT"
    if any(v in (UNKNOWN, STALE) for v in gates.values()):
        return "DATA_NOT_READY"
    if not evidence_refs:
        return "DATA_NOT_READY"
    if reviewer_status not in ("PASS", "PASS_WITH_WARNINGS"):
        return "DATA_NOT_READY"
    return "BUY"


def test_all_gates_and_review_pass():
    gates = {"gender": PASS, "size_110": PASS, "new": PASS,
             "price_cap": PASS, "identity": PASS, "stock": PASS}
    assert decide(gates, "PASS", ["ev-001"]) == "BUY"


def test_unknown_size_never_buys():
    gates = {"gender": PASS, "size_110": UNKNOWN, "new": PASS,
             "price_cap": PASS, "identity": PASS, "stock": PASS}
    assert decide(gates, "PASS", ["ev-001"]) == "DATA_NOT_READY"


def test_stale_stock_never_buys():
    gates = {"gender": PASS, "size_110": PASS, "new": PASS,
             "price_cap": PASS, "identity": PASS, "stock": STALE}
    assert decide(gates, "PASS", ["ev-001"]) == "DATA_NOT_READY"


def test_price_over_cap_rejects():
    gates = {"gender": PASS, "size_110": PASS, "new": PASS,
             "price_cap": FAIL, "identity": PASS, "stock": PASS}
    assert decide(gates, "PASS", ["ev-001"]) == "REJECT"


def test_listing_without_evidence_cannot_buy():
    gates = {"gender": PASS, "size_110": PASS, "new": PASS,
             "price_cap": PASS, "identity": PASS, "stock": PASS}
    assert decide(gates, "PASS", []) == "DATA_NOT_READY"


def test_independent_review_failure_blocks_buy():
    gates = {"gender": PASS, "size_110": PASS, "new": PASS,
             "price_cap": PASS, "identity": PASS, "stock": PASS}
    assert decide(gates, "FAIL", ["ev-001"]) == "DATA_NOT_READY"
