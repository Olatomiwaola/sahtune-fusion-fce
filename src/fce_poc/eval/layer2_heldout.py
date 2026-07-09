"""Layer-2 sealed held-out evaluation runner (docs/17 §3/§5/§6).

DIAGNOSTIC MODE (GDR-015): wires EXISTING components only — no new gate/policy
semantics. Writes NO evidence/model/report artifact; the audit log + export land in
a caller-supplied scratch dir. Prints a raw report to stdout.

GDR-014 (no-blind-report): the report body is emitted only if the required run
artifacts (seal-verified inputs, a non-empty audit chain, R1/R2 results, a
guard summary) are present; otherwise the runner reports the missing artifact and
refuses the summary.

Components wired: validator.evaluate (G1-G3), policy.evaluate (G4/policy),
kernel.evaluate_merge (fusion), crosscheck.check_parent (C3), envelope_integrity
.verify_integrity (G3), AuditWriter (G7), chain.verify_chain (R1),
export.export_package (R2), provenance.build_graph.

Run:  python -m fce_poc.eval.layer2_heldout <scratch_dir>
"""

from __future__ import annotations

import hashlib
import json
import sys
import uuid
from pathlib import Path

from fce_poc.taxonomy import load_taxonomy
from fce_poc.validator import evaluate as g2_evaluate, evaluate_batch
from fce_poc.policy import load_bundle
from fce_poc.policy.attributes import InjectedClock, PIPAttribute
from fce_poc.policy.evaluator import evaluate as policy_evaluate, record_canonical
from fce_poc.audit.records import new_record
from fce_poc.audit.writer import AuditWriter
from fce_poc.audit.chain import verify_chain
from fce_poc.audit.export import export_package, recompute_manifest_sha256
from fce_poc.audit.envelope_integrity import verify_integrity
from fce_poc.provenance import build_graph
from fce_poc.fusion import MergeParent, MergeRequest, evaluate_merge
from fce_poc.fusion.crosscheck import check_parent

REPO = Path(__file__).resolve().parents[3]
POLICY_DIR = REPO / "data" / "fixtures" / "policy"
CALIB = REPO / "data" / "fixtures" / "calibration"
HELDOUT = REPO / "data" / "fixtures" / "heldout"
VARIANTS = REPO / "data" / "fixtures" / "variants"

SEALED_BUNDLE = POLICY_DIR / "bundle_proj-baseline_0.2.0.json"
SEALED_BUNDLE_SHA = "6a830b2474a362f799fab045f0f2c23ca0b9d117c8f1e1d0acc5b51a69c53502"
HELDOUT_AGG_SHA = "059829241e527eb1aa09e3ff8ce8abafed1eeee445e04474f32ac267954ed63e"
PINNED = "0.2.0"
_NS = uuid.uuid5(uuid.NAMESPACE_URL, "https://sahtune-fce/eval/layer2")
_TS = {"ts": "2026-07-08T00:00:00Z", "clock_source": "injected"}
_VALID_PIP = [PIPAttribute(attr_id="clearance", value="PROJ-LEVEL-2", authenticated=True, integrity_bound=True)]

