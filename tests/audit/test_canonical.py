"""CANON-1 tests: determinism (T1) and float refusal (T2)."""

from __future__ import annotations

import pytest

from fce_poc.audit.canonical import FloatInHashDomain, canonical_bytes, sha256_hex


def test_t1_canonical_determinism_key_and_list_shuffle():  # T1 FCE-DR-SCH-004 D1 / FCE-REQ-POL-001
    a = {
        "audit_event_id": "e1", "reason_codes": ["RC-003", "RC-001"],
        "source_object_ids": ["b", "a"], "policy_rule_ids": ["RULE-POL-002", "RULE-POL-001"],
        "event_detail": {"release_caveat": ["Y", "X"], "parent_object_ids": ["2", "1"]},
    }
    b = {
        "event_detail": {"parent_object_ids": ["1", "2"], "release_caveat": ["X", "Y"]},
        "policy_rule_ids": ["RULE-POL-001", "RULE-POL-002"], "source_object_ids": ["a", "b"],
        "reason_codes": ["RC-001", "RC-003"], "audit_event_id": "e1",
    }
    assert canonical_bytes(a) == canonical_bytes(b)
    assert sha256_hex(a) == sha256_hex(b)


def test_t2_float_refused_anywhere():  # T2 D1(6)
    with pytest.raises(FloatInHashDomain):
        sha256_hex({"confidence": 0.87})
    with pytest.raises(FloatInHashDomain):
        sha256_hex({"event_detail": {"nested": [1, 2, 3.14]}})
    # integers, strings, bools, null are fine
    assert sha256_hex({"a": 1, "b": "x", "c": True, "d": None})
