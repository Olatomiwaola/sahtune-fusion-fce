"""G2 validation and the G1->G2 evaluation pipeline.

Implements RULE-VAL-001 and RULE-VAL-004..016 per
docs/05_data_model/m2-validation-rules.md, plus RULE-VAL-005 (synthetic banner
output) and the interim unknown-field disposition. RULE-VAL-002/003/017 live in
gates.py; RULE-VAL-018 (determinism) is a property verified by the tests.

Design points required by the M2 block:
  - Disposition record: {disposition, reason_code, failed_rules, detection_flags,
    synthetic_banner}.
  - Fail-closed at G2 is a quarantine with reason code RC-001.
  - Multi-failure determinism: ALL failed rules are reported (no first-failure
    short-circuit); failed_rules and detection_flags are sorted for a deterministic
    disposition (RULE-VAL-018).
  - Audit emission is a STUB INTERFACE ONLY. M4 owns the append-only audit writer
    (docs/08). No audit claims are made at M2.

Reason code note: RC-001 is the only fail-closed reason code available at M2 (RTM
v0.2 acceptance criteria, M2 block). The full reason-code registry lives in
docs/07_policy-decision-model.md (not in scope this sprint); a registry-consistency
check is flagged for a later sprint. G1 rejections and G2 quarantines are
distinguished by the `disposition` field ('rejected' vs 'quarantined').
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from .envelope import MISSING, Envelope, normalize
from .gates import force_policy_binding_state, g1_version_origin_gate
from .taxonomy import Taxonomy

REASON_CODE_FAIL_CLOSED = "RC-001"

SYNTHETIC_ORIGINS = frozenset({"SYNTHETIC", "SYNTHETIC-DERIVED"})

# Lifecycle types that MUST carry non-empty parentage (field 13). Detection at M2
# is by the fixture-declared lifecycle_type; enforcement that fused outputs carry
# true parentage is M5 (FCE-REQ-KRN-011, H1).
DERIVED_MERGED_TYPES = frozenset(
    {"tracklet", "fused_track", "transformed_object", "downgraded_object"}
)

# Interim disposition marker for unknown/extra envelope fields. The accept-and-ignore
# vs reject decision is not defined in docs/06 and is deferred to the architect
# (RT-M2S3-03 / FU-M2S3-2). Interim Sprint 4 behaviour is an explicit, tested choice:
# default fail-closed.
UNKNOWN_FIELD_RULE = "UNKNOWN-FIELD"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})$"
)


@dataclass(frozen=True)
class Disposition:
    """The validator's per-object disposition output."""

    disposition: str  # 'accepted' | 'quarantined' | 'rejected'
    reason_code: str | None
    failed_rules: tuple[str, ...]
    detection_flags: tuple[str, ...]
    synthetic_banner: bool


class AuditSink(Protocol):
    """Interface the M4 audit writer will implement. Stub only at M2."""

    def emit(self, disposition: Disposition, envelope: Envelope) -> None: ...


class NullAuditSink:
    """No-op audit stub. M4 owns the real append-only writer (docs/08).

    Present only to fix the interface shape; makes no audit claim at M2.
    """

    def emit(self, disposition: Disposition, envelope: Envelope) -> None:
        return None


# --- field-level predicates -------------------------------------------------