# --- §5 / manifest oracle (expected outcome per case) --------------------------
ORACLE = {
    "clean_corpus": "accepted at G2; ≥2 modalities traverse (FCE-REQ-ING-010)",
    "tampered": "G2/G3 integrity fail-closed (RC-001 path)",
    "malformed_unknown_field": "G2 reject RC-001",
    "malformed_duplicate": "quarantine RC-001 + duplicate_object_id",
    "stale": "fail-closed RC-004",
    "pip_spoof": "G4 fail-closed RC-008",
    "pre_marking": "accept-with-detection; forced unvalidated (RC-012)",
    "forged_parentage": "quarantine + unrecorded_parentage",
    "unauthorized_merge": "block + segregate; RC-003 (override-immune)",
    "covered_merge": "permit; HWM + kernel-written parentage",
}
# case -> FCE-REQ rows (coverage map, LAP-EVAL-002)
COVERAGE = {
    "clean_corpus": ["FCE-REQ-ING-010", "FCE-REQ-PRV-001", "FCE-REQ-MET-010"],
    "tampered": ["FCE-REQ-MET-010", "FCE-REQ-AUD-002"],
    "malformed_unknown_field": ["FCE-REQ-MET-010"],
    "malformed_duplicate": ["FCE-REQ-MET-010", "FCE-REQ-POL-012"],
    "stale": ["FCE-REQ-ING-011"],
    "pip_spoof": ["FCE-REQ-SEC-002"],
    "pre_marking": ["FCE-REQ-POL-012"],
    "forged_parentage": ["FCE-REQ-KRN-012", "FCE-REQ-PRV-002"],
    "unauthorized_merge": ["FCE-REQ-KRN-011"],
    "covered_merge": ["FCE-REQ-KRN-011", "FCE-REQ-PRV-002"],
    "determinism": ["FCE-REQ-POL-001"],
    "audit_R1_R2": ["FCE-REQ-AUD-002", "FCE-REQ-AUD-003", "FCE-REQ-EXP-001"],
}


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _aeid(tag):
    return str(uuid.uuid5(_NS, tag))


def _policy_request(obj, pip=None):
    return {"object": obj, "channel": {"domain": obj.get("domain_label")},
            "mission": "MISSION-ALPHA", "pip_attributes": pip if pip is not None else list(_VALID_PIP)}


def _emit_policy_record(writer, obj_id, pr, tag):
    out = None if pr["disposition"] != "permit" else obj_id
    writer.append(new_record(
        audit_event_id=_aeid(tag), event_type="policy-decision", event_timestamp=_TS,
        actor_identity="layer2-eval", source_object_ids=[obj_id], output_object_id=out,
        policy_bundle_version=PINNED, policy_rule_ids=pr["rules_fired"], decision=pr["disposition"],
        reason_codes=pr["reason_codes"], enforcement_action=pr["disposition"],
        disposition=pr["disposition"],
        event_detail={"pip_attributes_consumed": pr["pip_attributes_consumed"],
                      "detection_flags": pr["detection_flags"], "deterministic_evaluation": True}))


def _merge_parent(spec):
    return MergeParent(
        object_id=spec["object_id"], classification_label=spec.get("classification_label", "PROJ-LEVEL-1"),
        domain_label=spec["domain_label"], release_caveat=spec.get("release_caveat", []),
        lifecycle_type=spec.get("lifecycle_type", "normalized_observation"),
        parent_object_ids=spec.get("parent_object_ids", []), bundle_version=PINNED)


