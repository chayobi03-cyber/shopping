"""Load and validate versioned shopping policy configuration."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


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
    return normalized


def load_freshness_policy(path: str | Path | None = None) -> dict[str, int]:
    config_path = Path(path) if path else Path(__file__).resolve().parents[2] / "config" / "freshness.json"
    try:
        policy = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load freshness policy: {config_path}") from exc
    return validate_freshness_policy(policy)
