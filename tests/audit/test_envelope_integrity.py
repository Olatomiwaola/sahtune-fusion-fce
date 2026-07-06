"""Envelope integrity tamper-pair (T4) — FCE-DR-SCH-004 D2, FU-M2S3-1, FCE-REQ-MET-010."""

from __future__ import annotations

from fce_poc.audit.envelope_integrity import compute_integrity_hash, verify_integrity


def _envelope():
    env = {
        "object_id": "11111111-1111-4111-8111-111111111111",
        "schema_version": "0.2.0",
        "data_origin": "SYNTHETIC",
        "source_sensor_id": "SENSOR-EO-001",
        "modality": "eo_ir",
        "acquisition_timestamp": "2026-07-06T00:00:00Z",
        "ingest_timestamp": "2026-07-06T00:00:01Z",   # OUT (excluded)
        "classification_label": "PROJ-LEVEL-2",        # IN
        "domain_label": "DOMAIN-A",
        "release_caveat": ["PROJ-CAVEAT-X"],
        "handling_instructions": "handle per synthetic policy",
        "provenance_ref": "graph://node/1",
        "parent_object_ids": [],
        "policy_binding_state": "unvalidated",          # OUT (excluded)
    }
    env["integrity_hash"] = compute_integrity_hash(env)
    return env


def test_t4_tamper_in_field_fails():
    env = _envelope()
    assert verify_integrity(env) is True
    env["classification_label"] = "PROJ-LEVEL-3"  # IN field tampered
    assert verify_integrity(env) is False


def test_t4_tamper_out_field_still_verifies():
    env = _envelope()
    env["policy_binding_state"] = "validated"  # OUT field — not hashed
    assert verify_integrity(env) is True
    env["ingest_timestamp"] = "2026-07-06T09:99:99Z"  # OUT field — not hashed
    assert verify_integrity(env) is True
