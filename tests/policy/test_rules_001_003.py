"""TST-POL-001..003 — permit, cross-domain merge block, ambiguous quarantine."""

from __future__ import annotations

from fce_poc.policy import evaluate


def _ev(request, bundle, clock, resolvable):
    return evaluate(
        request, bundle, clock,
        pinned_version="0.1.0", resolvable_classifications=resolvable,
    )


def test_tst_pol_001_same_domain_permit(make_request, bundle, clock, resolvable_classifications):
    rec = _ev(make_request(), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "permit"
    assert "RULE-POL-001" in rec["rules_fired"]
    assert rec["reason_codes"] == []
    assert rec["enforcement_action"] == "release"


def test_tst_pol_002_cross_domain_merge_blocked(make_request, bundle, clock, resolvable_classifications):
    inputs = [
        {"object_id": "in-a", "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-A", "release_caveat": ["PROJ-CAVEAT-X"]},
        {"object_id": "in-b", "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-B", "release_caveat": ["PROJ-CAVEAT-X"]},
    ]
    rec = _ev(make_request(inputs=inputs), bundle, clock, resolvable_classifications)
    # No merge_permits combination exactly matches this cross-domain tuple multiset
    # (M5 Sprint 10: coverage delegated to fusion.permits.covers, exact-multiset) ->
    # block + RC-003 dominates the lattice.
    assert rec["disposition"] == "block"
    assert "RC-003" in rec["reason_codes"]
    assert "RULE-POL-002" in rec["rules_fired"]


def test_tst_pol_003_ambiguous_classification_quarantined(make_request, bundle, clock, resolvable_classifications):
    obj = {"object_id": "amb-1", "classification_label": "PROJ-LEVEL-9",
           "domain_label": "DOMAIN-A", "release_caveat": ["PROJ-CAVEAT-X"],
           "data_origin": "SYNTHETIC", "schema_version": "0.2.0"}
    rec = _ev(make_request(object=obj), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "quarantine"
    assert "RC-005" in rec["reason_codes"]
    assert "RULE-POL-003" in rec["rules_fired"]
    assert rec["disposition"] != "permit"
