"""Scenario 4 (UAV) synthetic observation fixtures for the S4 fused-track merge.

Labels fixed by the docs/17 §4 Resolution addendum (2026-07-08, lead decision):
  eo_ir observation        = (PROJ-LEVEL-1, DOMAIN-A, [PROJ-CAVEAT-X])
  uas_telemetry observation= (PROJ-LEVEL-2, DOMAIN-A, [PROJ-CAVEAT-X])
The fused-track HWM label is therefore (PROJ-LEVEL-2, DOMAIN-A, [PROJ-CAVEAT-X]),
which MP-V1-SAME-DOMAIN covers exactly in the sealed proj-baseline@0.2.0 (no re-pin).

data_origin=SYNTHETIC (visible SYNTHETIC banner follows structurally). GDR-016:
`build_s4_observations()` is the single builder used by both the fixture writer
and the tests, so builder and runtime share one normalization path. stdlib only.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

import fce_poc.policy  # noqa: F401  # policy graph before audit.__init__ (circular-import guard)
from fce_poc.audit.envelope_integrity import compute_integrity_hash

_NS = uuid.uuid5(uuid.NAMESPACE_URL, "https://sahtune-fce/fixtures/scenario-s4")
SCENARIOS_DIR = Path(__file__).resolve().parents[3] / "data" / "fixtures" / "scenarios"

_ACQUISITION = "2026-07-08T12:00:00Z"
_INGEST = "2026-07-08T00:00:00Z"  # injected clock (H4)


def _observation(key: str, sensor_id: str, modality: str, classification: str) -> dict:
    env = {
        "object_id": str(uuid.uuid5(_NS, key)),
        "schema_version": "0.2.0",
        "data_origin": "SYNTHETIC",
        "source_sensor_id": sensor_id,
        "modality": modality,
        "acquisition_timestamp": _ACQUISITION,
        "clock_source": "injected",
        "ingest_timestamp": _INGEST,
        "classification_label": classification,
        "domain_label": "DOMAIN-A",
        "release_caveat": ["PROJ-CAVEAT-X"],
        "handling_instructions": "Handle per project synthetic-data policy (Scenario 4 UAV fixture).",
        "provenance_ref": f"graph://node/s4-{key}",
        "parent_object_ids": [],
        "lifecycle_type": "normalized_observation",
    }
    env["integrity_hash"] = compute_integrity_hash(env)
    return env


def build_s4_observations() -> dict:
    """The two Scenario-4 observation envelopes (GDR-016 single shared builder)."""
    return {
        "eo_ir": _observation("eo-ir", "SENSOR-S4-EOIR-001", "eo_ir", "PROJ-LEVEL-1"),
        "uas_telemetry": _observation("uas-telemetry", "SENSOR-S4-UAS-001", "uas_telemetry", "PROJ-LEVEL-2"),
    }


def write_fixtures() -> list[Path]:
    SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)
    obs = build_s4_observations()
    paths = []
    for name, env in [("s4_eo_ir.json", obs["eo_ir"]), ("s4_uas_telemetry.json", obs["uas_telemetry"])]:
        p = SCENARIOS_DIR / name
        p.write_text(json.dumps(env, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        paths.append(p)
    return paths


if __name__ == "__main__":
    for p in write_fixtures():
        print(f"wrote {p}")
