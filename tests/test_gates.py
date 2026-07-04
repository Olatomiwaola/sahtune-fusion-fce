"""G1 gate tests: policy_binding_state forcing and version/origin gate."""

from __future__ import annotations

from conftest import load_fixture

from fce_poc.envelope import normalize
from fce_poc.gates import (
    BINDING_STATE_DETECTION_FLAG,
    FORCED_BINDING_STATE,
    force_policy_binding_state,
    g1_version_origin_gate,
)


def test_forcing_sets_unvalidated_and_flags_source_supplied():
    # RULE-VAL-017 / B3: source-supplied 'validated' is forced to 'unvalidated'
    # and recorded as detected; the ingested value is never trusted.
    env = normalize(load_fixture("source_supplied_binding_state.json"))
    forced, flags = force_policy_binding_state(env)
    assert forced.policy_binding_state == FORCED_BINDING_STATE
    assert flags == (BINDING_STATE_DETECTION_FLAG,)


def test_forcing_without_source_value_sets_no_flag(valid_raw):
    # A well-formed object omits the FCE-authority-set field: forced, but not flagged.
    forced, flags = force_policy_binding_state(normalize(valid_raw))
    assert forced.policy_binding_state == FORCED_BINDING_STATE
    assert flags == ()


def test_forcing_overrides_any_ingested_value():
    # Forcing executes regardless of the ingested value (even a valid-looking one).
    env = normalize({"policy_binding_state": "quarantined"})
    forced, flags = force_policy_binding_state(env)
    assert forced.policy_binding_state == FORCED_BINDING_STATE
    assert flags == (BINDING_STATE_DETECTION_FLAG,)


def test_supported_version_and_allowed_origin_pass(valid_raw):
    gate = g1_version_origin_gate(normalize(valid_raw))
    assert gate.passed
    assert gate.failed_rules == ()


def test_unsupported_version_fails_rule_002():
    env = normalize(load_fixture("unsupported_version.json"))
    gate = g1_version_origin_gate(env)
    assert not gate.passed
    assert gate.failed_rules == ("RULE-VAL-002",)


def test_live_origin_fails_rule_003():
    env = normalize(load_fixture("live_data_origin.json"))
    gate = g1_version_origin_gate(env)
    assert not gate.passed
    assert gate.failed_rules == ("RULE-VAL-003",)


def test_allowed_origins_all_pass_gate(valid_raw):
    for origin in ("SYNTHETIC", "SYNTHETIC-DERIVED", "PUBLIC-OPEN-SOURCE"):
        raw = dict(valid_raw)
        raw["data_origin"] = origin
        gate = g1_version_origin_gate(normalize(raw))
        assert "RULE-VAL-003" not in gate.failed_rules


def test_unknown_origin_fails_gate(valid_raw):
    raw = dict(valid_raw)
    raw["data_origin"] = "MYSTERY"
    gate = g1_version_origin_gate(normalize(raw))
    assert gate.failed_rules == ("RULE-VAL-003",)