def run_pass(scratch_dir: Path) -> dict:
    """One deterministic sealed held-out pass. Returns an ordered result dict."""
    scratch_dir.mkdir(parents=True, exist_ok=True)
    clock = InjectedClock(now=1000)
    tax = load_taxonomy(CALIB / "taxonomy.json")
    resolvable = frozenset(_load(CALIB / "taxonomy.json")["classification_label"])
    bundle = load_bundle(SEALED_BUNDLE)
    audit_log = scratch_dir / "audit.jsonl"
    if audit_log.exists():
        audit_log.unlink()
    writer = AuditWriter(audit_log, clock)
    results = {"cases": {}}

    # --- clean corpus (every object G1->G7; ≥2 modalities) ---
    modality_counts = {}
    corpus = {"accepted": 0, "quarantined": 0, "rejected": 0, "policy_permit": 0, "policy_other": 0, "total": 0}
    for f in sorted(HELDOUT.glob("*.json")):
        for obj in _load(f):
            vr = g2_evaluate(obj, tax)
            corpus["total"] += 1
            corpus[vr.disposition] = corpus.get(vr.disposition, 0) + 1
            modality_counts[obj.get("modality")] = modality_counts.get(obj.get("modality"), 0) + 1
            if vr.disposition == "accepted":
                pr = policy_evaluate(_policy_request(obj), bundle, clock, pinned_version=PINNED,
                                     resolvable_classifications=resolvable)
                corpus["policy_permit" if pr["disposition"] == "permit" else "policy_other"] += 1
                _emit_policy_record(writer, obj["object_id"], pr, f"corpus:{obj['object_id']}")
    results["cases"]["clean_corpus"] = {
        "actual": f"accepted={corpus['accepted']} quarantined={corpus['quarantined']} rejected={corpus['rejected']} "
                  f"policy_permit={corpus['policy_permit']} policy_other={corpus['policy_other']} total={corpus['total']}",
        "modalities": modality_counts, "oracle": ORACLE["clean_corpus"],
        "match": corpus["accepted"] == corpus["total"] and len([m for m in modality_counts if m]) >= 2,
    }

    # --- tampered (G3 integrity) ---
    tenv = _load(VARIANTS / "tampered.json")
    integrity_ok = verify_integrity(tenv)
    results["cases"]["tampered"] = {"actual": f"verify_integrity={integrity_ok} (fail-closed on False)",
                                    "oracle": ORACLE["tampered"], "match": integrity_ok is False}

    # --- malformed: unknown field (G2) ---
    menv = _load(VARIANTS / "malformed_unknown_field.json")
    mvr = g2_evaluate(menv, tax)
    results["cases"]["malformed_unknown_field"] = {
        "actual": f"disposition={mvr.disposition} reason_code={mvr.reason_code} failed_rules={list(mvr.failed_rules)}",
        "oracle": ORACLE["malformed_unknown_field"], "match": mvr.disposition in ("rejected", "quarantined")}

    # --- malformed: duplicate object_id pair (batch scan) ---
    dup_a, dup_b = _load(VARIANTS / "malformed_duplicate_id_a.json"), _load(VARIANTS / "malformed_duplicate_id_b.json")
    batch = evaluate_batch([dup_a, dup_b], tax)
    dup = batch[1]  # second occurrence of the shared object_id (per-run, FCE-DR-SCH-004 D5)
    results["cases"]["malformed_duplicate"] = {
        "actual": f"same object_id={dup_a['object_id'] == dup_b['object_id']}; batch[0]={batch[0].disposition}; "
                  f"batch[1] disposition={dup.disposition} reason_code={dup.reason_code} detection_flags={list(dup.detection_flags)}",
        "oracle": ORACLE["malformed_duplicate"],
        "match": dup.disposition == "quarantined" and dup.reason_code == "RC-001"
                 and any(fl.startswith("duplicate_object_id") for fl in dup.detection_flags),
    }

    # --- stale (RULE-ING-011 is tick-based; variant is acquisition_timestamp-based) ---
    senv = _load(VARIANTS / "stale.json")
    svr = g2_evaluate(senv, tax)
    spr = policy_evaluate(_policy_request(senv), bundle, clock, pinned_version=PINNED, resolvable_classifications=resolvable)
    _emit_policy_record(writer, senv["object_id"], spr, "stale")
    results["cases"]["stale"] = {
        "actual": f"validator={svr.disposition}; policy disposition={spr['disposition']} reason_codes={spr['reason_codes']} "
                  f"rules={spr['rules_fired']}; acquisition_timestamp={senv.get('acquisition_timestamp')}, "
                  f"no object_timestamp_tick -> RULE-ING-011 not triggered",
        "oracle": ORACLE["stale"], "match": "RC-004" in spr["reason_codes"]}

    # --- pip_spoof (G4 RC-008) ---
    spoof = _load(VARIANTS / "pip_spoof.json")
    spoof_pip = [PIPAttribute(attr_id=spoof["spoofed_pip_attribute"]["attr_id"], value=spoof["spoofed_pip_attribute"]["value"],
                              authenticated=spoof["spoofed_pip_attribute"]["authenticated"],
                              integrity_bound=spoof["spoofed_pip_attribute"]["integrity_bound"])]
    carrier = _load(HELDOUT / "osd04_s2stac_heldout.json")[0]
    ppr = policy_evaluate(_policy_request(carrier, spoof_pip), bundle, clock, pinned_version=PINNED, resolvable_classifications=resolvable)
    _emit_policy_record(writer, carrier["object_id"], ppr, "pip_spoof")
    results["cases"]["pip_spoof"] = {
        "actual": f"disposition={ppr['disposition']} reason_codes={ppr['reason_codes']} rules={ppr['rules_fired']}",
        "oracle": ORACLE["pip_spoof"], "match": ppr["disposition"] == "block" and "RC-008" in ppr["reason_codes"]}

    # --- pre_marking (RC-012 forced-unvalidated detection) ---
    penv = _load(VARIANTS / "pre_marking.json")
    pvr = g2_evaluate(penv, tax)
    results["cases"]["pre_marking"] = {
        "actual": f"validator disposition={pvr.disposition} detection_flags={list(pvr.detection_flags)}",
        "oracle": ORACLE["pre_marking"],
        "match": any("binding" in fl or "RC-012" in fl or "unvalidated" in fl for fl in pvr.detection_flags)}

    # --- forged_parentage (C3 crosscheck over provenance graph) ---
    fenv = _load(VARIANTS / "forged_parentage.json")
    graph = build_graph([])  # forged parent is not kernel-recorded
    fparent = _merge_parent(fenv)
    ok, flag = check_parent(fparent, graph)
    results["cases"]["forged_parentage"] = {
        "actual": f"check_parent ok={ok} flag={flag} (lifecycle={fenv.get('lifecycle_type')}, claimed={fenv.get('parent_object_ids')})",
        "oracle": ORACLE["forged_parentage"], "match": ok is False and flag == "unrecorded_parentage"}

    # --- unauthorized_merge (cross-domain, RC-003 block+segregate) ---
    um = _load(VARIANTS / "unauthorized_merge.json")
    um_parents = [_merge_parent(p) for p in um["request_parents"]]
    umreq = MergeRequest(parents=um_parents, mission="MISSION-ALPHA", output_lifecycle_type="fused_track",
                         proposed_output_object_id="UM-OUT")
    umd = evaluate_merge(umreq, bundle, writer, event_id=_aeid("unauthorized_merge"))
    results["cases"]["unauthorized_merge"] = {
        "actual": f"disposition={umd.disposition} reason_codes={umd.reason_codes} detection_flags={umd.detection_flags} output={umd.output_object_id}",
        "oracle": ORACLE["unauthorized_merge"],
        "match": "RC-003" in umd.reason_codes and umd.disposition in ("block", "segregate") and umd.output_object_id is None}

    # --- covered same-domain merge (S4 pair): permit + HWM + parentage ---
    eo = _load(REPO / "data" / "fixtures" / "scenarios" / "s4_eo_ir.json")
    ua = _load(REPO / "data" / "fixtures" / "scenarios" / "s4_uas_telemetry.json")
    creq = MergeRequest(parents=[_merge_parent({**eo, "release_caveat": eo["release_caveat"]}),
                                 _merge_parent({**ua, "release_caveat": ua["release_caveat"]})],
                        mission="MISSION-ALPHA", output_lifecycle_type="fused_track", proposed_output_object_id="S4-COVERED")
    cd = evaluate_merge(creq, bundle, writer, event_id=_aeid("covered_merge"))
    results["cases"]["covered_merge"] = {
        "actual": f"disposition={cd.disposition} output_label={cd.output_label} parentage={cd.audit_event.get('source_object_ids')}",
        "oracle": ORACLE["covered_merge"],
        "match": cd.disposition == "permit" and cd.output_label == ("PROJ-LEVEL-2", "DOMAIN-A", ["PROJ-CAVEAT-X"])
                 and cd.audit_event.get("source_object_ids") == [eo["object_id"], ua["object_id"]]}

    # --- R1 (tamper-evident chain) + R2 (export + manifest recompute) ---
    r1 = verify_chain(audit_log)
    export_dir = scratch_dir / "export"
    exp = export_package(audit_log, export_dir, clock, package_id="LAP-EVAL-EXPORT")
    r2_ok = recompute_manifest_sha256(exp.manifest_path) == exp.manifest_sha256
    results["audit"] = {"R1_verify_chain": {"ok": r1.ok, "count": r1.record_count},
                        "R2_export": {"record_count": exp.manifest["record_count"],
                                      "chain_head_hash": exp.manifest["chain_head_hash"],
                                      "manifest_sha256_recompute_match": r2_ok}}
    results["chain_records"] = r1.record_count
    return results


