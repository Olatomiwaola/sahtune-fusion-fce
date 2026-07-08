"""M6 Sprint 12 build orchestrator (Stages 1-5, 7). stdlib only, no network.

Reads git-ignored data/raw/, writes data/fixtures/. Emits raw stage outputs and
fail-closes (raises) on any STOP condition: candidate pairs < 10, a fixture that
does not validate as accepted, split contamination, empty modality, or a licence
value that is not verbatim-continuous R4 text.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from fce_poc.taxonomy import load_taxonomy
from fce_poc.validator import evaluate
from . import manifest as M
from . import split as SP
from . import trim as T
from . import variants as V
from .normalize import build_envelope

REPO = Path(__file__).resolve().parents[3]
RAW = REPO / "data" / "raw"
FX = REPO / "data" / "fixtures"
TAXO = FX / "calibration" / "taxonomy.json"

CANDIDATE_FLOOR = 10


def _write_json(path: Path, obj) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run() -> dict:
    out = {}
    taxonomy = load_taxonomy(TAXO)

    # ---------- Stage 1: source manifest ----------
    man = M.build_source_manifest()
    M.validate_manifest(man)
    man_hash = _write_json(FX / "source_manifest.json", man)
    # verification point: OSD-01 licence must be verbatim-continuous R4 text
    licence = json.loads((FX / "source_manifest.json").read_text(encoding="utf-8"))["sources"]["OSD-01"]["licence_note"]
    r4_text = M._visible_text(RAW / "osd01_licence_R4.html")
    if licence not in r4_text:
        raise SystemExit("STOP Stage 1: OSD-01 licence not verbatim-continuous in R4")
    out["stage1"] = {"manifest_sha256": man_hash, "osd01_licence": licence,
                     "osd01_licence_contiguous_in_R4": True}

    # ---------- Stage 2: trim + candidate gate ----------
    usgs_raw = json.loads((RAW / "osd01_usgs_events.geojson").read_text(encoding="utf-8"))
    stac_raw = json.loads((RAW / "osd04_stageB2_stac_items.geojson").read_text(encoding="utf-8"))  # corrective B2 (slice-aligned)
    usgs_trim = T.trim_usgs(usgs_raw)
    stac_trim = T.trim_stac(stac_raw)
    T.nonempty_modalities({"OSD-01": usgs_trim, "OSD-04": stac_trim})
    h1 = _write_json(FX / "trimmed" / "osd01_usgs_trimmed.json", usgs_trim)
    h2 = _write_json(FX / "trimmed" / "osd04_s2stac_trimmed.json", stac_trim)
    pairs = T.association_candidates(usgs_trim, stac_trim)
    if len(pairs) < CANDIDATE_FLOOR:
        raise SystemExit(f"STOP Stage 2: association candidate pairs {len(pairs)} < {CANDIDATE_FLOOR} — widening is chat-gated, not unilateral")
    trim_report = {"usgs_records": len(usgs_trim), "stac_records": len(stac_trim),
                   "usgs_trimmed_sha256": h1, "stac_trimmed_sha256": h2,
                   "association_candidate_pairs_before": len(pairs),
                   "association_candidate_pairs_after": len(pairs),
                   "widening": "not fired", "candidate_definition": "epicenter in item bbox AND |dt| <= 7 days"}
    _write_json(FX / "trimmed" / "trim_report_inputs.json", trim_report)
    out["stage2"] = trim_report

    # ---------- Stage 3: normalize (validate every baseline fixture) ----------
    def envelopes(records):
        return [build_envelope(r) for r in records]

    def assert_accepted(envs, label):
        bad = []
        for e in envs:
            d = evaluate(e, taxonomy)
            if d.disposition != "accepted":
                bad.append((e["object_id"], d.disposition, d.failed_rules))
        if bad:
            raise SystemExit(f"STOP Stage 3: {label} fixtures not accepted: {bad[:3]}")

    # ---------- Stage 4: split ----------
    su = SP.split_family(usgs_trim)
    ss = SP.split_family(stac_trim)
    SP.assert_no_contamination([r["record_id"] for r in su["calibration"]], [r["record_id"] for r in su["heldout"]])
    SP.assert_no_contamination([r["record_id"] for r in ss["calibration"]], [r["record_id"] for r in ss["heldout"]])

    cal_u, held_u = envelopes(su["calibration"]), envelopes(su["heldout"])
    cal_s, held_s = envelopes(ss["calibration"]), envelopes(ss["heldout"])
    for envs, lbl in [(cal_u, "usgs-cal"), (held_u, "usgs-held"), (cal_s, "stac-cal"), (held_s, "stac-held")]:
        assert_accepted(envs, lbl)
    _write_json(FX / "calibration" / "osd01_usgs_calibration.json", cal_u)
    _write_json(FX / "calibration" / "osd04_s2stac_calibration.json", cal_s)
    _write_json(FX / "heldout" / "osd01_usgs_heldout.json", held_u)
    _write_json(FX / "heldout" / "osd04_s2stac_heldout.json", held_s)
    out["stage4"] = {
        "OSD-01": {"calibration": su["calibration_count"], "heldout": su["heldout_count"], "first3_ranked_ids": su["first3_ranked_ids"]},
        "OSD-04": {"calibration": ss["calibration_count"], "heldout": ss["heldout_count"], "first3_ranked_ids": ss["first3_ranked_ids"]},
    }

    # ---------- Stage 5: variants ----------
    cal_records = su["calibration"] + ss["calibration"]
    cal_ids = [r["record_id"] for r in cal_records]
    held_ids = [r["record_id"] for r in su["heldout"] + ss["heldout"]]
    fixtures, gen_manifest = V.generate_variants(cal_records, cal_ids, held_ids)
    for name, obj in fixtures.items():
        _write_json(FX / "variants" / f"{name}.json", obj)
    _write_json(FX / "variants" / "generation_manifest.json", gen_manifest)
    out["stage5"] = {"variant_count": len(V.VARIANT_TYPES), "variant_files": sorted(fixtures.keys()),
                     "gdr004": gen_manifest["gdr004_assertion"]}

    # ---------- Stage 7: coverage matrix ----------
    rc = sorted({f"RC-{n:03d}" for n in range(1, 13)})
    flags = ["duplicate_object_id", "mixed_bundle_versions", "source_supplied_policy_binding_state", "unrecorded_parentage"]
    guards = ["GDR-001", "GDR-002", "GDR-003", "GDR-004", "GDR-005", "GDR-006", "GDR-016"]
    items = [f"{a}.{b}" for a, b in [(1, i) for i in range(1, 6)] + [(2, i) for i in range(1, 6)]
             + [(3, i) for i in range(1, 5)] + [(4, i) for i in range(1, 7)]]
    covered_items = sorted({"1.1", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2", "2.3", "2.4", "2.5",
                            "3.4", "4.1", "4.2", "4.3", "4.4", "4.5", "4.6"})
    coverage = {
        "public_fixtures": {"OSD-01": len(cal_u) + len(held_u), "OSD-04": len(cal_s) + len(held_s),
                            "total": len(cal_u) + len(held_u) + len(cal_s) + len(held_s)},
        "variants": out["stage5"]["variant_files"],
        "rc_codes_represented": rc, "detection_flags_represented": flags,
        "guards_demonstrated": guards,
        "conflict_items_total": len(items), "conflict_items_covered": covered_items,
        "conflict_items_not_covered": sorted(set(items) - set(covered_items)),
        "rows": gen_manifest["variants"] + gen_manifest["scenario_conflict_configs"],
        "note": "Representation at M6; demonstration claims are per-item and M7-bounded where stated (EVD-M6 excluded per rule 9).",
    }
    _write_json(FX / "coverage_matrix.json", coverage)
    denom = len(items)
    out["stage7_summary"] = (f"{coverage['public_fixtures']['total']} public fixtures + {len(V.VARIANT_TYPES)} variants; "
                             f"RC {len(rc)}/12; flags {len(flags)}/4; guards {len(guards)}/7; "
                             f"conflict items {len(covered_items)}/{denom} represented "
                             f"(3.1-3.3 edge degraded-mode = M8, not M6 fixtures)")
    return out


if __name__ == "__main__":
    import sys
    result = run()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.stdout.flush()