def _is_nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _is_uuid(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True


def _is_rfc3339(value: Any) -> bool:
    return isinstance(value, str) and bool(_RFC3339_RE.match(value))


def _is_sha256_format(value: Any) -> bool:
    # Format only. Hash VERIFICATION is explicitly deferred pending the
    # hash-input-domain definition (RULE-VAL-016, freeze record field 14).
    return isinstance(value, str) and bool(_SHA256_RE.match(value))


def _is_provenance_ref(value: Any) -> bool:
    # uri / graph-node-id shape only; resolvability is M4 provenance-graph scope.
    return (
        isinstance(value, str)
        and value.strip() != ""
        and not any(ch.isspace() for ch in value)
        and ":" in value
    )


# --- G2 validation ----------------------------------------------------------

def validate_g2(env: Envelope, taxonomy: Taxonomy) -> tuple[tuple[str, ...], bool]:
    """Run all G2 field rules. Returns (sorted failed rule IDs, synthetic_banner).

    No short-circuit: every rule is evaluated so that all failures are reported.
    """
    failed: list[str] = []

    # RULE-VAL-001 object_id present, valid uuid (duplicate-ID handling pending).
    if not _is_uuid(env.object_id):
        failed.append("RULE-VAL-001")

    # RULE-VAL-004 PUBLIC-OPEN-SOURCE requires a source-manifest reference (presence).
    if env.data_origin == "PUBLIC-OPEN-SOURCE" and not _is_nonempty_str(
        env.source_manifest_ref
    ):
        failed.append("RULE-VAL-004")

    # RULE-VAL-006 source_sensor_id present, non-empty string.
    if not _is_nonempty_str(env.source_sensor_id):
        failed.append("RULE-VAL-006")

    # RULE-VAL-007 modality present and within the taxonomy fixture enum.
    if not (_is_nonempty_str(env.modality) and taxonomy.contains("modality", env.modality)):
        failed.append("RULE-VAL-007")

    # RULE-VAL-008 acquisition_timestamp RFC3339 + clock_source present, non-empty.
    if not (_is_rfc3339(env.acquisition_timestamp) and _is_nonempty_str(env.clock_source)):
        failed.append("RULE-VAL-008")

    # RULE-VAL-009 ingest_timestamp present, valid RFC3339.
    if not _is_rfc3339(env.ingest_timestamp):
        failed.append("RULE-VAL-009")

    # RULE-VAL-010 classification_label within the project-taxonomy fixture enum.
    if not (
        _is_nonempty_str(env.classification_label)
        and taxonomy.contains("classification_label", env.classification_label)
    ):
        failed.append("RULE-VAL-010")

    # RULE-VAL-011 domain_label within the project-taxonomy fixture enum.
    if not (
        _is_nonempty_str(env.domain_label)
        and taxonomy.contains("domain_label", env.domain_label)
    ):
        failed.append("RULE-VAL-011")

    # RULE-VAL-012 release_caveat is a list (empty permitted, null fails); members in taxonomy.
    release_caveat = env.release_caveat
    if not isinstance(release_caveat, list) or not all(
        isinstance(member, str) and taxonomy.contains("release_caveat", member)
        for member in release_caveat
    ):
        failed.append("RULE-VAL-012")

    # RULE-VAL-013 handling_instructions present, non-empty string.
    if not _is_nonempty_str(env.handling_instructions):
        failed.append("RULE-VAL-013")

    # RULE-VAL-014 provenance_ref present, non-empty, uri/graph-node-id shape.
    if not _is_provenance_ref(env.provenance_ref):
        failed.append("RULE-VAL-014")

    # RULE-VAL-015 parent_object_ids: list of uuids (null fails); non-empty for
    # derived/merged lifecycle types, empty otherwise.
    parents = env.parent_object_ids
    if not isinstance(parents, list) or not all(_is_uuid(p) for p in parents):
        failed.append("RULE-VAL-015")
    else:
        derived = env.lifecycle_type in DERIVED_MERGED_TYPES
        if derived and len(parents) == 0:
            failed.append("RULE-VAL-015")
        elif not derived and len(parents) > 0:
            failed.append("RULE-VAL-015")

    # RULE-VAL-016 integrity_hash present, sha-256 FORMAT only (verification deferred).
    if not _is_sha256_format(env.integrity_hash):
        failed.append("RULE-VAL-016")

    # Interim: unknown/extra envelope fields fail closed (RT-M2S3-03 / FU-M2S3-2).
    if env.unknown_fields:
        failed.append(UNKNOWN_FIELD_RULE)

    # RULE-VAL-005 synthetic banner flag is validator output (not a failure condition).
    banner = env.data_origin in SYNTHETIC_ORIGINS

    return tuple(sorted(failed)), banner


# --- G1 -> G2 pipeline ------------------------------------------------------

def evaluate(
    raw: Mapping[str, Any],
    taxonomy: Taxonomy,
    audit_sink: AuditSink | None = None,
) -> Disposition:
    """Normalize -> G1 (force field 15, version/origin gate) -> G2 -> disposition.

    Deterministic: identical (raw, taxonomy) yields an identical Disposition
    (RULE-VAL-018).
    """
    env = normalize(raw)

    # G1 step 1: force field 15 BEFORE any validation reads it; record detection.
    env, detection_flags = force_policy_binding_state(env)
    detection_flags = tuple(sorted(detection_flags))

    # Banner keys off data_origin regardless of overall disposition (RULE-VAL-005).
    banner = env.data_origin in SYNTHETIC_ORIGINS

    # G1 step 2/3: envelope-version + data_origin gate. Reject fail-closed before policy.
    gate = g1_version_origin_gate(env)
    if not gate.passed:
        disposition = Disposition(
            disposition="rejected",
            reason_code=REASON_CODE_FAIL_CLOSED,
            failed_rules=gate.failed_rules,
            detection_flags=detection_flags,
            synthetic_banner=banner,
        )
    else:
        failed_rules, banner = validate_g2(env, taxonomy)
        if failed_rules:
            disposition = Disposition(
                disposition="quarantined",
                reason_code=REASON_CODE_FAIL_CLOSED,
                failed_rules=failed_rules,
                detection_flags=detection_flags,
                synthetic_banner=banner,
            )
        else:
            disposition = Disposition(
                disposition="accepted",
                reason_code=None,
                failed_rules=(),
                detection_flags=detection_flags,
                synthetic_banner=banner,
            )

    # Audit emission is a stub interface only at M2 (M4 owns the writer).
    (audit_sink or NullAuditSink()).emit(disposition, env)
    return disposition
