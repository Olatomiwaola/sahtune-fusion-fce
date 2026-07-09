"""TST-UNT-030 — stale object fails closed with RC-004 (FCE-REQ-ING-011, RT-M3S6-05).

RULE-ING-011 freshness gate: an object tick that is older than the deterministic
staleness threshold — or lies in the future (unverifiable) — on the injected clock
yields a fail-closed `reject` carrying RC-004; a fresh control object carries no
RC-004 and proceeds. The decision record records `clock_source` and the staleness
threshold. Substantive anti-replay / trusted time = H4 (explicitly not claimed).

Trace: FCE-REQ-ING-011, RT-M3S6-05, docs/09 item 2.3, docs/17 §3e/§5.
"""
from fce_poc.policy import evaluate
from fce_poc.policy.evaluator import STALENESS_THRESHOLD_TICKS


def _ev(request, bundle, clock, resolvable):
    return evaluate(request, bundle, clock, pinned_version="0.2.0", resolvable_classifications=resolvable)


def test_unt_030_stale_object_rejects_rc004(make_request, bundle, clock, resolvable_classifications):
    # clock now=100; tick=0 is older than the threshold -> stale.
    rec = _ev(make_request(object_timestamp_tick=0), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "reject"                     # fail-closed
    assert rec["disposition"] != "permit"
    assert "RC-004" in rec["reason_codes"]
    assert "RULE-ING-011" in rec["rules_fired"]
    assert rec["clock_source"] == "injected"                  # audit event / decision record
    assert rec["staleness_threshold"] == STALENESS_THRESHOLD_TICKS


def test_unt_030_future_tick_rejects_rc004(make_request, bundle, clock, resolvable_classifications):
    # a future tick (> now) is unverifiable -> fail-closed RC-004.
    rec = _ev(make_request(object_timestamp_tick=10_000), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "reject"
    assert "RC-004" in rec["reason_codes"]


def test_unt_030_fresh_control_no_rc004(make_request, bundle, clock, resolvable_classifications):
    # fresh tick (== now) -> RULE-ING-011 does not fire; the otherwise-valid object permits.
    rec = _ev(make_request(object_timestamp_tick=100), bundle, clock, resolvable_classifications)
    assert "RC-004" not in rec["reason_codes"]
    assert rec["disposition"] == "permit"
