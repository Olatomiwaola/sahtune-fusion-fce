"""TST-POL-004 — PIP attribute authentication (B1 / FCE-REQ-SEC-002).

A spoofed or unauthenticated attribute fails closed at G4 with RC-008; no decision
consumes the attribute. RC-011/RC-008 authN here is mechanism-simulated (fixture
flags), not demonstrated authentication (H3/H4) — see EVD-M3.
"""

from __future__ import annotations

from fce_poc.policy import evaluate


def _ev(request, bundle, clock, resolvable):
    return evaluate(
        request, bundle, clock,
        pinned_version="0.2.0", resolvable_classifications=resolvable,
    )


def test_tst_pol_004_spoofed_attribute_fails_closed(make_request, bundle, clock, resolvable_classifications, pip_spoofed):
    rec = _ev(make_request(pip_attributes=pip_spoofed), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "block"
    assert "RC-008" in rec["reason_codes"]
    assert "RULE-POL-004" in rec["rules_fired"]
    assert any(f.startswith("pip-failed:") for f in rec["detection_flags"])


def test_tst_pol_004_unauthenticated_attribute_fails_closed(make_request, bundle, clock, resolvable_classifications, pip_unauthenticated):
    rec = _ev(make_request(pip_attributes=pip_unauthenticated), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "block"
    assert "RC-008" in rec["reason_codes"]
    assert "RULE-POL-004" in rec["rules_fired"]


def test_valid_pip_does_not_trip_rule_004(make_request, bundle, clock, resolvable_classifications):
    rec = _ev(make_request(), bundle, clock, resolvable_classifications)
    assert "RULE-POL-004" not in rec["rules_fired"]
    assert "RC-008" not in rec["reason_codes"]
