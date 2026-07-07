"""Red-team hook tests for the fusion evaluator (docs/18 §9; RT-M5S9 dispositions)."""

from __future__ import annotations

from fce_poc.policy.attributes import InjectedClock
from fce_poc.audit.writer import AuditWriter
from fce_poc.fusion import MergeRequest, evaluate_merge
from test_vectors import _bundle, _parent  # same-dir helpers on sys.path


def test_rt_m5s9_01_combination_not_membership(tmp_path):
    """RT-M5S9-01: a permit enumerating [T1,T2] must NOT cover [T1,T1]."""
    # Two DISTINCT object ids, both tuple T_A = (PROJ-LEVEL-1, DOMAIN-A, [X]).
    req = MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-1", "DOMAIN-A"), _parent("B", "PROJ-LEVEL-1", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F")
    d = evaluate_merge(req, _bundle(), AuditWriter(tmp_path / "a.jsonl", InjectedClock(now=1)), "e-01")
    assert d.disposition == "segregate"
    assert d.reason_codes == ["RC-003"]


def test_rt_m5s9_02_superset_denied(tmp_path):
    """RT-M5S9-02: a superset re-request after segregation is still denied absent a covering combination."""
    bundle = _bundle()
    writer = AuditWriter(tmp_path / "a.jsonl", InjectedClock(now=1))
    evaluate_merge(MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-2", "DOMAIN-A"), _parent("B", "PROJ-LEVEL-2", "DOMAIN-B")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F1"),
        bundle, writer, "e-02a")
    d = evaluate_merge(MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-2", "DOMAIN-A"), _parent("B", "PROJ-LEVEL-2", "DOMAIN-B"),
                 _parent("C", "PROJ-LEVEL-1", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F2"),
        bundle, writer, "e-02b")
    assert d.disposition == "segregate"
    assert d.reason_codes == ["RC-003"]


def test_rt_m5s9_03_duplicate_id_and_tt_enumeration(tmp_path):
    """RT-M5S9-03: duplicate object_id refused fail-closed; [T,T] permitted only when explicitly enumerated."""
    bundle = _bundle()
    # (a) duplicate object_id → refuse (RC-001 path).
    wa = AuditWriter(tmp_path / "a.jsonl", InjectedClock(now=1))
    da = evaluate_merge(MergeRequest(
        parents=[_parent("A", "PROJ-LEVEL-3", "DOMAIN-A"), _parent("A", "PROJ-LEVEL-3", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F"),
        bundle, wa, "e-03a")
    assert da.disposition == "quarantine"
    assert da.reason_codes == ["RC-001"]
    # (b) two DISTINCT ids sharing tuple T_C = (PROJ-LEVEL-3, DOMAIN-A, [X]) → permitted (MP-TT enumerated).
    wb = AuditWriter(tmp_path / "b.jsonl", InjectedClock(now=1))
    db = evaluate_merge(MergeRequest(
        parents=[_parent("X", "PROJ-LEVEL-3", "DOMAIN-A"), _parent("Y", "PROJ-LEVEL-3", "DOMAIN-A")],
        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="F2"),
        bundle, wb, "e-03b")
    assert db.disposition == "permit"


def test_rt_m5s9_05_override_vs_quarantines():
    """RT-M5S9-05: override vs RC-005 quarantine and vs unrecorded_parentage quarantine → both rejected."""
    from fce_poc.policy import OverrideRequest, override_valid
    permitted_envelope = frozenset({"permit", "restrict", "route-to-higher-domain", "transform"})  # excludes quarantine
    override = OverrideRequest(authority_authenticated=True, reason_code="RC-007",
                               audit_signature_placeholder=True, expires_at_tick=200)
    clock = InjectedClock(now=100)
    assert override_valid(override, {"disposition": "quarantine", "reason_code": "RC-005"}, permitted_envelope, clock) is False
    assert override_valid(override, {"disposition": "quarantine", "reason_code": "RC-001"}, permitted_envelope, clock) is False
