"""Fusion merge evaluator — test vectors V1–V7 (docs/18 §8). One test per vector."""

from __future__ import annotations

from pathlib import Path

from fce_poc.policy.attributes import InjectedClock
from fce_poc.policy import load_bundle
from fce_poc.audit.writer import AuditWriter
from fce_poc.fusion import MergeParent, MergeRequest, evaluate_merge

REPO = Path(__file__).resolve().parents[2]
BUNDLE_PATH = REPO / "data" / "fixtures" / "policy" / "bundle_proj-baseline_0.2.0.json"


def _bundle():
    return load_bundle(BUNDLE_PATH)


def _writer(tmp_path, name="audit.jsonl"):
    return AuditWriter(tmp_path / name, InjectedClock(now=1000))


def _parent(oid, cls, dom, cav=None, lifecycle="normalized_observation", parents=None, ver="0.1.0"):
    return MergeParent(
        object_id=oid, classification_label=cls, domain_label=dom,
        release_caveat=cav or ["PROJ-CAVEAT-X"], lifecycle_type=lifecycle,
        parent_object_ids=parents or [], bundle_version=ver,
    )


def test_v1_permitted_same_domain_merge(tmp_path):
    """V1 — FCE-REQ-KRN-011, FCE-REQ-PRV-002: permitted 2-parent merge, HWM label, kernel-written parentage."""
    req = MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-1", "DOMAIN-A"), _parent("B", "PROJ-LEVEL-2", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F1")
    d = evaluate_merge(req, _bundle(), _writer(tmp_path), event_id="e-v1")
    assert d.disposition == "permit"
    assert d.output_object_id == "F1"
    assert d.output_label == ("PROJ-LEVEL-2", "DOMAIN-A", ["PROJ-CAVEAT-X"])  # high-water mark
    assert d.audit_event["event_type"] == "fusion-decision"
    assert d.audit_event["source_object_ids"] == ["A", "B"]  # kernel-written parentage
    assert d.audit_event["output_object_id"] == "F1"


def test_v2_blocked_cross_domain_merge(tmp_path):
    """V2 — FCE-REQ-KRN-011: no covering combination → RC-003, segregate, null output."""
    req = MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-2", "DOMAIN-A"), _parent("B", "PROJ-LEVEL-2", "DOMAIN-B")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F2")
    d = evaluate_merge(req, _bundle(), _writer(tmp_path), event_id="e-v2")
    assert d.disposition == "segregate"
    assert d.reason_codes == ["RC-003"]
    assert d.output_object_id is None
    assert d.audit_event["event_type"] == "fusion-decision"
    assert d.audit_event["output_object_id"] is None


def test_v3_self_declared_parentage_quarantined(tmp_path):
    """V3 — FCE-REQ-KRN-012: caller-supplied parentage (forward cross-check) → quarantine, unrecorded_parentage."""
    req = MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-1", "DOMAIN-A", lifecycle="tracklet", parents=["X"]),
                 _parent("B", "PROJ-LEVEL-2", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F3")
    d = evaluate_merge(req, _bundle(), _writer(tmp_path), event_id="e-v3")
    assert d.disposition == "quarantine"
    assert d.reason_codes == ["RC-001"]
    assert "unrecorded_parentage" in d.detection_flags
    assert "unrecorded_parentage" in d.audit_event["event_detail"]["detection_flags"]
    assert d.audit_event["event_type"] == "quarantine"


def test_v4_derived_empty_parents_refused(tmp_path):
    """V4 — FCE-REQ-KRN-012: derived-type object with empty parents → refused (field-13 backstop + kernel assert)."""
    req = MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-1", "DOMAIN-A", lifecycle="tracklet", parents=[]),
                 _parent("B", "PROJ-LEVEL-2", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F4")
    d = evaluate_merge(req, _bundle(), _writer(tmp_path), event_id="e-v4")
    assert d.disposition == "quarantine"
    assert "unrecorded_parentage" in d.detection_flags


def test_v5_mixed_bundle_versions_quarantined(tmp_path):
    """V5 — FCE-REQ-POL-012, FCE-REQ-POL-001: mixed pinned bundle versions → quarantine RC-005, mixed_bundle_versions."""
    req = MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-1", "DOMAIN-A", ver="0.1.0"),
                 _parent("B", "PROJ-LEVEL-2", "DOMAIN-A", ver="0.2.0")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F5")
    d = evaluate_merge(req, _bundle(), _writer(tmp_path), event_id="e-v5")
    assert d.disposition == "quarantine"
    assert d.reason_codes == ["RC-005"]
    assert "mixed_bundle_versions" in d.detection_flags
    assert "mixed_bundle_versions" in d.audit_event["event_detail"]["detection_flags"]


def test_v6_override_vs_rc003_rejected():
    """V6 — FCE-REQ-OPS-002: override attempt against V2's RC-003 block → rejected (override_immutable, B2)."""
    from fce_poc.policy import OverrideRequest, override_valid
    underlying = {"disposition": "segregate", "reason_code": "RC-003"}
    override = OverrideRequest(authority_authenticated=True, reason_code="RC-007",
                               audit_signature_placeholder=True, expires_at_tick=200)
    permitted_envelope = frozenset({"permit", "restrict", "route-to-higher-domain", "transform"})
    assert override_valid(override, underlying, permitted_envelope, InjectedClock(now=100)) is False


def test_v7_reverse_crosscheck_quarantined(tmp_path):
    """V7 — FCE-REQ-KRN-012: ARCH-09-known derivation output presenting as non-derived (reverse) → quarantine, unrecorded_parentage."""
    bundle = _bundle()
    writer = _writer(tmp_path)
    # Prior permitted merge creates derivation output F1 (recorded in ARCH-09/the chain).
    evaluate_merge(MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-1", "DOMAIN-A"), _parent("B", "PROJ-LEVEL-2", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F1"),
        bundle, writer, event_id="e-v7a")
    # F1 now presents as a NON-derived parent → reverse cross-check fails.
    req = MergeRequest(
        parents=[_parent("F1", "PROJ-LEVEL-2", "DOMAIN-A", lifecycle="normalized_observation", parents=[]),
                 _parent("C", "PROJ-LEVEL-1", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F7")
    d = evaluate_merge(req, bundle, writer, event_id="e-v7b")
    assert d.disposition == "quarantine"
    assert "unrecorded_parentage" in d.detection_flags
