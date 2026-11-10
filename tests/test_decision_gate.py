"""Tests exercise the production deterministic decision gate."""
from shopping.decision import evaluate_candidate, evaluate_decision
from shopping.validators import GateResult

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
STALE = "STALE"


def base_gates():
    return {"gender": PASS, "size_110": PASS, "new": PASS,
            "price_cap": PASS, "identity": PASS, "stock": PASS, "evidence_coverage": PASS}


def test_all_gates_and_review_pass():
    assert evaluate_decision(base_gates(), "PASS", ["ev-001"]) == "BUY"


def test_unknown_size_never_buys():
    gates = base_gates()
    gates["size_110"] = UNKNOWN
    assert evaluate_decision(gates, "PASS", ["ev-001"]) == "DATA_NOT_READY"


def test_stale_stock_never_buys():
    gates = base_gates()
    gates["stock"] = STALE
    assert evaluate_decision(gates, "PASS", ["ev-001"]) == "DATA_NOT_READY"


def test_price_over_cap_rejects():
    gates = base_gates()
    gates["price_cap"] = FAIL
    assert evaluate_decision(gates, "PASS", ["ev-001"]) == "REJECT"


def test_listing_without_evidence_cannot_buy():
    assert evaluate_decision(base_gates(), "PASS", []) == "DATA_NOT_READY"


def test_independent_review_failure_blocks_buy():
    assert evaluate_decision(base_gates(), "FAIL", ["ev-001"]) == "DATA_NOT_READY"


def test_empty_gates_fail_closed():
    assert evaluate_decision({}, "PASS", ["ev-001"]) == "DATA_NOT_READY"


def test_missing_mandatory_gate_fails_closed():
    gates = base_gates()
    del gates["size_110"]
    assert evaluate_decision(gates, "PASS", ["ev-001"]) == "DATA_NOT_READY"


def test_unrecognized_mandatory_gate_state_fails_closed():
    gates = base_gates()
    gates["stock"] = "UNRECOGNIZED"
    assert evaluate_decision(gates, "PASS", ["ev-001"]) == "DATA_NOT_READY"


def test_candidate_composition_requires_evidence_coverage_and_review():
    results = {
        name: GateResult(PASS, "OK", "passed", ("ev-001",))
        for name in ["gender", "size_110", "new", "price_cap", "identity", "stock", "evidence_coverage"]
    }
    decision = evaluate_candidate(results, GateResult(PASS, "REVIEW_OK", "independent review passed"))
    assert decision.decision == "BUY"
    assert decision.hard_gates["evidence_coverage"] == PASS


def test_candidate_composition_missing_evidence_coverage_is_not_ready():
    results = {
        name: GateResult(PASS, "OK", "passed", ("ev-001",))
        for name in ["gender", "size_110", "new", "price_cap", "identity", "stock"]
    }
    decision = evaluate_candidate(results, GateResult(PASS, "REVIEW_OK", "independent review passed"))
    assert decision.decision == "DATA_NOT_READY"


def test_candidate_composition_failed_review_blocks_buy():
    results = {
        name: GateResult(PASS, "OK", "passed", ("ev-001",))
        for name in ["gender", "size_110", "new", "price_cap", "identity", "stock", "evidence_coverage"]
    }
    decision = evaluate_candidate(results, GateResult("UNKNOWN", "REVIEW_PENDING", "review pending"))
    assert decision.decision == "DATA_NOT_READY"
