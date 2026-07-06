"""Replay — R1 delegation + R2 decision-sequence reconstruction (FCE-REQ-AUD-003).

R2 reconstructs the ordered decision sequence from the JSONL alone and verifies
internal consistency: dispositions ∈ D3 lattice, reason codes ∈ closed registry,
bundle-version continuity (non-decreasing semver), sentinel legality per class.
Lineage resolution reads source_object_ids / output_object_id ONLY — never
event_detail.source_asserted_object_id (RT-M4S7-03).

R3 (re-evaluation cross-check) is NOT implemented this sprint (optional by spec);
stated in EVD-M4.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .chain import load_records, verify_chain
from .records import LATTICE_SET, RC_SET, bundle_is_legal, _is_semver


@dataclass(frozen=True)
class Decision:
    audit_event_id: str
    event_type: str
    source_object_ids: tuple
    output_object_id: object
    policy_bundle_version: str
    policy_rule_ids: tuple
    disposition: str
    reason_codes: tuple


@dataclass
class ReplayResult:
    ok: bool
    r1_ok: bool
    decisions: list
    errors: list = field(default_factory=list)


def _semver_tuple(value):
    return tuple(int(part) for part in value.split("."))


def reconstruct(path) -> ReplayResult:
    r1 = verify_chain(path)
    records = load_records(path)
    decisions = []
    errors = []
    semver_seq = []

    for rec in records:
        cls = rec.get("event_type")
        disposition = rec.get("disposition")
        reason_codes = rec.get("reason_codes", [])
        bundle = rec.get("policy_bundle_version")

        if disposition not in LATTICE_SET:
            errors.append(f"{rec.get('audit_event_id')}: disposition {disposition!r} not in D3 lattice")
        if not set(reason_codes) <= RC_SET:
            errors.append(f"{rec.get('audit_event_id')}: reason code outside closed registry")
        if not bundle_is_legal(cls, bundle):
            errors.append(f"{rec.get('audit_event_id')}: illegal sentinel/bundle {bundle!r} for {cls}")
        if _is_semver(bundle):
            semver_seq.append(bundle)

        # Lineage uses trusted fields ONLY (never detail.source_asserted_object_id).
        decisions.append(Decision(
            audit_event_id=rec.get("audit_event_id"),
            event_type=cls,
            source_object_ids=tuple(rec.get("source_object_ids", [])),
            output_object_id=rec.get("output_object_id"),
            policy_bundle_version=bundle,
            policy_rule_ids=tuple(rec.get("policy_rule_ids", [])),
            disposition=disposition,
            reason_codes=tuple(reason_codes),
        ))

    for earlier, later in zip(semver_seq, semver_seq[1:]):
        if _semver_tuple(later) < _semver_tuple(earlier):
            errors.append(f"bundle-version continuity broken: {earlier} -> {later}")
            break

    return ReplayResult(ok=(r1.ok and not errors), r1_ok=r1.ok, decisions=decisions, errors=errors)
