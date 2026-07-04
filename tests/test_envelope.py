"""Envelope normalization tests (GDR-016 normalization identity)."""

from __future__ import annotations

import json

from conftest import load_fixture

from fce_poc.envelope import KNOWN_FIELDS, MANDATORY_FIELDS, MISSING, Envelope, normalize


def test_normalize_is_deterministic(valid_raw):
    # RULE-VAL-018 support: identical input yields an equal Envelope.
    assert normalize(valid_raw) == normalize(valid_raw)


def test_normalization_identity_fixture_vs_runtime(valid_raw):
    # GDR-016: the fixture-builder path and the runtime path use the SAME function.
    # A round-trip through JSON (the on-disk form) must normalize identically.
    round_tripped = json.loads(json.dumps(valid_raw))
    assert normalize(round_tripped) == normalize(valid_raw)


def test_valid_object_has_all_mandatory_fields_present(valid_raw):
    env = normalize(valid_raw)
    for name in MANDATORY_FIELDS:
        # policy_binding_state is FCE-authority-set and legitimately absent from source.
        if name == "policy_binding_state":
            continue
        assert getattr(env, name) is not MISSING, f"{name} should be present"


def test_absent_field_is_missing_sentinel():
    env = normalize({"object_id": "x"})
    assert env.object_id == "x"
    assert env.schema_version is MISSING


def test_null_is_preserved_and_distinct_from_missing():
    env = normalize({"release_caveat": None})
    # JSON null -> None, which must be distinguishable from an absent field.
    assert env.release_caveat is None
    assert env.release_caveat is not MISSING
    assert env.handling_instructions is MISSING


def test_empty_list_is_preserved():
    env = normalize({"parent_object_ids": []})
    assert env.parent_object_ids == []
    assert env.parent_object_ids is not None


def test_unknown_fields_are_captured_sorted():
    env = normalize({"zeta": 1, "alpha": 2, "object_id": "x"})
    assert env.unknown_fields == ("alpha", "zeta")


def test_known_companion_fields_are_not_unknown():
    raw = load_fixture("valid_object.json")
    env = normalize(raw)
    assert env.unknown_fields == ()
    # ai_confidence / clock_source / lifecycle_type are known, not unknown.
    for name in ("ai_confidence", "clock_source", "lifecycle_type"):
        assert name in KNOWN_FIELDS
