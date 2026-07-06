"""Audit record construction + validation (internal helper).

Approved decomposition (project-lead override, M4 Sprint 8): record
construction/validation is separated from writer I/O. The action list, reason-code
registry, and D3 lattice are imported from the M3 policy modules (docs/07-derived,
guarded by the M3 registry guard) — not re-hardcoded here.

Validation covers: the 9 closed event classes, structured event_timestamp,
bundle-version semver-or-legal-sentinel per class, reason_codes ⊆ RC-001..012,
enforcement_action ∈ the 11 actions, disposition ∈ the 9 D3 values, confidence
must be null, the per-class requiredness matrix, and the closed per-class
event_detail (unknown detail fields refused; ingest_attempt_id mandatory for
ingestion). Field 14 (content hash) and field 15 (previous hash) are chain-set by
the writer and are not part of the constructed body.
"""

from __future__ import annotations

import re

from fce_poc.policy.actions import ACTIONS, SEVERITY_ORDER
from fce_poc.policy.reason_codes import REASON_CODES

EVENT_CLASSES = (
    "ingestion", "transformation", "policy-decision", "fusion-decision",
    "routing", "quarantine", "downgrade", "export", "override",
)

BUNDLE_SENTINELS = frozenset({"N/A-PRE-G4", "N/A-EXPORT"})
_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

KNOWN_RULE_IDS = frozenset(f"RULE-POL-{i:03d}" for i in range(1, 7))  # docs/07 RULE-POL-001..006
ACTIONS_SET = frozenset(ACTIONS)
LATTICE_SET = frozenset(SEVERITY_ORDER)
RC_SET = frozenset(REASON_CODES)

SIGNATURE_PLACEHOLDER = "PLACEHOLDER-NO-CRYPTO-H6"
EXPORT_STATUS_VALUES = frozenset({"not-exported", "exported"})
REVIEW_STATUS_VALUES = frozenset({"unreviewed", "reviewed"})

# Closed per-class event_detail schemas (unknown keys refused).
DETAIL_SCHEMA = {
    "ingestion": {
        "required": {"ingest_attempt_id"},
        "optional": {"source_asserted_object_id", "object_id_authenticated",
                     "detection_flags", "validation_rule_refs"},
    },
    "transformation": {"required": {"transformation_ref"}, "optional": set()},
    "policy-decision": {
        # Required per docs/07 D4 atomic emission (FU-M4S8-1, 2026-07-06).
        "required": {"pip_attributes_consumed", "detection_flags", "deterministic_evaluation"},
        "optional": set(),
    },
    "fusion-decision": {"required": set(), "optional": {"merge_permit_ref", "rc003_context"}},
    "routing": {"required": {"destination_domain"}, "optional": set()},
    "quarantine": {"required": {"review_queue_ref"}, "optional": set()},
    "downgrade": {"required": {"authority_ref", "transformation_proof_ref"}, "optional": set()},
    "export": {"required": {"manifest_ref", "record_range", "manifest_sha256"}, "optional": set()},
    "override": {
        "required": {"precondition_results", "envelope_check", "override_immutable_check"},
        "optional": set(),
    },
}

# Requiredness matrix (docs/08). downgrade is not in the docs/08 matrix table;
# minimal requiredness supplied by ENGINEERING JUDGMENT (recorded in EVD-M4).
SRC_MIN = {
    "ingestion": 0, "transformation": 1, "policy-decision": 1, "fusion-decision": 2,
    "routing": 1, "quarantine": 1, "downgrade": 1, "export": 0, "override": 1,
}
SRC_EXACT_EMPTY = frozenset({"export"})
RULES_MIN = {
    "ingestion": 0, "transformation": 0, "policy-decision": 0, "fusion-decision": 1,
    "routing": 1, "quarantine": 0, "downgrade": 1, "export": 0, "override": 1,
}
RULES_EXACT_EMPTY = frozenset({"export"})

# Common field order (18), for stable record construction. 14/15 are chain-set.
COMMON_FIELDS = (
    "audit_event_id", "event_type", "event_timestamp", "actor_identity",
    "source_object_ids", "output_object_id", "policy_bundle_version",
    "policy_rule_ids", "decision", "reason_codes", "enforcement_action",
    "disposition", "confidence", "record_content_hash", "previous_record_hash",
    "signature_placeholder", "export_status", "review_status",
)


class RecordValidationError(ValueError):
    """Raised on any record-schema violation; the writer refuses fail-closed."""


def _is_semver(value) -> bool:
    return isinstance(value, str) and bool(_SEMVER_RE.match(value))


