"""G2 validator and end-to-end evaluation tests (LAP-UNIT-* + RULE-VAL-018).

Test-ID map to docs/16 Required Laptop Tests / docs/05_data_model/m2-poc-file-plan.md:
  LAP-UNIT-001 valid object accepted
  LAP-UNIT-002 missing mandatory metadata (incl. per-field variants) quarantined RC-001
  LAP-UNIT-003 source-supplied binding state forced + detected
  LAP-UNIT-004 unsupported version rejected before policy
  LAP-UNIT-006 data_origin=LIVE rejected fail-closed at G1
  LAP-UNIT-007 malformed values quarantined RC-001 (all failures reported)
  LAP-UNIT-008 PUBLIC-OPEN-SOURCE without manifest ref quarantined RC-001
  LAP-UNIT-009 null-vs-empty for release_caveat and parent_object_ids
RULE-VAL-018 determinism is asserted directly.
"""

from __future__ import annotations

import pytest

from conftest import load_fixture

from fce_poc.envelope import normalize
from fce_poc.gates import BINDING_STATE_DETECTION_FLAG
from fce_poc.validator import REASON_CODE_FAIL_CLOSED, UNKNOWN_FIELD_RULE, evaluate

# Field -> the rule that fires when that mandatory field is absent. schema_version and
# data_origin are rejected at G1 (not quarantined); policy_binding_state is
# FCE-authority-set and legitimately absent, so it is excluded from this map.
MISSING_FIELD_RULE = {
    "object_id": "RULE-VAL-001",
    "source_sensor_id": "RULE-VAL-006",
    "modality": "RULE-VAL-007",
    "acquisition_timestamp": "RULE-VAL-008",
    "clock_source": "RULE-VAL-008",
    "ingest_timestamp": "RULE-VAL-009",
    "classification_label": "RULE-VAL-010",
    "domain_label": "RULE-VAL-011",
    "release_caveat": "RULE-VAL-012",
    "handling_instructions": "RULE-VAL-013",
    "provenance_ref": "RULE-VAL-014",
    "parent_object_ids": "RULE-VAL-015",
    "integrity_hash": "RULE-VAL-016",
}


# --- LAP-UNIT-001 -----------------------------------------------------------

def test_lap_unit_001_valid_object_accepted(valid_raw, taxonomy):
    disp = evaluate(valid_raw, taxonomy)
    assert disp.disposition == "accepted"
    assert disp.reason_code is None
    assert disp.failed_rules == ()
    assert disp.synthetic_banner is True  # RULE-VAL-005
    assert disp.detection_flags == ()


# --- LAP-UNIT-002 -----------------------------------------------------------

def test_lap_unit_002_missing_field_quarantined(taxonomy):
    disp = evaluate(load_fixture("missing_field.json"), taxonomy)
    assert disp.disposition == "quarantined"
    assert disp.reason_code == REASON_CODE_FAIL_CLOSED
    assert "RULE-VAL-013" in disp.failed_rules  # handling_instructions omitted


@pytest.mark.parametrize("field_name,rule", sorted(MISSING_FIELD_RULE.items()))
def test_lap_unit_002_per_field_variants(valid_raw, taxonomy, field_name, rule):
    # Remove one mandatory field at a time; each must trip its mapped rule and
    # quarantine RC-001.
    raw = dict(valid_raw)
    del raw[field_name]
    disp = evaluate(raw, taxonomy)
    assert disp.disposition == "quarantined"
    assert disp.reason_code == REASON_CODE_FAIL_CLOSED
    assert rule in disp.failed_rules


# --- LAP-UNIT-003 -----------------------------------------------------------

def test_lap_unit_003_source_supplied_binding_state(taxonomy):
    disp = evaluate(load_fixture("source_supplied_binding_state.json"), taxonomy)
    # Forced to unvalidated at G1, detection recorded; object otherwise valid.
    assert disp.disposition == "accepted"
    assert disp.detection_flags == (BINDING_STATE_DETECTION_FLAG,)


# --- LAP-UNIT-004 -----------------------------------------------------------

def test_lap_unit_004_unsupported_version_rejected(taxonomy):
    disp = evaluate(load_fixture("unsupported_version.json"), taxonomy)
    assert disp.disposition == "rejected"  # before policy, never reaches G2
    assert disp.failed_rules == ("RULE-VAL-002",)


# --- LAP-UNIT-006 -----------------------------------------------------------

def test_lap_unit_006_live_origin_rejected_fail_closed(taxonomy):
    disp = evaluate(load_fixture("live_data_origin.json"), taxonomy)
    assert disp.disposition == "rejected"
    assert disp.failed_rules == ("RULE-VAL-003",)
    assert disp.synthetic_banner is False


# --- LAP-UNIT-007 -----------------------------------------------------------

