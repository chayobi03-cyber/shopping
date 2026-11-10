"""Load and validate versioned shopping freshness policies."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from shopping.validators import GateResult, evaluate_freshness


REQUIRED_TTL_KEYS = {
    "price", "availability", "review_aggregate", "official_product_specification"
}


def validate_freshness_policy(policy: Mapping[str, Any]) -> dict[str, int]:
    ttl_values = policy.get("ttl_seconds")
    if not isinstance(ttl_values, Mapping):
        raise ValueError("freshness policy must contain a ttl_seconds object")
    missing = REQUIRED_TTL_KEYS.difference(ttl_values.keys())
    if missing:
        raise ValueError(f"freshness TTL values missing: {sorted(missing)}")
    normalized: dict[str, int] = {}
    for key in REQUIRED_TTL_KEYS:
        value = ttl_values[key]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"TTL for {key} must be a non-negative integer")
        normalized[key] = value
    skew = policy.get("clock_skew_tolerance_seconds", 60)
    if not isinstance(skew, int) or isinstance(skew, bool) or skew < 0:
        raise ValueError("clock skew tolerance must be a non-negative integer")
    normalized["clock_skew_tolerance_seconds"] = skew
    return normalized


def load_freshness_policy(path: str | Path | None = None) -> dict[str, int]:
    config_path = Path(path) if path else Path(__file__).resolve().parents[2] / "config" / "freshness.json"
    try:
        policy = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load freshness policy: {config_path}") from exc
    if not isinstance(policy, Mapping):
        raise ValueError("freshness policy root must be a JSON object")
    return validate_freshness_policy(policy)


def evaluate_policy_freshness(
    observed_at: str,
    data_class: str,
    *,
    now: str | None = None,
    policy_path: str | Path | None = None,
) -> GateResult:
    """Evaluate freshness using the committed TTL and clock-skew policy."""
    policy = load_freshness_policy(policy_path)
    if data_class not in REQUIRED_TTL_KEYS:
        return GateResult("UNKNOWN", "FRESHNESS_CLASS_UNKNOWN", f"Unsupported freshness class: {data_class}")
    return evaluate_freshness(
        observed_at,
        policy[data_class],
        now=now,
        allowed_clock_skew_seconds=policy["clock_skew_tolerance_seconds"],
    )
