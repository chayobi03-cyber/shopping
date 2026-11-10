"""Tests exercise the production deterministic decision gate."""
from shopping.decision import REQUIRED_HARD_GATES, evaluate_candidate, evaluate_decision
from shopping.validators import GateResult, validate_independent_review

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
STALE = "STALE"


def clean_review():
    return validate_independent_review(
        "run-primary", "run-review", "PASS", ["PASS"], [], [["review-ev-001"]]
    )


def base_results():
    return {
        name: GateResult(PASS, "OK", f"{name} passed", (f"ev-{name}",))
        for name in REQUIRED_HARD_GATES
    }


def test_all_gates_and_review_pass():
    assert evaluate_decision(base_results(), clean_review()) == "BUY"


def test_unknown_size_never_buys():
    results = base_results()
    results["size_110"] = GateResult(UNKNOWN, "SIZE_UNKNOWN", "size unresolved")
    assert evaluate_decision(results, clean_review()) == "DATA_NOT_READY"


def test_stale_stock_never_buys():
    results = base_results()
    results["stock"] = GateResult(STALE, "STOCK_STALE", "stock observation stale")
    assert evaluate_decision(results, clean_review()) == "DATA_NOT_READY"


def test_price_over_cap_rejects():
    results = base_results()
    results["price_cap"] = GateResult(FAIL, "PRICE_CAP_EXCEEDED", "over budget", ("ev-price",))
    assert evaluate_decision(results, clean_review()) == "REJECT"


def test_passing_gate_without_its_own_evidence_cannot_buy():
    results = base_results()
    results["size_110"] = GateResult(PASS, "SIZE_PASS", "size passed", ())
    assert evaluate_decision(results, clean_review()) == "DATA_NOT_READY"


def test_independent_review_failure_blocks_buy():
    pending_review = GateResult(UNKNOWN, "REVIEW_PENDING", "review pending")
    assert evaluate_decision(base_results(), pending_review) == "DATA_NOT_READY"


def test_empty_gates_fail_closed():
    assert evaluate_decision({}, clean_review()) == "DATA_NOT_READY"


def test_missing_mandatory_gate_fails_closed():
    results = base_results()
    del results["size_110"]
    assert evaluate_decision(results, clean_review()) == "DATA_NOT_READY"


def test_unrecognized_mandatory_gate_state_fails_closed():
    results = base_results()
    results["stock"] = GateResult("UNRECOGNIZED", "BAD_STATUS", "invalid")
    assert evaluate_decision(results, clean_review()) == "DATA_NOT_READY"


def test_candidate_composition_requires_evidence_coverage_and_review():
    decision = evaluate_candidate(base_results(), clean_review())
    assert decision.decision == "BUY"
    assert decision.hard_gates["evidence_coverage"] == PASS
    assert "review-ev-001" in decision.evidence_refs


def test_candidate_composition_missing_evidence_coverage_is_not_ready():
    results = base_results()
    del results["evidence_coverage"]
    decision = evaluate_candidate(results, clean_review())
    assert decision.decision == "DATA_NOT_READY"


def test_candidate_composition_failed_review_blocks_buy():
    results = base_results()
    pending = GateResult(UNKNOWN, "REVIEW_PENDING", "review pending")
    decision = evaluate_candidate(results, pending)
    assert decision.decision == "DATA_NOT_READY"


def test_unvalidated_positive_review_cannot_authorize_buy():
    results = base_results()
    arbitrary_pass = GateResult(PASS, "ARBITRARY_PASS", "not independently validated", ("ev-review",))
    assert evaluate_decision(results, arbitrary_pass) == "DATA_NOT_READY"


def test_low_level_decision_gate_rejects_unvalidated_review_string():
    assert evaluate_decision(base_results(), "PASS") == "DATA_NOT_READY"


def test_plain_string_gate_cannot_authorize_buy():
    results = base_results()
    results["gender"] = "PASS"
    assert evaluate_decision(results, clean_review()) == "DATA_NOT_READY"
