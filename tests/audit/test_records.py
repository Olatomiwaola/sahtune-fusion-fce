"""Record schema tests: per-class emission, requiredness, sentinel legality, duplicate."""

from __future__ import annotations

import pytest

from fce_poc.policy.attributes import InjectedClock
from fce_poc.audit.records import EVENT_CLASSES, RecordValidationError, new_record, validate_record_body
from fce_poc.audit.writer import AuditWriter
from fce_poc.audit.chain import verify_chain

TS = {"ts": "2026-07-06T00:00:00Z", "clock_source": "injected"}
OID = "11111111-1111-4111-8111-111111111111"
OID2 = "22222222-2222-4222-8222-222222222222"
OUT = "33333333-3333-4333-8333-333333333333"


def valid_body(cls, **over):
    """Return new_record kwargs for a minimally valid record of the given class."""
    base = dict(
        audit_event_id=f"e0000000-0000-4000-8000-0000000000{EVENT_CLASSES.index(cls):02d}",
        event_type=cls, event_timestamp=TS, actor_identity="actor",
        source_object_ids=[OID], output_object_id=None, policy_bundle_version="0.1.0",
        policy_rule_ids=[], decision="x", reason_codes=[],
        enforcement_action="permit", disposition="permit", event_detail={},
    )
    per_class = {
        "ingestion": dict(policy_bundle_version="N/A-PRE-G4", event_detail={"ingest_attempt_id": "a0000000-0000-4000-8000-000000000001"}),
        "transformation": dict(output_object_id=OUT, enforcement_action="transform", disposition="transform", event_detail={"transformation_ref": "t"}),
        "policy-decision": dict(policy_rule_ids=["RULE-POL-001"], event_detail={"pip_attributes_consumed": [], "detection_flags": [], "deterministic_evaluation": True}),
        "fusion-decision": dict(source_object_ids=[OID, OID2], output_object_id=OUT, policy_rule_ids=["RULE-POL-001"], event_detail={"merge_permit_ref": "m"}),
        "routing": dict(output_object_id=OUT, policy_rule_ids=["RULE-POL-001"], enforcement_action="route-to-higher-domain", disposition="route-to-higher-domain", event_detail={"destination_domain": "DOMAIN-B"}),
        "quarantine": dict(reason_codes=["RC-005"], enforcement_action="quarantine", disposition="quarantine", event_detail={"review_queue_ref": "q1"}),
        "downgrade": dict(output_object_id=OUT, policy_rule_ids=["RULE-POL-001"], enforcement_action="downgrade", disposition="permit", event_detail={"authority_ref": "auth-1", "transformation_proof_ref": "proof-1"}),
        "export": dict(source_object_ids=[], policy_bundle_version="N/A-EXPORT", enforcement_action="permit", disposition="permit", event_detail={"manifest_ref": "m", "record_range": ["e1", "e2"], "manifest_sha256": "0" * 64}),
        "override": dict(policy_rule_ids=["RULE-POL-005"], enforcement_action="override", disposition="permit", event_detail={"precondition_results": {}, "envelope_check": True, "override_immutable_check": False}),
    }
    base.update(per_class[cls])
    base.update(over)
    return base


def test_t5_per_class_emission_nine_of_nine(tmp_path):  # T5 traces FCE-REQ-AUD-001
    writer = AuditWriter(tmp_path / "a.jsonl", InjectedClock(now=1))
    for cls in EVENT_CLASSES:
        writer.append(new_record(**valid_body(cls)))
    result = verify_chain(tmp_path / "a.jsonl")
    assert result.ok
    assert result.record_count == 9


def test_t6_requiredness_rejections():  # T6 traces FCE-DR-AUD-001 D2
    with pytest.raises(RecordValidationError):  # fusion with 1 parent
        validate_record_body(new_record(**valid_body("fusion-decision", source_object_ids=[OID])))
    with pytest.raises(RecordValidationError):  # ingestion missing ingest_attempt_id
        validate_record_body(new_record(**valid_body("ingestion", event_detail={})))
    with pytest.raises(RecordValidationError):  # unknown detail field
        validate_record_body(new_record(**valid_body("routing", event_detail={"destination_domain": "DOMAIN-B", "extra": 1})))
    with pytest.raises(RecordValidationError):  # malformed event_timestamp (missing sub-field)
        validate_record_body(new_record(**valid_body("policy-decision", event_timestamp={"ts": "2026-07-06T00:00:00Z"})))
    with pytest.raises(RecordValidationError):  # empty clock_source
        validate_record_body(new_record(**valid_body("policy-decision", event_timestamp={"ts": "2026-07-06T00:00:00Z", "clock_source": ""})))


def test_t7_sentinel_legality_rejections():  # T7 traces RT-M4S7-04
    with pytest.raises(RecordValidationError):  # N/A-PRE-G4 on policy-decision
        validate_record_body(new_record(**valid_body("policy-decision", policy_bundle_version="N/A-PRE-G4")))
    with pytest.raises(RecordValidationError):  # N/A-EXPORT on ingestion
        validate_record_body(new_record(**valid_body("ingestion", policy_bundle_version="N/A-EXPORT")))
    with pytest.raises(RecordValidationError):  # semver on export
        validate_record_body(new_record(**valid_body("export", policy_bundle_version="0.1.0")))


def test_t14_duplicate_object_id_quarantine_path(tmp_path):  # T14 traces FCE-DR-SCH-004 D5
    body = new_record(**valid_body(
        "ingestion", disposition="quarantine", enforcement_action="quarantine",
        reason_codes=["RC-001"],
        event_detail={"ingest_attempt_id": "a0000000-0000-4000-8000-0000000000dd",
                      "detection_flags": [f"duplicate_object_id:{OID}"]}))
    validate_record_body(body)  # accepted shape
    writer = AuditWriter(tmp_path / "a.jsonl", InjectedClock(now=1))
    rec = writer.append(body)
    assert rec["disposition"] == "quarantine"
    assert rec["reason_codes"] == ["RC-001"]
    assert f"duplicate_object_id:{OID}" in rec["event_detail"]["detection_flags"]
