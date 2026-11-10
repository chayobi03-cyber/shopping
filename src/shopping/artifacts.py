"""Versioned artifact writers for reproducible shopping research runs."""
from __future__ import annotations

import csv
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
from uuid import uuid4

from jsonschema import Draft202012Validator, FormatChecker


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_run_manifest(
    request_id: str,
    branch: str,
    *,
    agents: Sequence[Mapping[str, Any]] = (),
    artifact_refs: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
    decision_refs: Sequence[str] = (),
    status: str = "RUNNING",
    run_id: str | None = None,
    commit_sha: str | None = None,
) -> dict[str, Any]:
    """Create a schema-compatible run manifest; callers finalize status/time later."""
    if not request_id or not branch:
        raise ValueError("request_id and branch are required")
    if status not in {"RUNNING", "COMPLETED", "FAILED", "DATA_NOT_READY", "BLOCKED"}:
        raise ValueError("Invalid run status")
    return {
        "run_id": run_id or f"run-{uuid4().hex}",
        "request_id": request_id,
        "started_at": utc_now_iso(),
        "completed_at": None,
        "status": status,
        "branch": branch,
        "commit_sha": commit_sha,
        "agents": [dict(agent) for agent in agents],
        "artifact_refs": list(artifact_refs),
        "evidence_refs": sorted(set(evidence_refs)),
        "decision_refs": sorted(set(decision_refs)),
        "notes": [],
    }


def _safe_destination(root: str | Path, relative_path: str | Path) -> tuple[Path, Path]:
    root_path = Path(root).resolve()
    relative = Path(relative_path)
    if relative.is_absolute():
        raise ValueError("Artifact path must be relative to the data root")
    destination = (root_path / relative).resolve()
    if destination == root_path or root_path not in destination.parents:
        raise ValueError("Artifact path escapes the configured data root")
    return root_path, destination


def validate_json_artifact(payload: Mapping[str, Any], schema_path: str | Path) -> None:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(dict(payload))


def write_immutable_json(
    root: str | Path,
    relative_path: str | Path,
    payload: Mapping[str, Any],
    schema_path: str | Path,
) -> Path:
    """Validate and atomically create a JSON artifact; never overwrite an existing snapshot."""
    _, destination = _safe_destination(root, relative_path)
    validate_json_artifact(payload, schema_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f"Immutable artifact already exists: {destination}")
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix=f".{destination.name}.", suffix=".tmp", delete=False
        ) as handle:
            temp_name = handle.name
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        # Hard-link creation is atomic and fails if another writer already created the target.
        os.link(temp_name, destination)
    except FileExistsError:
        raise
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
    return destination


def append_csv_observation(
    root: str | Path,
    relative_path: str | Path,
    fieldnames: Sequence[str],
    row: Mapping[str, Any],
    *,
    primary_key: str,
) -> Path:
    """Append a single observation, rejecting schema drift and duplicate observation IDs.

    Writers must be serialized by the orchestrator. This function does not claim
    multi-process locking or transactional database semantics.
    """
    if not fieldnames or len(set(fieldnames)) != len(fieldnames):
        raise ValueError("CSV fieldnames must be non-empty and unique")
    if primary_key not in fieldnames:
        raise ValueError("primary_key must be one of the CSV columns")
    if set(row.keys()) != set(fieldnames):
        raise ValueError("CSV row keys must exactly match the declared columns")
    if row.get(primary_key) in (None, ""):
        raise ValueError("CSV primary key value is required")
    _, destination = _safe_destination(root, relative_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    exists = destination.exists()
    if exists:
        with destination.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != list(fieldnames):
                raise ValueError("Existing CSV header does not match declared schema")
            for existing in reader:
                if existing.get(primary_key) == str(row[primary_key]):
                    raise ValueError(f"Duplicate CSV primary key: {row[primary_key]}")
    with destination.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="raise")
        if not exists:
            writer.writeheader()
        writer.writerow({key: row[key] for key in fieldnames})
    return destination


def render_decision_report(
    decision_snapshot: Mapping[str, Any],
    product_summary: Mapping[str, Any],
) -> str:
    """Render a compact Markdown report from structured decision inputs."""
    gates = decision_snapshot.get("hard_gates", {})
    evidence_refs = decision_snapshot.get("evidence_refs", [])
    decision = decision_snapshot.get("decision", "DATA_NOT_READY")
    lines = [
        f"# Shopping Decision — {decision_snapshot.get('decision_id', 'UNASSIGNED')}",
        "",
        f"- **Decision:** {decision}",
        f"- **Product:** {product_summary.get('brand', 'Unknown')} {product_summary.get('model_name', 'Unknown')}",
        f"- **Variant ID:** {decision_snapshot.get('product_variant_id', 'Unknown')}",
        f"- **As of:** {decision_snapshot.get('as_of', 'Unknown')}",
        f"- **Review:** {decision_snapshot.get('review_status', 'NOT_REVIEWED')}",
        "",
        "## Hard gates",
        "",
        "| Gate | Status |",
        "|---|---|",
    ]
    for key in sorted(gates):
        lines.append(f"| {key} | {gates[key]} |")
    lines.extend(["", "## Evidence references", ""])
    lines.extend([f"- {ref}" for ref in sorted(set(evidence_refs))] or ["- None recorded"])
    notes = decision_snapshot.get("notes", [])
    lines.extend(["", "## Notes", ""])
    lines.extend([f"- {note}" for note in notes] or ["- None"])
    lines.append("")
    return "\n".join(lines)
