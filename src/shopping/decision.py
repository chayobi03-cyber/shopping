"""Deterministic shopping recommendation gates.

This module is independent of LLM agents and never executes purchases.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping, Sequence

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
STALE = "STALE"

REQUIRED_HARD_GATES = frozenset({
    "gender", "size_110", "new", "price_cap", "price_freshness", "identity", "stock", "evidence_coverage"
})


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
    hard_gates: Mapping[str, str],
    reviewer_status: str,
    evidence_refs: Sequence[str],
) -> str:
    """Return BUY/REJECT/DATA_NOT_READY using fail-closed semantics."""
    if not REQUIRED_HARD_GATES.issubset(hard_gates.keys()):
        return "DATA_NOT_READY"
    if any(hard_gates[name] == FAIL for name in REQUIRED_HARD_GATES):
        return "REJECT"
    if any(hard_gates[name] != PASS for name in REQUIRED_HARD_GATES):
        return "DATA_NOT_READY"
    if not evidence_refs:
        return "DATA_NOT_READY"
    if reviewer_status not in ("PASS", "PASS_WITH_WARNINGS"):
        return "DATA_NOT_READY"
    return "BUY"


def evaluate_candidate(
    validation_results: Mapping[str, object],
    reviewer_result: object,
) -> DecisionResult:
    """Combine GateResult-like outputs without trusting narrative agent scores.

    validation_results must contain each required gate key and objects with a
    status, evidence_refs, and message attribute (as produced by validators.py).
    reviewer_result must be a validated review GateResult. A non-PASS review
    blocks BUY but does not silently convert an unknown product fact into FAIL.
    """
    gates: dict[str, str] = {}
    refs: set[str] = set()
    reasons: list[str] = []
    for name in REQUIRED_HARD_GATES:
        result = validation_results.get(name)
        if result is None:
            gates[name] = UNKNOWN
            reasons.append(f"{name}: missing validation result")
            continue
        status = getattr(result, "status", UNKNOWN)
        gates[name] = status if status in {PASS, FAIL, UNKNOWN, STALE} else UNKNOWN
        refs.update(getattr(result, "evidence_refs", ()) or ())
        message = getattr(result, "message", "")
        if message:
            reasons.append(f"{name}: {message}")
    reviewer_status = getattr(reviewer_result, "status", UNKNOWN)
    reviewer_code = getattr(reviewer_result, "code", "")
    reviewer_status = PASS if reviewer_status == PASS and reviewer_code == "REVIEW_INDEPENDENT_PASS" else UNKNOWN
    decision = evaluate_decision(gates, reviewer_status, sorted(refs))
    if reviewer_status != PASS:
        reasons.append("Independent review has not passed.")
    return DecisionResult(decision, gates, reviewer_status, tuple(sorted(refs)), tuple(reasons))
