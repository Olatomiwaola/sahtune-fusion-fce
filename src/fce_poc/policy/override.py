"""Envelope-bounded operator override (RULE-POL-005, B2; RT-M3S5-01 fix).

An override is valid only when all preconditions hold AND the underlying
decision's reason code is not override_immutable. RC-002 and RC-003 are
override_immutable (B2), so an override can never relax a domain-mismatch block
or an unpermitted cross-domain merge. Time-limit validity uses the injected
clock only (H4).
"""

from __future__ import annotations

from dataclasses import dataclass

from .attributes import InjectedClock
from .reason_codes import is_override_immutable


@dataclass(frozen=True)
class OverrideRequest:
    authority_authenticated: bool
    reason_code: str | None            # RC-007 on success
    audit_signature_placeholder: bool  # placeholder only; no crypto claim
    expires_at_tick: int               # compared to injected clock


def time_limit_valid(override: OverrideRequest, clock: InjectedClock) -> bool:
    """Injected-clock only: valid while now <= expiry. No wall-clock (H4)."""
    return clock.now <= override.expires_at_tick


def override_valid(
    override: OverrideRequest,
    underlying_decision: dict,
    permitted_envelope,
    clock: InjectedClock,
) -> bool:
    """RULE-POL-005. Returns True iff the override may act within the envelope."""
    if not override.authority_authenticated:
        return False
    if not override.reason_code:
        return False
    if not override.audit_signature_placeholder:
        return False
    if not time_limit_valid(override, clock):
        return False
    # Override acts only inside an already-permitted envelope (B2).
    if underlying_decision.get("disposition") not in set(permitted_envelope):
        return False
    # Cannot override a decision carrying an override_immutable reason code (B2).
    if is_override_immutable(underlying_decision.get("reason_code")):
        return False
    return True
