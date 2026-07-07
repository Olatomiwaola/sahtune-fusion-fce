"""ARCH-08 Fusion Compliance Kernel (docs/18 §1, §3–§7).

Sole fusion authority. For each MergeRequest:
  1. require >=2 DISTINCT object_ids (duplicate/self-merge refused, RC-001);
  2. require one pinned bundle version (mixed → quarantine RC-005,
     mixed_bundle_versions);
  3. C3 bidirectional parentage cross-check (mismatch → quarantine RC-001,
     unrecorded_parentage);
  4. exact-multiset covers() (no covering combination → block/segregate, RC-003);
  5. permit: atomic decision -> HWM label (ARCH-07) -> kernel-written
     parent_object_ids -> provenance link (the fusion-decision audit record IS the
     ARCH-09 record, kernel-only) -> audit.

Audit uses the existing writer/records unchanged: fusion-decision records for
permit/block, quarantine-class records (with optional detection_flags) for the
quarantine outcomes. No policy-decision record is fabricated for quarantines.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from fce_poc.audit.chain import load_records
from fce_poc.audit.records import new_record
from fce_poc.provenance import build_graph

from . import crosscheck, labels, permits

TS = {"ts": "2026-07-06T00:00:00Z", "clock_source": "injected"}
MERGE_RULE = "RULE-POL-002"  # docs/07 cross-domain merge rule (permit-if-covered / block)


@dataclass
class MergeParent:
    object_id: str
    classification_label: str
    domain_label: str
    release_caveat: list = field(default_factory=list)
    lifecycle_type: str = "normalized_observation"
    parent_object_ids: list = field(default_factory=list)
    bundle_version: str = "0.1.0"


@dataclass
class MergeRequest:
    parents: list
    mission: str
    output_lifecycle_type: str
    proposed_output_object_id: str


@dataclass
class MergeDecision:
    disposition: str
    reason_codes: list
    detection_flags: list
    output_object_id: object
    output_label: object
    audit_event: dict


def _covering_permit_id(request_tuples, merge_permits):
    from collections import Counter
    want = Counter(request_tuples)
    for permit in merge_permits:
        for combination in permit.get("permitted_combinations", []):
            if Counter(permits.canonical_tuple(c, d, cav) for (c, d, cav) in combination) == want:
                return permit.get("permit_id")
    return None


def _quarantine(writer, event_id, source_ids, reason_codes, detection_flags, bundle_version):
    detail = {"review_queue_ref": f"rq-{event_id}"}
    if detection_flags:
        detail["detection_flags"] = list(detection_flags)
    rec = new_record(
        audit_event_id=event_id, event_type="quarantine", event_timestamp=TS,
        actor_identity="krn", source_object_ids=source_ids, output_object_id=None,
        policy_bundle_version=bundle_version, policy_rule_ids=[], decision="quarantine",
        reason_codes=reason_codes, enforcement_action="quarantine", disposition="quarantine",
        event_detail=detail)
    return writer.append(rec)


def evaluate_merge(request, bundle, writer, event_id) -> MergeDecision:
    ids = [p.object_id for p in request.parents]
    bv = bundle.version

    # 1. >=2 distinct object_ids (duplicate / self-merge refused).
    if len(ids) < 2 or len(set(ids)) != len(ids):
        rec = _quarantine(writer, event_id, ids or ["UNKNOWN"], ["RC-001"], [], bv)
        return MergeDecision("quarantine", ["RC-001"], [], None, None, rec)

    # 2. single pinned bundle version.
    if len({p.bundle_version for p in request.parents}) > 1:
        rec = _quarantine(writer, event_id, ids, ["RC-005"], ["mixed_bundle_versions"], bv)
        return MergeDecision("quarantine", ["RC-005"], ["mixed_bundle_versions"], None, None, rec)

    # 3. C3 bidirectional parentage cross-check over ARCH-09 (provenance graph).
    graph = build_graph(load_records(writer.path))
    for parent in request.parents:
        ok, flag = crosscheck.check_parent(parent, graph)
        if not ok:
            rec = _quarantine(writer, event_id, ids, ["RC-001"], [flag], bv)
            return MergeDecision("quarantine", ["RC-001"], [flag], None, None, rec)

    # 4. exact-multiset covering combination.
    request_tuples = [
        permits.canonical_tuple(p.classification_label, p.domain_label, p.release_caveat)
        for p in request.parents
    ]
    if not permits.covers(request_tuples, bundle.merge_permits):
        rec = writer.append(new_record(
            audit_event_id=event_id, event_type="fusion-decision", event_timestamp=TS,
            actor_identity="krn", source_object_ids=ids, output_object_id=None,
            policy_bundle_version=bv, policy_rule_ids=[MERGE_RULE], decision="block",
            reason_codes=["RC-003"], enforcement_action="segregate", disposition="segregate",
            event_detail={"rc003_context": "no covering combination in the active bundle"}))
        return MergeDecision("segregate", ["RC-003"], [], None, None, rec)

    # 5. permit — atomic construction sequence.
    output_label = labels.hwm(
        [(p.classification_label, p.domain_label, p.release_caveat) for p in request.parents]
    )
    output_id = request.proposed_output_object_id
    permit_id = _covering_permit_id(request_tuples, bundle.merge_permits)
    rec = writer.append(new_record(
        audit_event_id=event_id, event_type="fusion-decision", event_timestamp=TS,
        actor_identity="krn", source_object_ids=ids, output_object_id=output_id,
        policy_bundle_version=bv, policy_rule_ids=[MERGE_RULE], decision="permit",
        reason_codes=[], enforcement_action="permit", disposition="permit",
        event_detail={"merge_permit_ref": permit_id}))
    return MergeDecision("permit", [], [], output_id, output_label, rec)
