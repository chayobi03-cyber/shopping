"""Deterministic shopping recommendation gates.

This module is independent of LLM agents and never executes purchases.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping

from shopping.validators import GateResult

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
STALE = "STALE"

REQUIRED_HARD_GATES = (
    "gender", "size_110", "new", "price_cap", "price_freshness",
    "identity", "stock", "evidence_coverage"
)


@dataclass(frozen=True)
class DecisionResult:
    decision: str
    hard_gates: Mapping[str, str]
    reviewer_status: str
    evidence_refs: tuple[str, ...]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict:
        value = asdict(self)
        value["evidence_refs"] = list(self.evidence_refs)
        value["reasons"] = list(self.reasons)
        return value


def evaluate_decision(
    hard_gate_results: Mapping[str, object],
    reviewer_result: object,
) -> str:
    """Return BUY/REJECT/DATA_NOT_READY; every passing gate needs its own evidence."""
    # A known hard failure is decisive even if other fields are still missing.
    if any(
        isinstance(hard_gate_results.get(name), GateResult)
        and hard_gate_results[name].status == FAIL
        and bool(hard_gate_results[name].evidence_refs)
        for name in REQUIRED_HARD_GATES
    ):
        return "REJECT"
    if not set(REQUIRED_HARD_GATES).issubset(hard_gate_results.keys()):
        return "DATA_NOT_READY"
    for name in REQUIRED_HARD_GATES:
        result = hard_gate_results[name]
        if not isinstance(result, GateResult):
            return "DATA_NOT_READY"
        if result.status != PASS or not result.evidence_refs:
            return "DATA_NOT_READY"
    if (
        not isinstance(reviewer_result, GateResult)
        or reviewer_result.status != PASS
        or reviewer_result.code != "REVIEW_INDEPENDENT_PASS"
        or not reviewer_result.evidence_refs
    ):
        return "DATA_NOT_READY"
    return "BUY"


def evaluate_candidate(
    validation_results: Mapping[str, object],
    reviewer_result: object,
) -> DecisionResult:
    """Combine typed validator outputs without trusting narrative agent scores."""
    gate_states: dict[str, str] = {}
    refs: set[str] = set()
    reasons: list[str] = []
    for name in REQUIRED_HARD_GATES:
        result = validation_results.get(name)
        if not isinstance(result, GateResult):
            gate_states[name] = UNKNOWN
            reasons.append(f"{name}: missing or untyped validation result")
            continue
        gate_states[name] = result.status if result.status in {PASS, FAIL, UNKNOWN, STALE} else UNKNOWN
        refs.update(result.evidence_refs)
        if result.message:
            reasons.append(f"{name}: {result.message}")
    if isinstance(reviewer_result, GateResult):
        refs.update(reviewer_result.evidence_refs)
        reviewer_status = PASS if (
            reviewer_result.status == PASS
            and reviewer_result.code == "REVIEW_INDEPENDENT_PASS"
            and reviewer_result.evidence_refs
        ) else UNKNOWN
    else:
        reviewer_status = UNKNOWN
    decision = evaluate_decision(validation_results, reviewer_result)
    if reviewer_status != PASS:
        reasons.append("Independent review has not passed with evidence.")
    return DecisionResult(decision, gate_states, reviewer_status, tuple(sorted(refs)), tuple(reasons))
