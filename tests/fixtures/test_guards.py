"""Stage 6 — fixture-build guard rejection tests (docs/16 GDR-*, M6-06 Stage 6).

Each guard must have a rejection test (docs/16 Pass/Fail #8). These run against the
Stage-1..5 build artifacts on disk plus synthesized failure cases (contamination is
synthesized in-memory, never in the real layout).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from fce_poc.audit.canonical import canonical_bytes
from fce_poc.audit.envelope_integrity import verify_integrity
from fce_poc.envelope import normalize as env_normalize
from fce_poc.gates import g1_version_origin_gate
from fce_poc.fixtures import manifest as M
from fce_poc.fixtures import split as SP
from fce_poc.fixtures import trim as T
from fce_poc.fixtures.normalize import build_envelope, runtime_ingest

REPO = Path(__file__).resolve().parents[2]
FX = REPO / "data" / "fixtures"


def _load(rel):
    return json.loads((FX / rel).read_text(encoding="utf-8"))


# GDR-004 / LAP-RED-001 — held-out id in calibration aborts.
def test_lap_red_001_split_contamination_aborts():
    with pytest.raises(ValueError, match="GDR-004"):
        SP.assert_no_contamination(["a", "b", "held-1"], ["held-1"])
    # real layout is clean:
    cal = [e["object_id"] for e in _load("calibration/osd01_usgs_calibration.json")]
    held = [e["object_id"] for e in _load("heldout/osd01_usgs_heldout.json")]
    assert set(cal).isdisjoint(held)


# GDR-001/-002/-003 / LAP-RED-002a/b/c — manifest missing hash / licence / query.
def _real_manifest():
    m = M.build_source_manifest()
    M.validate_manifest(m)  # real manifest is complete
    return m


def test_lap_red_002a_missing_hash_refused():
    m = _real_manifest()
    m["sources"]["OSD-01"].pop("raw_file_sha256")
    with pytest.raises(ValueError, match="GDR-001"):
        M.validate_manifest(m)


def test_lap_red_002b_missing_licence_refused():
    m = _real_manifest()
    m["sources"]["OSD-04"].pop("licence_note")
    with pytest.raises(ValueError, match="GDR-002"):
        M.validate_manifest(m)


def test_lap_red_002c_missing_query_params_refused():
    m = _real_manifest()
    m["sources"]["OSD-01"].pop("query_params")
    with pytest.raises(ValueError, match="GDR-003"):
        M.validate_manifest(m)


# GDR-005 / LAP-RED-005 — empty modality after trim aborts.
def test_lap_red_005_empty_modality_aborts():
    with pytest.raises(ValueError, match="GDR-005"):
        T.nonempty_modalities({"OSD-01": [{"x": 1}], "OSD-04": []})


# GDR-016 / LAP-RED-006 — fixture-builder and runtime path byte-identical (train/serve).
def test_lap_red_006_normalization_identity():
    rec = _load("trimmed/osd01_usgs_trimmed.json")[0]
    assert canonical_bytes(build_envelope(rec)) == canonical_bytes(runtime_ingest(rec))
    # a built calibration fixture verifies its own CANON-1 integrity hash:
    fixture = _load("calibration/osd01_usgs_calibration.json")[0]
    assert verify_integrity(fixture) is True
    # and rebuilding from the source trimmed record reproduces it byte-for-byte:
    by_id = {build_envelope(r)["object_id"]: r for r in _load("trimmed/osd01_usgs_trimmed.json")}
    rebuilt = build_envelope(by_id[fixture["object_id"]])
    assert canonical_bytes(rebuilt) == canonical_bytes(fixture)


# GDR-006 — unsupported envelope version rejected (reuse of the G1 gate).
def test_gdr006_envelope_version_gate():
    old = copy.deepcopy(_load("calibration/osd01_usgs_calibration.json")[0])
    old["schema_version"] = "0.1.0"
    gate = g1_version_origin_gate(env_normalize(old))
    assert not gate.passed and "RULE-VAL-002" in gate.failed_rules
