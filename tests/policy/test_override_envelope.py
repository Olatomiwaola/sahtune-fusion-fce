"""TST-POL-005a..e — envelope-bounded override (RULE-POL-005, B2; RT-M3S5-01 fix).

Time-limit validity uses the injected clock only (H4). 005d exercises the RC-002
override_immutable path; 005e exercises expiry by injected clock.
"""

from __future__ import annotations

from fce_poc.policy import InjectedClock, OverrideRequest, override_valid

# An "already-permitted envelope" of dispositions an override may act within (B2).
ENVELOPE = frozenset({"permit", "restrict", "route-to-higher-domain", "transform"})
CLOCK = InjectedClock(now=100)


def _override(**overrides):
    base = dict(
        authority_authenticated=True,
        reason_code="RC-007",
        audit_signature_placeholder=True,
        expires_at_tick=200,
    )
    base.update(overrides)
    return OverrideRequest(**base)


def test_tst_pol_005a_valid_override_accepted():
    underlying = {"disposition": "restrict", "reason_code": None}
    assert override_valid(_override(), underlying, ENVELOPE, CLOCK) is True


def test_tst_pol_005b_override_vs_rc003_cross_domain_block_rejected():
    underlying = {"disposition": "block", "reason_code": "RC-003"}
    assert override_valid(_override(), underlying, ENVELOPE, CLOCK) is False


def test_tst_pol_005c_missing_precondition_rejected():
    underlying = {"disposition": "restrict", "reason_code": None}
    assert override_valid(_override(authority_authenticated=False), underlying, ENVELOPE, CLOCK) is False


def test_tst_pol_005d_override_vs_rc002_immutable_rejected():
    # Disposition IS within the envelope, so only the RC-002 override_immutable
    # flag can reject this — isolates the RT-M3S5-01 fix.
    underlying = {"disposition": "restrict", "reason_code": "RC-002"}
    assert override_valid(_override(), underlying, ENVELOPE, CLOCK) is False


def test_tst_pol_005e_expired_override_rejected():
    underlying = {"disposition": "restrict", "reason_code": None}
    expired = _override(expires_at_tick=50)  # < clock.now (100)
    assert override_valid(expired, underlying, ENVELOPE, CLOCK) is False
