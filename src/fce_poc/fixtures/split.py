"""Stage 4 — deterministic 70/30 calibration/held-out split (FCE-DR-POC-003).

Stratified per source family (and therefore per modality). Deterministic rank =
sha-256 over UTF-8 of "<stable_source_record_id>:<seed>"; sort ascending by rank
within each family; first 70% -> calibration, remainder -> held-out. Keyed on the
stable SOURCE record id, never the per-run object_id (FCE-DR-SCH-004 D5).
"""

from __future__ import annotations

import hashlib

SEED = 12918724377571503927  # FCE-DR-POC-003, minted blind at Sprint 11 close


def _rank(record_id: str) -> str:
    return hashlib.sha256(f"{record_id}:{SEED}".encode("utf-8")).hexdigest()


def split_family(records: list[dict], ratio: float = 0.70) -> dict:
    """Split one family's records. Returns calibration/heldout lists + audit anchors."""
    ranked = sorted(records, key=lambda r: _rank(r["record_id"]))
    cut = int(len(ranked) * ratio)
    calibration = ranked[:cut]
    heldout = ranked[cut:]
    return {
        "calibration": calibration,
        "heldout": heldout,
        "calibration_count": len(calibration),
        "heldout_count": len(heldout),
        "first3_ranked_ids": [r["record_id"] for r in ranked[:3]],
    }


def assert_no_contamination(calibration_ids, heldout_ids) -> None:
    """GDR-004: any held-out id appearing in the calibration set aborts."""
    overlap = set(calibration_ids) & set(heldout_ids)
    if overlap:
        raise ValueError(f"GDR-004: held-out ids present in calibration set — abort: {sorted(overlap)}")
