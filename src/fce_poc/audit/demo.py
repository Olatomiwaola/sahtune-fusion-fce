"""Deterministic sample-chain generator (judgment: a demo module under audit/).

Produces a small chain covering: accepted ingestion (+ policy-decision), a G1 reject
(RC-011 mechanism-simulated, attempt-ID identity, with a poisoning source_asserted_
object_id), a transformation, a permitted fusion (2 parents), a blocked cross-domain
merge (RC-003), and an export record carrying the manifest sha-256. Chain verifies R1+R2.

All ids are fixed and the clock is injected, so the emitted JSONL is byte-deterministic.
Non-decision events (ingestion-accept, transformation, export) carry a neutral
disposition/enforcement drawn from the closed sets (ENGINEERING JUDGMENT — EVD-M4).
"""

from __future__ import annotations

from pathlib import Path

from fce_poc.policy.attributes import InjectedClock

from .export import export_package
from .records import new_record
from .writer import AuditWriter

TS = {"ts": "2026-07-06T00:00:00Z", "clock_source": "injected"}

OBJ_A = "11111111-1111-4111-8111-111111111111"
OBJ_B = "22222222-2222-4222-8222-222222222222"
OBJ_T = "33333333-3333-4333-8333-333333333333"
OBJ_F = "44444444-4444-4444-8444-444444444444"
ATTEMPT_A = "a0000000-0000-4000-8000-000000000001"
ATTEMPT_B = "a0000000-0000-4000-8000-000000000002"
ATTEMPT_R = "a0000000-0000-4000-8000-0000000000ff"


def build_sample(audit_path, export_dir, clock=None) -> list:
    clock = clock or InjectedClock(now=1000)
    audit_path = Path(audit_path)
    if audit_path.exists():
        audit_path.unlink()
    writer = AuditWriter(audit_path, clock)

    # 1-2: accepted ingestions (trusted origins).
    writer.append(new_record(
        audit_event_id="e0000000-0000-4000-8000-000000000001", event_type="ingestion",
        event_timestamp=TS, actor_identity="svc-ingest", source_object_ids=[OBJ_A],
        output_object_id=None, policy_bundle_version="N/A-PRE-G4", policy_rule_ids=[],
        decision="accept", reason_codes=[], enforcement_action="permit", disposition="permit",
        event_detail={"ingest_attempt_id": ATTEMPT_A, "object_id_authenticated": True}))
    writer.append(new_record(
        audit_event_id="e0000000-0000-4000-8000-000000000002", event_type="ingestion",
        event_timestamp=TS, actor_identity="svc-ingest", source_object_ids=[OBJ_B],
        output_object_id=None, policy_bundle_version="N/A-PRE-G4", policy_rule_ids=[],
        decision="accept", reason_codes=[], enforcement_action="permit", disposition="permit",
        event_detail={"ingest_attempt_id": ATTEMPT_B, "object_id_authenticated": True}))

    # 3: policy-decision (permit) on OBJ_A.
    writer.append(new_record(
        audit_event_id="e0000000-0000-4000-8000-000000000003", event_type="policy-decision",
        event_timestamp=TS, actor_identity="pdp", source_object_ids=[OBJ_A],
        output_object_id=None, policy_bundle_version="0.1.0", policy_rule_ids=["RULE-POL-001"],
        decision="permit", reason_codes=[], enforcement_action="permit", disposition="permit",
        event_detail={"pip_attributes_consumed": [["mission", True]], "detection_flags": [],
                      "deterministic_evaluation": True}))

    # 4: G1 reject (RC-011 mechanism-simulated), attempt-ID identity, poisoning asserted id.
    writer.append(new_record(
        audit_event_id="e0000000-0000-4000-8000-000000000004", event_type="ingestion",
        event_timestamp=TS, actor_identity="svc-ingest", source_object_ids=[],
        output_object_id=None, policy_bundle_version="N/A-PRE-G4", policy_rule_ids=[],
        decision="reject", reason_codes=["RC-011"], enforcement_action="reject", disposition="reject",
        event_detail={"ingest_attempt_id": ATTEMPT_R, "source_asserted_object_id": OBJ_A,
                      "object_id_authenticated": False}))

    # 5: transformation OBJ_A -> OBJ_T.
    writer.append(new_record(
        audit_event_id="e0000000-0000-4000-8000-000000000005", event_type="transformation",
        event_timestamp=TS, actor_identity="svc-transform", source_object_ids=[OBJ_A],
        output_object_id=OBJ_T, policy_bundle_version="0.1.0", policy_rule_ids=[],
        decision="transform", reason_codes=[], enforcement_action="transform", disposition="transform",
        event_detail={"transformation_ref": "xform-1"}))

    # 6: permitted fusion OBJ_A + OBJ_B -> OBJ_F.
    writer.append(new_record(
        audit_event_id="e0000000-0000-4000-8000-000000000006", event_type="fusion-decision",
        event_timestamp=TS, actor_identity="krn", source_object_ids=[OBJ_A, OBJ_B],
        output_object_id=OBJ_F, policy_bundle_version="0.1.0", policy_rule_ids=["RULE-POL-001"],
        decision="permit", reason_codes=[], enforcement_action="permit", disposition="permit",
        event_detail={"merge_permit_ref": "mp-1"}))

    # 7: blocked cross-domain merge (RC-003, segregate).
    writer.append(new_record(
        audit_event_id="e0000000-0000-4000-8000-000000000007", event_type="fusion-decision",
        event_timestamp=TS, actor_identity="krn", source_object_ids=[OBJ_A, OBJ_B],
        output_object_id=None, policy_bundle_version="0.1.0", policy_rule_ids=["RULE-POL-002"],
        decision="block", reason_codes=["RC-003"], enforcement_action="segregate", disposition="segregate",
        event_detail={"rc003_context": "domain mismatch DOMAIN-A vs DOMAIN-B"}))

    # 8: export record carrying the manifest sha-256.
    result = export_package(audit_path, export_dir, clock, package_id="PKG-SAMPLE-001")
    writer.append(new_record(
        audit_event_id="e0000000-0000-4000-8000-000000000008", event_type="export",
        event_timestamp=TS, actor_identity="svc-export", source_object_ids=[],
        output_object_id=None, policy_bundle_version="N/A-EXPORT", policy_rule_ids=[],
        decision="export", reason_codes=[], enforcement_action="permit", disposition="permit",
        export_status="exported",
        event_detail={"manifest_ref": "manifest.json",
                      "record_range": [result.manifest["first_event_id"], result.manifest["last_event_id"]],
                      "manifest_sha256": result.manifest_sha256}))

    from .chain import load_records
    return load_records(audit_path)


if __name__ == "__main__":
    import tempfile

    from .chain import verify_chain
    from .replay import reconstruct

    sample = Path("evidence/laptop-poc/audit_sample.jsonl")
    sample.parent.mkdir(parents=True, exist_ok=True)
    export_dir = Path(tempfile.mkdtemp(prefix="fce-audit-export-"))
    records = build_sample(sample, export_dir, InjectedClock(now=1000))
    r1 = verify_chain(sample)
    rp = reconstruct(sample)
    print(f"wrote {sample} ({len(records)} records)")
    print(f"R1 ok={r1.ok} count={r1.record_count}")
    print(f"R2 ok={rp.ok} r1_ok={rp.r1_ok} errors={rp.errors} decisions={len(rp.decisions)}")
    print("event_types:", [r["event_type"] for r in records])
    print(f"export package (scratch, not committed): {export_dir}")
