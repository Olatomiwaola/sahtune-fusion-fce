"""TST-FUS-S4 — Scenario 4 fused-track positive merge (docs/17 §4 Resolution).

Two S4 observations (eo_ir L1 + uas_telemetry L2, DOMAIN-A, [PROJ-CAVEAT-X]) merge
under the sealed proj-baseline@0.2.0 via MP-V1-SAME-DOMAIN: permit; HWM output label
(PROJ-LEVEL-2, DOMAIN-A, [PROJ-CAVEAT-X]); kernel-written parentage equal to the two
observation ids; a fusion-decision audit event present. GDR-016: the observation
fixtures come from the single shared builder and are byte-identical to the on-disk
fixtures.

Trace: FCE-REQ-KRN-011, FCE-REQ-PRV-002, docs/17 §4, docs/09 Scenario 4.
"""
import json
from pathlib import Path

from fce_poc.audit.canonical import canonical_bytes
from fce_poc.audit.writer import AuditWriter
from fce_poc.policy.attributes import InjectedClock
from fce_poc.fusion import MergeParent, MergeRequest, evaluate_merge
from fce_poc.fixtures.scenario_s4 import build_s4_observations

REPO = Path(__file__).resolve().parents[2]
SCEN = REPO / "data" / "fixtures" / "scenarios"


def _parent(env):
    return MergeParent(
        object_id=env["object_id"], classification_label=env["classification_label"],
        domain_label=env["domain_label"], release_caveat=env["release_caveat"],
        lifecycle_type="normalized_observation", parent_object_ids=[], bundle_version="0.2.0")


def test_fus_s4_fused_track_permit_hwm_parentage(bundle, tmp_path):
    # `bundle` is the sealed proj-baseline@0.2.0 (conftest, flipped in place at L1-1).
    obs = build_s4_observations()
    eo, ua = obs["eo_ir"], obs["uas_telemetry"]
    req = MergeRequest(parents=[_parent(eo), _parent(ua)], mission="MISSION-ALPHA",
                       output_lifecycle_type="fused_track", proposed_output_object_id="S4-FUSED-1")
    d = evaluate_merge(req, bundle, AuditWriter(tmp_path / "s4.jsonl", InjectedClock(now=1)), event_id="e-s4")
    assert d.disposition == "permit"
    assert d.output_label == ("PROJ-LEVEL-2", "DOMAIN-A", ["PROJ-CAVEAT-X"])  # high-water mark
    assert d.audit_event["source_object_ids"] == [eo["object_id"], ua["object_id"]]  # kernel-written parentage
    assert d.audit_event["output_object_id"] == "S4-FUSED-1"
    assert d.audit_event["event_type"] == "fusion-decision"


def test_fus_s4_gdr016_builder_matches_on_disk_fixtures():
    obs = build_s4_observations()
    for name, key in [("s4_eo_ir.json", "eo_ir"), ("s4_uas_telemetry.json", "uas_telemetry")]:
        disk = json.loads((SCEN / name).read_text(encoding="utf-8"))
        assert canonical_bytes(disk) == canonical_bytes(obs[key])   # train/serve identity
        assert disk["data_origin"] == "SYNTHETIC"                    # synthetic banner source