def test_lap_unit_007_malformed_values_quarantined(taxonomy):
    disp = evaluate(load_fixture("malformed_types.json"), taxonomy)
    assert disp.disposition == "quarantined"
    assert disp.reason_code == REASON_CODE_FAIL_CLOSED
    # ALL failures reported, no first-failure short-circuit (multi-failure determinism).
    expected = {
        "RULE-VAL-001",  # bad uuid
        "RULE-VAL-006",  # empty source_sensor_id
        "RULE-VAL-007",  # unknown modality
        "RULE-VAL-008",  # bad acquisition ts + empty clock_source
        "RULE-VAL-009",  # bad ingest ts
        "RULE-VAL-010",  # unknown classification
        "RULE-VAL-011",  # unknown domain
        "RULE-VAL-012",  # release_caveat not a list
        "RULE-VAL-013",  # empty handling_instructions
        "RULE-VAL-014",  # provenance_ref has whitespace
        "RULE-VAL-015",  # parent_object_ids contains bad uuid
        "RULE-VAL-016",  # bad integrity_hash format
    }
    assert expected.issubset(set(disp.failed_rules))
    assert len(disp.failed_rules) >= len(expected)


# --- LAP-UNIT-008 -----------------------------------------------------------

def test_lap_unit_008_open_source_missing_manifest_quarantined(taxonomy):
    disp = evaluate(load_fixture("open_source_missing_manifest.json"), taxonomy)
    assert disp.disposition == "quarantined"
    assert disp.reason_code == REASON_CODE_FAIL_CLOSED
    assert "RULE-VAL-004" in disp.failed_rules
    assert disp.synthetic_banner is False  # PUBLIC-OPEN-SOURCE is not a synthetic origin


# --- LAP-UNIT-009 -----------------------------------------------------------

def test_lap_unit_009_null_release_caveat_fails(valid_raw, taxonomy):
    raw = dict(valid_raw)
    raw["release_caveat"] = None
    disp = evaluate(raw, taxonomy)
    assert disp.disposition == "quarantined"
    assert "RULE-VAL-012" in disp.failed_rules


def test_lap_unit_009_null_parent_object_ids_fails(valid_raw, taxonomy):
    raw = dict(valid_raw)
    raw["parent_object_ids"] = None
    disp = evaluate(raw, taxonomy)
    assert disp.disposition == "quarantined"
    assert "RULE-VAL-015" in disp.failed_rules


def test_lap_unit_009_empty_lists_accepted(valid_raw, taxonomy):
    raw = dict(valid_raw)
    raw["release_caveat"] = []          # empty list permitted
    raw["parent_object_ids"] = []       # empty permitted for normalized_observation
    disp = evaluate(raw, taxonomy)
    assert disp.disposition == "accepted"


def test_derived_lifecycle_requires_nonempty_parents(valid_raw, taxonomy):
    raw = dict(valid_raw)
    raw["lifecycle_type"] = "tracklet"  # derived: parent_object_ids must be non-empty
    raw["parent_object_ids"] = []
    disp = evaluate(raw, taxonomy)
    assert "RULE-VAL-015" in disp.failed_rules

    raw["parent_object_ids"] = ["3f2504e0-4f89-41d3-9a0c-0305e82c3399"]
    assert evaluate(raw, taxonomy).disposition == "accepted"


# --- interim unknown-field handling (RT-M2S3-03) ----------------------------

def test_unknown_field_fails_closed_interim(valid_raw, taxonomy):
    raw = dict(valid_raw)
    raw["smuggled"] = "payload"
    disp = evaluate(raw, taxonomy)
    assert disp.disposition == "quarantined"
    assert UNKNOWN_FIELD_RULE in disp.failed_rules


# --- RULE-VAL-016 format-only / verification deferred ------------------------

def test_integrity_hash_format_only(valid_raw, taxonomy):
    # A well-formed sha-256 passes the format check even though verification is
    # explicitly deferred; a malformed hash fails RULE-VAL-016.
    assert evaluate(valid_raw, taxonomy).disposition == "accepted"
    raw = dict(valid_raw)
    raw["integrity_hash"] = "deadbeef"  # too short -> format failure
    assert "RULE-VAL-016" in evaluate(raw, taxonomy).failed_rules


# --- RULE-VAL-018 determinism -----------------------------------------------

def test_rule_val_018_determinism_accepted(valid_raw, taxonomy):
    assert evaluate(valid_raw, taxonomy) == evaluate(valid_raw, taxonomy)


def test_rule_val_018_determinism_multifailure(taxonomy):
    raw = load_fixture("malformed_types.json")
    first = evaluate(raw, taxonomy)
    second = evaluate(raw, taxonomy)
    assert first == second
    assert first.failed_rules == second.failed_rules  # identical order (sorted)