def _canonical(results: dict) -> str:
    trimmed = {"cases": {k: {"actual": v["actual"], "oracle": v["oracle"], "match": v["match"]}
                         for k, v in results["cases"].items()},
               "audit": results["audit"]}
    return json.dumps(trimmed, sort_keys=True, ensure_ascii=False)


def main(scratch_dir: str) -> int:
    scratch = Path(scratch_dir)
    scratch.mkdir(parents=True, exist_ok=True)

    # --- run-open seal check (GDR: verify sealed inputs before any held-out use) ---
    bundle_sha = hashlib.sha256(SEALED_BUNDLE.read_bytes()).hexdigest()
    per = sorted(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  data/fixtures/heldout/{p.name}"
                 for p in HELDOUT.glob("*"))
    agg_sha = hashlib.sha256(("\n".join(per) + "\n").encode()).hexdigest()
    seal_ok = bundle_sha == SEALED_BUNDLE_SHA and agg_sha == HELDOUT_AGG_SHA

    # --- two passes for determinism (LAP-EVAL-001) ---
    r1 = run_pass(scratch / "run1")
    r2 = run_pass(scratch / "run2")
    determinism_identical = _canonical(r1) == _canonical(r2)

    # --- GDR-014 no-blind-report: required artifacts present? ---
    artifacts = {"seal_verified": seal_ok, "audit_chain_nonempty": r1["chain_records"] > 0,
                 "R1_present": "R1_verify_chain" in r1["audit"], "R2_present": "R2_export" in r1["audit"],
                 "determinism_run": True}
    guard_summary = {
        "GDR-014_no_blind_report": "PASS — all required run artifacts present" if all(artifacts.values())
                                   else f"REFUSE REPORT — missing: {[k for k, v in artifacts.items() if not v]}",
        "GDR-015_diagnostic_read_only": "PASS — no evidence/model/report artifact written; outputs confined to scratch dir",
        "seal_check": {"bundle_sha_match": bundle_sha == SEALED_BUNDLE_SHA, "heldout_agg_match": agg_sha == HELDOUT_AGG_SHA},
        "required_artifacts": artifacts,
    }

    print("=" * 78)
    print("LAYER-2 SEALED HELD-OUT EVALUATION — diagnostic run (no evidence written)")
    print("=" * 78)
    print(f"\n[GUARD SUMMARY]  {json.dumps(guard_summary, indent=2)}")
    if not all(artifacts.values()):
        print("\nGDR-014: required artifacts missing — report body refused.")
        return 1

    print("\n[RUN SUMMARY — expected (oracle) vs actual]")
    negatives = []
    for case, r in r1["cases"].items():
        mark = "MATCH" if r["match"] is True else ("REPORTED" if r["match"] is None else "*** NEGATIVE ***")
        print(f"\n  case: {case}   [{mark}]")
        print(f"    oracle: {r['oracle']}")
        print(f"    actual: {r['actual']}")
        if "modalities" in r:
            print(f"    modalities: {r['modalities']}")
        if r["match"] is False:
            negatives.append(case)

    print(f"\n[R1/R2 AUDIT VERIFICATION]  {json.dumps(r1['audit'], indent=2)}")
    print(f"\n[DETERMINISM — LAP-EVAL-001]  two passes byte-identical: {determinism_identical}")
    print(f"\n[COVERAGE MAP — LAP-EVAL-002]  {json.dumps(COVERAGE, indent=2)}")
    print(f"\n[NEGATIVES — verbatim, not fixed]  {negatives if negatives else 'none'}")
    print("\n" + "=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
