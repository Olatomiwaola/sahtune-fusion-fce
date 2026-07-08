"""Stage 5 — seven red-team variant generators (docs/09 v1 matrix).

Lineage lives in the fixture-generation manifest (A1); envelope parent_object_ids
stays empty EXCEPT forged-parentage (the test payload). data_origin per
FCE-DR-SCH-005 / A4. GDR-004: every variant derives from a CALIBRATION-side parent;
a held-out parent aborts. No held-out material is ever a variant parent.
"""

from __future__ import annotations

import copy
import uuid

from .normalize import build_envelope, object_id_for  # imports policy graph first (circular-import guard)
from fce_poc.audit.envelope_integrity import compute_integrity_hash

VARIANT_TYPES = (
    "tampered", "malformed", "stale", "pip_spoof",
    "pre_marking", "unauthorized_merge", "forged_parentage",
)


def _assert_calibration(record_id, calibration_ids, heldout_ids):
    if record_id in heldout_ids or record_id not in calibration_ids:
        raise ValueError(f"GDR-004: variant parent {record_id!r} is not calibration-side — abort")


def generate_variants(calibration_records, calibration_ids, heldout_ids):
    """Return (variant_fixtures: dict[name->obj], generation_manifest: dict)."""
    cal_ids = set(calibration_ids)
    held_ids = set(heldout_ids)
    usgs = [r for r in calibration_records if r["source_id"] == "OSD-01"]
    stac = [r for r in calibration_records if r["source_id"] == "OSD-04"]
    fixtures = {}
    entries = []

    def parent_env(rec):
        _assert_calibration(rec["record_id"], cal_ids, held_ids)
        return build_envelope(rec), rec["record_id"]

    # 1. tampered — mutate a label AFTER hashing (integrity mismatch); public parent.
    penv, pid = parent_env(usgs[0])
    tampered = copy.deepcopy(penv)
    tampered["data_origin"] = "SYNTHETIC-DERIVED"
    tampered["classification_label"] = "PROJ-LEVEL-3"  # stored integrity_hash now stale
    fixtures["tampered"] = tampered
    entries.append({"variant": "tampered", "parent_source_record_ids": [pid],
                    "mutation": "classification_label + data_origin changed post-hash (integrity mismatch)",
                    "data_origin": "SYNTHETIC-DERIVED", "envelope_parentage": "empty",
                    "expected_outcome": "G2/G3 integrity fail-closed (RC-001 path)",
                    "scenario_items": ["S1 tampered"], "trace": ["FCE-REQ-MET-010"]})

    # 2. malformed — (a) unknown field, (b) duplicate object_id pair.
    penv, pid = parent_env(usgs[1])
    malformed = copy.deepcopy(penv)
    malformed["data_origin"] = "SYNTHETIC"
    malformed["integrity_hash"] = compute_integrity_hash(malformed)
    malformed["extra_unknown_field"] = "not-in-schema"
    fixtures["malformed_unknown_field"] = malformed
    dpenv, dpid = parent_env(usgs[2])
    dup_a = copy.deepcopy(dpenv); dup_a["data_origin"] = "SYNTHETIC"
    dup_a["integrity_hash"] = compute_integrity_hash(dup_a)
    dup_b = copy.deepcopy(dup_a)  # identical object_id -> duplicate_object_id
    fixtures["malformed_duplicate_id_a"] = dup_a
    fixtures["malformed_duplicate_id_b"] = dup_b
    entries.append({"variant": "malformed", "parent_source_record_ids": [pid, dpid],
                    "mutation": "unknown envelope field; and a duplicate object_id pair",
                    "data_origin": "SYNTHETIC", "envelope_parentage": "empty",
                    "expected_outcome": "G2 reject RC-001 (FCE-DR-SCH-003); duplicate object_id -> quarantine RC-001 + duplicate_object_id flag (FCE-DR-SCH-004 D5)",
                    "scenario_items": ["S3 malformed"], "trace": ["FCE-REQ-MET-010"]})

    # 3. stale — valid envelope, very old acquisition_timestamp (staleness demo is M7).
    penv, pid = parent_env(stac[0])
    stale = copy.deepcopy(penv)
    stale["data_origin"] = "SYNTHETIC-DERIVED"
    stale["acquisition_timestamp"] = "2000-01-01T00:00:00Z"
    stale["integrity_hash"] = compute_integrity_hash(stale)
    fixtures["stale"] = stale
    entries.append({"variant": "stale", "parent_source_record_ids": [pid],
                    "mutation": "acquisition_timestamp set beyond staleness policy",
                    "data_origin": "SYNTHETIC-DERIVED", "envelope_parentage": "empty",
                    "expected_outcome": "RC-004 fail-closed — fixture at M6, demonstration M7 (RT-M3S6-05)",
                    "scenario_items": ["2.3", "S3 replay"], "trace": ["FCE-REQ-ING-011"]})

    # 4. pip_spoof — unauthenticated PIP attribute (policy-layer config, not envelope).
    penv, pid = parent_env(usgs[3])
    fixtures["pip_spoof"] = {
        "variant": "pip_spoof", "parent_object_id": penv["object_id"],
        "spoofed_pip_attribute": {"attr_id": "clearance", "value": "PROJ-LEVEL-3",
                                  "authenticated": False, "integrity_bound": False},
        "data_origin": "SYNTHETIC", "expected_outcome": "G4 fail-closed, RC-008",
    }
    entries.append({"variant": "pip_spoof", "parent_source_record_ids": [pid],
                    "mutation": "unauthenticated/unbound PIP attribute presented at G4",
                    "data_origin": "SYNTHETIC", "envelope_parentage": "empty",
                    "expected_outcome": "G4 fail-closed, RC-008",
                    "scenario_items": ["S1 PIP spoof"], "trace": ["FCE-REQ-SEC-002"]})

    # 5. pre_marking — source-supplied policy_binding_state (forced + detected at G1).
    penv, pid = parent_env(usgs[4])
    pre = copy.deepcopy(penv)
    pre["data_origin"] = "SYNTHETIC-DERIVED"
    pre["integrity_hash"] = compute_integrity_hash(pre)
    pre["policy_binding_state"] = "validated"  # field 15 excluded from integrity domain
    fixtures["pre_marking"] = pre
    entries.append({"variant": "pre_marking", "parent_source_record_ids": [pid],
                    "mutation": "source-supplied policy_binding_state=validated",
                    "data_origin": "SYNTHETIC-DERIVED", "envelope_parentage": "empty",
                    "expected_outcome": "forced unvalidated + RC-012 / source_supplied detection flag",
                    "scenario_items": ["3.4 pre-marking"], "trace": ["FCE-REQ-MET-010"]})

    # 6. unauthorized_merge — cross-domain request (public DOMAIN-A + synthetic DOMAIN-B).
    penv, pid = parent_env(usgs[5])
    synth_b = {"object_id": object_id_for("SYNTH", "domain-b-track-1"),
               "data_origin": "SYNTHETIC", "domain_label": "DOMAIN-B",
               "classification_label": "PROJ-LEVEL-1", "modality": "radar_like"}
    fixtures["unauthorized_merge"] = {
        "variant": "unauthorized_merge",
        "request_parents": [
            {"object_id": penv["object_id"], "domain_label": penv["domain_label"],
             "data_origin": penv["data_origin"], "source_record_id": pid},
            synth_b,
        ],
        "data_origin_note": "request only; no output object exists on block",
        "expected_outcome": "RC-003 block + segregate; null output",
    }
    entries.append({"variant": "unauthorized_merge", "parent_source_record_ids": [pid],
                    "mutation": "cross-domain merge request with no covering combination",
                    "data_origin": "SYNTHETIC + PUBLIC parents (request only; no output object)",
                    "envelope_parentage": "n/a (no output)",
                    "expected_outcome": "RC-003 block + segregate",
                    "scenario_items": ["1.1", "2.1"], "trace": ["FCE-REQ-KRN-011"]})

    # 7. forged_parentage — derived-type object with self-declared parentage (the payload).
    penv, pid = parent_env(usgs[6])
    forged = copy.deepcopy(penv)
    forged["data_origin"] = "SYNTHETIC-DERIVED"
    forged["lifecycle_type"] = "tracklet"
    forged["parent_object_ids"] = [str(uuid.uuid5(uuid.NAMESPACE_URL, "forged-parent-not-in-arch09"))]
    forged["integrity_hash"] = compute_integrity_hash(forged)
    fixtures["forged_parentage"] = forged
    entries.append({"variant": "forged_parentage", "parent_source_record_ids": [pid],
                    "mutation": "derived lifecycle_type with caller-supplied parent_object_ids not in ARCH-09",
                    "data_origin": "SYNTHETIC-DERIVED", "envelope_parentage": "non-empty (test payload)",
                    "expected_outcome": "quarantine + unrecorded_parentage flag (docs/18 §1, C3)",
                    "scenario_items": ["S1 forged parentage", "V3/V7"], "trace": ["FCE-REQ-KRN-012"]})

    manifest = {
        "note": "Fixture-generation manifest (A1). Variants derive only from calibration-side parents (GDR-004 asserted). Envelope parent_object_ids empty except forged_parentage.",
        "gdr004_assertion": "passed — no held-out id used as a variant parent",
        "variants": entries,
        "scenario_conflict_configs": [
            {"item": "1.2 / 2.2", "config": "RC-002 caveat/domain-mismatch channel case (block, override-immune)", "side": "calibration"},
            {"item": "1.3", "config": "ambiguous classification (unresolvable label) -> quarantine RC-005", "side": "calibration"},
            {"item": "1.4", "config": "mixed pinned bundle-version merge pair -> quarantine RC-005 + mixed_bundle_versions", "side": "calibration"},
            {"item": "2.4", "config": "broad-release partial-permit (restrict; permitted subset in rules-fired citation, TST-POL-007)", "side": "calibration"},
            {"item": "2.5", "config": "route-to-higher-domain delivery disposition (TST-POL-008; envelope invariant)", "side": "calibration"},
            {"item": "3.4", "config": "G1-reject family: unsupported schema_version / LIVE / source-supplied binding", "side": "calibration"},
            {"item": "4.1-4.6", "config": "S4 override (accept/reject/immunity) + downgrade (valid/invalid proof) inputs", "side": "calibration"},
        ],
    }
    return fixtures, manifest
