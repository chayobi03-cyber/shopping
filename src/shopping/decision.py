"""Deterministic shopping recommendation gates.

This module is intentionally independent of LLM agents. It does not execute purchases.
"""
from __future__ import annotations

from typing import Mapping, Sequence

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
STALE = "STALE"

REQUIRED_HARD_GATES = frozenset({
    "gender", "size_110", "new", "price_cap", "identity", "stock"
})


def evaluate_decision(
    hard_gates: Mapping[str, str],
    reviewer_status: str,
    evidence_refs: Sequence[str],
) -> str:
    """Return BUY/REJECT/DATA_NOT_READY using fail-closed semantics.

    All mandatory gates must be present and PASS. Any explicit hard failure
    rejects the candidate; missing, stale, or unrecognized states fail closed.
    """
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
