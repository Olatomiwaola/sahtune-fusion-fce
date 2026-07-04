"""Object envelope and the SINGLE normalization function (GDR-016).

The 15-field object metadata schema is frozen at v0.2.0
(docs/05_data_model/m2-schema-freeze-record.md, FCE-DR-SCH-001/002). This module
holds the Envelope dataclass and `normalize()` — the one normalization function
used by BOTH the fixture builder and the runtime path. GDR-016 (normalization
identity) requires that fixtures are built the same way runtime input is parsed;
tests that build envelopes from JSON therefore call `normalize()` too.

Distinctions preserved by normalization (needed for the null-vs-empty rules,
LAP-UNIT-009):
  - field absent in the source        -> MISSING sentinel
  - field present with JSON null       -> None
  - field present with empty list []   -> []
Unknown/extra keys are captured in `unknown_fields` so the validator can apply
the interim fail-closed disposition (RT-M2S3-03 / FU-M2S3-2).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


class _Missing:
    """Singleton marker for 'field absent in source', distinct from JSON null."""

    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return "MISSING"

    def __bool__(self) -> bool:
        return False


MISSING = _Missing()

# The 15 mandatory fields, in schema field-number order (docs/06 v0.2.0).
MANDATORY_FIELDS: tuple[str, ...] = (
    "object_id",              # 1
    "schema_version",         # 2
    "data_origin",            # 3
    "source_sensor_id",       # 4
    "modality",               # 5
    "acquisition_timestamp",  # 6
    "ingest_timestamp",       # 7
    "classification_label",   # 8
    "domain_label",           # 9
    "release_caveat",         # 10
    "handling_instructions",  # 11
    "provenance_ref",         # 12
    "parent_object_ids",      # 13
    "integrity_hash",         # 14
    "policy_binding_state",   # 15 (FCE-authority-set; forced at G1, never trusted)
)

# Companion / advisory keys that are part of the frozen schema but not themselves
# one of the 15 mandatory fields:
#   clock_source        - companion of field 6 (acquisition_timestamp)
#   source_manifest_ref - required only when data_origin = PUBLIC-OPEN-SOURCE (field 3)
#   lifecycle_type      - declares the object lifecycle type (drives the field-13 rule)
#   ai_confidence       - advisory attribute, never a gate input (shared constraint 2)
COMPANION_FIELDS: tuple[str, ...] = (
    "clock_source",
    "source_manifest_ref",
    "lifecycle_type",
    "ai_confidence",
)

KNOWN_FIELDS: tuple[str, ...] = MANDATORY_FIELDS + COMPANION_FIELDS


@dataclass(frozen=True)
class Envelope:
    """A normalized object envelope. Absent fields hold the MISSING sentinel."""

    object_id: Any = MISSING
    schema_version: Any = MISSING
    data_origin: Any = MISSING
    source_sensor_id: Any = MISSING
    modality: Any = MISSING
    acquisition_timestamp: Any = MISSING
    ingest_timestamp: Any = MISSING
    classification_label: Any = MISSING
    domain_label: Any = MISSING
    release_caveat: Any = MISSING
    handling_instructions: Any = MISSING
    provenance_ref: Any = MISSING
    parent_object_ids: Any = MISSING
    integrity_hash: Any = MISSING
    policy_binding_state: Any = MISSING
    clock_source: Any = MISSING
    source_manifest_ref: Any = MISSING
    lifecycle_type: Any = MISSING
    ai_confidence: Any = MISSING
    unknown_fields: tuple[str, ...] = field(default_factory=tuple)


def normalize(raw: Mapping[str, Any]) -> Envelope:
    """The single normalization function (GDR-016).

    Maps a raw mapping (e.g. a parsed JSON object) to an Envelope, preserving the
    absent / null / empty distinctions and recording any unknown keys. Pure and
    deterministic: identical input yields an equal Envelope (supports RULE-VAL-018).
    """
    if not isinstance(raw, Mapping):
        raise TypeError(f"normalize() expects a mapping, got {type(raw).__name__}")

    values = {name: raw.get(name, MISSING) for name in KNOWN_FIELDS}
    unknown = tuple(sorted(k for k in raw if k not in KNOWN_FIELDS))
    return Envelope(unknown_fields=unknown, **values)
