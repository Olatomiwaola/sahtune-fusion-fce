"""Envelope integrity_hash — FCE-DR-SCH-004 D2.

Hash domain = CANON-1 over envelope fields 1–6 and 8–13 (12 fields). Excluded:
field 7 ingest_timestamp (FCE-assigned), field 14 integrity_hash (self), field 15
policy_binding_state (FCE-authority-set, B3). G2 integrity check = recompute and
compare; mismatch is the G2 quarantine trigger (RC-001 path).

Scope (per instruction): this module lives in audit/ so the M2 validator stays
untouched; Sprint 8 proves the check via tests, it does not refactor the validator.
"""

from __future__ import annotations

from typing import Mapping

from .canonical import sha256_hex

# Fields 1–6 and 8–13, by name (docs/06 v0.2.0 field numbering).
INTEGRITY_IN_FIELDS = (
    "object_id",              # 1
    "schema_version",         # 2
    "data_origin",            # 3
    "source_sensor_id",       # 4
    "modality",               # 5
    "acquisition_timestamp",  # 6
    # 7 ingest_timestamp — EXCLUDED
    "classification_label",   # 8
    "domain_label",           # 9
    "release_caveat",         # 10
    "handling_instructions",  # 11
    "provenance_ref",         # 12
    "parent_object_ids",      # 13
    # 14 integrity_hash (self), 15 policy_binding_state — EXCLUDED
)


def _in_domain(envelope: Mapping) -> dict:
    missing = [f for f in INTEGRITY_IN_FIELDS if f not in envelope]
    if missing:
        raise ValueError(f"envelope missing integrity IN-fields: {missing}")
    return {field: envelope[field] for field in INTEGRITY_IN_FIELDS}


def compute_integrity_hash(envelope: Mapping) -> str:
    """sha-256 (CANON-1) over the 12 IN fields."""
    return sha256_hex(_in_domain(envelope))


def verify_integrity(envelope: Mapping) -> bool:
    """Recompute and compare against the stored integrity_hash."""
    return compute_integrity_hash(envelope) == envelope.get("integrity_hash")
