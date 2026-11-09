"""Deterministic shopping recommendation gates.

This module is intentionally independent of LLM agents. It does not execute purchases.
"""
from __future__ import annotations

from typing import Mapping, Sequence

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
STALE = "STALE"


def evaluate_decision(
    hard_gates: Mapping[str, str],
    reviewer_status: str,
    evidence_refs: Sequence[str],
) -> str:
    """Return BUY/REJECT/DATA_NOT_READY using fail-closed semantics."""
    if not hard_gates:
        return "DATA_NOT_READY"
    if any(value == FAIL for value in hard_gates.values()):
        return "REJECT"
    if any(value not in (PASS,) for value in hard_gates.values()):
        return "DATA_NOT_READY"
    if not evidence_refs:
        return "DATA_NOT_READY"
    if reviewer_status not in ("PASS", "PASS_WITH_WARNINGS"):
        return "DATA_NOT_READY"
    return "BUY"