def _nonempty_str(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def new_record(*, audit_event_id, event_type, event_timestamp, actor_identity,
               source_object_ids, output_object_id, policy_bundle_version,
               policy_rule_ids, decision, reason_codes, enforcement_action,
               disposition, event_detail, confidence=None,
               export_status="not-exported", review_status="unreviewed",
               signature_placeholder=SIGNATURE_PLACEHOLDER) -> dict:
    """Construct a record body (fields 1–13, 16–18, event_detail). No 14/15."""
    return {
        "audit_event_id": audit_event_id,
        "event_type": event_type,
        "event_timestamp": event_timestamp,
        "actor_identity": actor_identity,
        "source_object_ids": list(source_object_ids),
        "output_object_id": output_object_id,
        "policy_bundle_version": policy_bundle_version,
        "policy_rule_ids": list(policy_rule_ids),
        "decision": decision,
        "reason_codes": list(reason_codes),
        "enforcement_action": enforcement_action,
        "disposition": disposition,
        "confidence": confidence,
        "signature_placeholder": signature_placeholder,
        "export_status": export_status,
        "review_status": review_status,
        "event_detail": event_detail,
    }


def bundle_is_legal(cls, value) -> bool:
    """Per-class policy_bundle_version legality (semver or class-legal sentinel)."""
    if cls == "ingestion":
        return value == "N/A-PRE-G4"
    if cls == "export":
        return value == "N/A-EXPORT"
    if cls == "quarantine":
        return value == "N/A-PRE-G4" or _is_semver(value)
    return _is_semver(value)


def _validate_bundle(cls, value):
    if not bundle_is_legal(cls, value):
        raise RecordValidationError(f"{cls}: illegal policy_bundle_version {value!r}")


def _validate_output(cls, value, reason_codes):
    if cls in ("ingestion", "quarantine", "export", "override"):
        ok = value is None
    elif cls in ("transformation", "downgrade"):
        ok = _nonempty_str(value)
    elif cls == "policy-decision":
        ok = value is None or _nonempty_str(value)
    elif cls == "routing":
        ok = value is None or _nonempty_str(value)
    elif cls == "fusion-decision":
        ok = (value is None) if "RC-003" in reason_codes else _nonempty_str(value)
    else:
        ok = True
    if not ok:
        raise RecordValidationError(f"{cls}: illegal output_object_id {value!r}")


def _validate_detail(cls, detail):
    if not isinstance(detail, dict):
        raise RecordValidationError(f"{cls}: event_detail must be an object")
    schema = DETAIL_SCHEMA[cls]
    allowed = schema["required"] | schema["optional"]
    unknown = set(detail) - allowed
    if unknown:
        raise RecordValidationError(f"{cls}: unknown event_detail fields {sorted(unknown)}")
    missing = schema["required"] - set(detail)
    if missing:
        raise RecordValidationError(f"{cls}: missing required event_detail {sorted(missing)}")
    if cls == "ingestion" and not _nonempty_str(detail.get("ingest_attempt_id")):
        raise RecordValidationError("ingestion: ingest_attempt_id must be a non-empty uuid string")


def validate_record_body(rec: dict) -> None:
    """Validate a constructed record body. Raises RecordValidationError."""
    cls = rec.get("event_type")
    if cls not in EVENT_CLASSES:
        raise RecordValidationError(f"event_type not in the closed 9-class set: {cls!r}")

    if not _nonempty_str(rec.get("audit_event_id")):
        raise RecordValidationError("audit_event_id must be a non-empty uuid string")

    ts = rec.get("event_timestamp")
    if not isinstance(ts, dict) or set(ts) != {"ts", "clock_source"}:
        raise RecordValidationError("event_timestamp must be {ts, clock_source} exactly")
    if not _nonempty_str(ts.get("ts")) or not _nonempty_str(ts.get("clock_source")):
        raise RecordValidationError("event_timestamp.ts and .clock_source must be non-empty")

    if not _nonempty_str(rec.get("actor_identity")):
        raise RecordValidationError("actor_identity must be a non-empty string")

    src = rec.get("source_object_ids")
    if not isinstance(src, list) or not all(_nonempty_str(x) for x in src):
        raise RecordValidationError("source_object_ids must be a list of non-empty id strings")
    if cls in SRC_EXACT_EMPTY:
        if len(src) != 0:
            raise RecordValidationError(f"{cls}: source_object_ids must be empty")
    elif len(src) < SRC_MIN[cls]:
        raise RecordValidationError(f"{cls}: source_object_ids needs >= {SRC_MIN[cls]}")

    reason_codes = rec.get("reason_codes")
    if not isinstance(reason_codes, list) or not set(reason_codes) <= RC_SET:
        raise RecordValidationError(f"reason_codes must be a list within {sorted(RC_SET)}")

    _validate_output(cls, rec.get("output_object_id"), reason_codes)
    _validate_bundle(cls, rec.get("policy_bundle_version"))

    rules = rec.get("policy_rule_ids")
    if not isinstance(rules, list) or not set(rules) <= KNOWN_RULE_IDS:
        raise RecordValidationError(f"policy_rule_ids must be a list within {sorted(KNOWN_RULE_IDS)}")
    if cls in RULES_EXACT_EMPTY and len(rules) != 0:
        raise RecordValidationError(f"{cls}: policy_rule_ids must be empty")
    if len(rules) < RULES_MIN[cls]:
        raise RecordValidationError(f"{cls}: policy_rule_ids needs >= {RULES_MIN[cls]}")

    if not _nonempty_str(rec.get("decision")):
        raise RecordValidationError("decision must be a non-empty string")

    if rec.get("enforcement_action") not in ACTIONS_SET:
        raise RecordValidationError(f"enforcement_action not in the 11 actions: {rec.get('enforcement_action')!r}")

    if rec.get("disposition") not in LATTICE_SET:
        raise RecordValidationError(f"disposition not a D3 lattice value: {rec.get('disposition')!r}")

    if rec.get("confidence") is not None:
        raise RecordValidationError("confidence must be null at TRL 1-3 (FCE-DR-SCH-004)")

    if rec.get("export_status") not in EXPORT_STATUS_VALUES:
        raise RecordValidationError("export_status invalid")
    if rec.get("review_status") not in REVIEW_STATUS_VALUES:
        raise RecordValidationError("review_status invalid")
    if not _nonempty_str(rec.get("signature_placeholder")):
        raise RecordValidationError("signature_placeholder must be a non-empty placeholder string")

    _validate_detail(cls, rec.get("event_detail"))
