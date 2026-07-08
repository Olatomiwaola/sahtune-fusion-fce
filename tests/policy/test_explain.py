"""TST-EXP-001..004 — FCE-REQ-OPS-001 explanation surface (ARCH-13, render-only).

Unit tests over the pure explain()/explain_text() surface. They construct
representative evaluator-record dicts (the shape evaluate() returns) and assert
the explanation re-presents already-decided fields. No new decision logic; no
engine wiring — the integration flavour is exercised on real evaluate() output
in the Layer-2 held-out run.

Trace: FCE-REQ-OPS-001, docs/17 §3f, docs/09 item 2.4, FCE-REQ-KRN-002.
"""
import pytest

from fce_poc.policy.explain import explain, explain_text


def _decision(**over):
    base = {
        "input_object_ids": ["obj-1"],
        "pip_attributes_consumed": [{"id": "clearance", "auth": "unauthenticated"}],
        "bundle_version": "0.2.0",
        "rules_fired": ["RULE-POL-001"],
        "disposition": "permit",
        "reason_codes": [],
        "enforcement_action": "permit",
        "detection_flags": [],
        "evaluation_timestamp": {"ts": "2026-07-08T00:00:00Z", "clock_source": "injected"},
        "deterministic_evaluation": True,
    }
    base.update(over)
    return base


def test_exp_001_lists_rules_attrs_decision_reason():
    e = explain(
        _decision(
            disposition="reject",
            enforcement_action="reject",
            reason_codes=["RC-008"],
            rules_fired=["RULE-G4-PIP"],
        )
    )
    assert e["rules_fired"] == ["RULE-G4-PIP"]
    assert e["disposition"] == "reject"
    assert e["enforcement_action"] == "reject"
    assert e["reason_codes"] == ["RC-008"]
    assert e["pip_attributes_consumed"][0]["auth"] == "unauthenticated"
    txt = explain_text(_decision(reason_codes=["RC-008"], rules_fired=["RULE-G4-PIP"]))
    assert "RC-008" in txt and "RULE-G4-PIP" in txt


def test_exp_002_partial_permit_subset_via_rules_not_event_detail():
    # item 2.4: restrict/partial-permit — subset cited via rules_fired, reason_codes
    # empty, and the surface has no permitted_channels (RT-M6S11-01).
    d = _decision(
        disposition="restrict",
        enforcement_action="restrict",
        reason_codes=[],
        rules_fired=["RULE-POL-001", "MP-CHANNEL-SUBSET"],
    )
    e = explain(d)
    assert e["disposition"] == "restrict"
    assert e["reason_codes"] == []
    assert "MP-CHANNEL-SUBSET" in e["rules_fired"]
    assert "permitted_channels" not in e


def test_exp_003_block_names_immunity_without_override_path():
    d = _decision(
        disposition="block",
        enforcement_action="block",
        reason_codes=["RC-003"],
        rules_fired=["RULE-POL-002"],
    )
    e = explain(d)
    assert e["disposition"] == "block"
    assert "RC-003" in e["reason_codes"]
    assert "override" not in explain_text(d).lower()


def test_exp_004_cites_deterministic_rule_id():
    d = _decision(rules_fired=["RULE-POL-001"], deterministic_evaluation=True)
    e = explain(d)
    assert e["rules_fired"]
    assert e["deterministic_evaluation"] is True


def test_exp_fail_closed_on_missing_field():
    bad = _decision()
    del bad["disposition"]
    with pytest.raises(KeyError):
        explain(bad)
