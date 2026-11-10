import csv
import json

import pytest

from shopping.artifacts import (
    append_csv_observation,
    create_run_manifest,
    render_decision_report,
    validate_json_artifact,
    write_immutable_json,
)


ROOT = __file__
SCHEMAS = __import__("pathlib").Path(__file__).parents[1] / "schemas"


def valid_decision():
    gates = {name: "PASS" for name in (
        "gender", "size_110", "new", "price_cap", "price_freshness",
        "identity", "stock", "evidence_coverage"
    )}
    return {
        "decision_id": "dec-001",
        "product_variant_id": "variant-001",
        "as_of": "2026-11-10T09:00:00+09:00",
        "hard_gates": gates,
        "decision": "BUY",
        "evidence_refs": ["ev-001", "review-ev-001"],
        "review_status": "PASS"
    }


def test_run_manifest_is_schema_compatible():
    manifest = create_run_manifest("req-001", "feature/test", run_id="run-001")
    validate_json_artifact(manifest, SCHEMAS / "run-manifest.schema.json")


def test_write_immutable_json_validates_and_never_overwrites(tmp_path):
    path = write_immutable_json(
        tmp_path, "decisions/dec-001.json", valid_decision(),
        SCHEMAS / "decision.schema.json"
    )
    assert path.exists()
    assert json.loads(path.read_text(encoding="utf-8"))["decision"] == "BUY"
    with pytest.raises(FileExistsError):
        write_immutable_json(
            tmp_path, "decisions/dec-001.json", valid_decision(),
            SCHEMAS / "decision.schema.json"
        )


def test_write_immutable_json_rejects_invalid_snapshot(tmp_path):
    sample = valid_decision()
    sample["hard_gates"]["size_110"] = "UNKNOWN"
    with pytest.raises(Exception):
        write_immutable_json(tmp_path, "decision.json", sample, SCHEMAS / "decision.schema.json")


def test_artifact_path_cannot_escape_root(tmp_path):
    with pytest.raises(ValueError):
        write_immutable_json(tmp_path, "../escape.json", valid_decision(), SCHEMAS / "decision.schema.json")


def test_append_csv_observation_writes_header_and_prevents_duplicate(tmp_path):
    columns = ["observation_id", "seller", "price"]
    file_path = append_csv_observation(
        tmp_path, "offers/offers.csv", columns,
        {"observation_id": "obs-1", "seller": "official", "price": 29900},
        primary_key="observation_id"
    )
    with file_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [{"observation_id": "obs-1", "seller": "official", "price": "29900"}]
    with pytest.raises(ValueError):
        append_csv_observation(
            tmp_path, "offers/offers.csv", columns,
            {"observation_id": "obs-1", "seller": "official", "price": 28900},
            primary_key="observation_id"
        )


def test_append_csv_rejects_header_drift(tmp_path):
    append_csv_observation(
        tmp_path, "offers/offers.csv", ["id", "price"],
        {"id": "1", "price": 30000}, primary_key="id"
    )
    with pytest.raises(ValueError):
        append_csv_observation(
            tmp_path, "offers/offers.csv", ["id", "price", "seller"],
            {"id": "2", "price": 28000, "seller": "official"}, primary_key="id"
        )


def test_markdown_report_is_rendered_from_snapshot():
    report = render_decision_report(
        valid_decision(), {"brand": "TOPTEN", "model_name": "Fine Merino Cardigan"}
    )
    assert "# Shopping Decision — dec-001" in report
    assert "| size_110 | PASS |" in report
    assert "review-ev-001" in report
