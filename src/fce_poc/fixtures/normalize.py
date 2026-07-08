"""GDR-016 single shared normalization: trimmed source record -> 15-field v0.2.0 envelope.

The SAME `build_envelope` function is used by the fixture builder and by the runtime
ingestion proxy (`runtime_ingest`); LAP-RED-006 asserts byte-identity of the CANON-1
canonicalization of the two paths. Deterministic, pure, no network, no clock read
(the ingest timestamp is an injected constant — H4).

Baseline public-fixture labels are the least-restrictive taxonomy values
(PROJ-LEVEL-1 / DOMAIN-A / []). Conflict-case labels are applied only in Stage-5
variant configs, never by mutating the baseline. `policy_binding_state` is OMITTED
(FCE-authority-set; forced at G1) so baseline fixtures do not trip the pre-marking
detection — matching data/fixtures/calibration/valid_object.json.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Mapping

import fce_poc.policy  # noqa: F401  # establish policy->fusion->audit graph before audit.__init__ (avoids a latent circular import in the existing package)
from fce_poc.audit.envelope_integrity import compute_integrity_hash

# Deterministic namespace for per-record object_id (uuid5) — reproducible across runs.
FIXTURE_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "https://sahtune-fce/fixtures/m6-sprint12")

INGEST_TIMESTAMP = "2026-07-08T00:00:00Z"  # injected clock (H4); deterministic, no wall-clock read
HANDLING = "Handle per project public-open-source fixture policy (TRL 1-3 PoC; reproducible public-source anchor)."

MODALITY_BY_SOURCE = {"OSD-01": "acoustic_like", "OSD-04": "eo_ir"}
SOURCE_CODE = {"OSD-01": "usgs", "OSD-04": "s2stac"}


def object_id_for(source_id: str, record_id: str) -> str:
    """Deterministic per-record uuid (uuid5 over source:record_id)."""
    return str(uuid.uuid5(FIXTURE_NAMESPACE, f"{source_id}:{record_id}"))


def epoch_ms_to_rfc3339(ms: int) -> str:
    """USGS event `time` (epoch milliseconds, UTC) -> RFC3339 Z, second precision."""
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_envelope(record: Mapping) -> dict:
    """The single normalization function (GDR-016).

    record keys required: source_id ('OSD-01'|'OSD-04'), record_id (stable source id),
    acquisition_timestamp (RFC3339). Returns the v0.2.0 PUBLIC-OPEN-SOURCE envelope
    dict (15 mandatory fields minus the G1-forced field 15, plus the frozen companion
    fields). integrity_hash is CANON-1 over fields 1-6, 8-13.
    """
    source_id = record["source_id"]
    record_id = record["record_id"]
    code = SOURCE_CODE[source_id]
    env = {
        "object_id": object_id_for(source_id, record_id),          # 1
        "schema_version": "0.2.0",                                 # 2
        "data_origin": "PUBLIC-OPEN-SOURCE",                       # 3
        "source_sensor_id": f"FIXTURE-{code.upper()}-{record_id}",  # 4
        "modality": MODALITY_BY_SOURCE[source_id],                 # 5
        "acquisition_timestamp": record["acquisition_timestamp"],   # 6
        "ingest_timestamp": INGEST_TIMESTAMP,                      # 7 (injected)
        "classification_label": "PROJ-LEVEL-1",                    # 8 baseline
        "domain_label": "DOMAIN-A",                                # 9 baseline
        "release_caveat": [],                                      # 10 baseline
        "handling_instructions": HANDLING,                         # 11
        "provenance_ref": f"manifest://{code}/{record_id}",         # 12 (uri shape)
        "parent_object_ids": [],                                   # 13 (non-derived)
        # 15 policy_binding_state omitted — forced at G1
        "clock_source": "source-metadata",                         # companion of 6
        "source_manifest_ref": f"data/fixtures/source_manifest.json#{source_id}",  # required for PUBLIC-OPEN-SOURCE
        "lifecycle_type": "normalized_observation",                # non-derived
    }
    env["integrity_hash"] = compute_integrity_hash(env)            # 14
    return env


def runtime_ingest(record: Mapping) -> dict:
    """Runtime ingestion path proxy — identical to the fixture builder (GDR-016).

    Kept as a named entry point so LAP-RED-006 can assert train/serve identity by
    comparing the two paths; both delegate to `build_envelope`.
    """
    return build_envelope(record)
