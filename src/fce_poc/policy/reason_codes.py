"""Closed reason-code registry mirror (docs/07 "Reason-code registry (CLOSED — v1)").

This is a code mirror of the authoritative registry in docs/07; the guard test
(test_registry_guard.py) asserts the codes used here are a subset of the docs/07
registry, so the two cannot drift silently.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReasonCode:
    code: str
    meaning: str
    override_immutable: bool


# override_immutable: true = no operator override may act against a decision
# carrying this code (RT-M3S5-01; B2 for RC-002/RC-003).
REASON_CODES: dict[str, ReasonCode] = {
    "RC-001": ReasonCode("RC-001", "Missing or malformed mandatory metadata", False),
    "RC-002": ReasonCode("RC-002", "Classification/domain/caveat mismatch with channel (B2)", True),
    "RC-003": ReasonCode("RC-003", "No explicit permit for cross-domain merge (B2)", True),
    "RC-004": ReasonCode("RC-004", "Stale or unverifiable timestamp", False),
    "RC-005": ReasonCode("RC-005", "Ambiguous condition; enqueue human review", False),
    "RC-006": ReasonCode("RC-006", "Authorized downgrade with valid transformation proof", False),
    "RC-007": ReasonCode("RC-007", "Authenticated override within time limit (envelope-bounded; see B2)", False),
    "RC-008": ReasonCode("RC-008", "Unverifiable or unauthenticated PIP attribute; fail closed at G4", False),
    "RC-009": ReasonCode("RC-009", "G1 reject: unsupported schema_version (envelope-version gate, GDR-006)", False),
    "RC-010": ReasonCode("RC-010", "G1 reject: unsupported data_origin (LIVE at TRL 1-3 per FCE-DR-SCH-002)", False),
    "RC-011": ReasonCode("RC-011", "G1 reject: source authentication failure (H14 audit hook)", False),
    "RC-012": ReasonCode("RC-012", "G1 detection (non-reject): source-supplied policy_binding_state forced unvalidated", False),
}


def is_override_immutable(code: str | None) -> bool:
    rc = REASON_CODES.get(code) if code is not None else None
    return bool(rc and rc.override_immutable)
