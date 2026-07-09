"""FCE-DR-SCH-004 D5 — bounded per-run duplicate object_id detection (RT-M6S11-04).

A repeated object_id within one run fails closed to a `quarantined` disposition on
the existing RC-001 path, carrying a `duplicate_object_id:<id>` detection flag that
names the colliding id. First occurrences and unrelated validation are unchanged.

Trace: FCE-REQ-MET-010, FCE-DR-SCH-004 D5, docs/17 §5, docs/09 item S3.
"""
import json
from pathlib import Path

from fce_poc.taxonomy import load_taxonomy
from fce_poc.validator import evaluate, evaluate_batch

REPO = Path(__file__).resolve().parents[1]
TAX = load_taxonomy(REPO / "data" / "fixtures" / "calibration" / "taxonomy.json")
VAR = REPO / "data" / "fixtures" / "variants"
HELDOUT = REPO / "data" / "fixtures" / "heldout"


def _load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def test_duplicate_object_id_second_occurrence_quarantined():
    a = _load(VAR / "malformed_duplicate_id_a.json")
    b = _load(VAR / "malformed_duplicate_id_b.json")
    assert a["object_id"] == b["object_id"]  # duplicate pair by construction

    first, second = evaluate_batch([a, b], TAX)
    # first occurrence is unchanged (a plain valid-object accept)
    assert first.disposition == evaluate(a, TAX).disposition
    # second occurrence fails closed: quarantine, RC-001 path, flag names the colliding id
    assert second.disposition == "quarantined"
    assert second.reason_code == "RC-001"
    assert f"duplicate_object_id:{a['object_id']}" in second.detection_flags


def test_unique_object_ids_no_duplicate_flag():
    a = _load(VAR / "malformed_duplicate_id_a.json")
    other = _load(HELDOUT / "osd04_s2stac_heldout.json")[0]
    assert a["object_id"] != other["object_id"]

    dispositions = evaluate_batch([a, other], TAX)
    for d in dispositions:
        assert not any(f.startswith("duplicate_object_id") for f in d.detection_flags)


def test_evaluate_batch_does_not_change_single_object_behavior():
    a = _load(VAR / "malformed_duplicate_id_a.json")
    assert evaluate_batch([a], TAX)[0].disposition == evaluate(a, TAX).disposition
