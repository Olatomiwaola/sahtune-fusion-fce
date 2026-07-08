"""TST-POL-006a..c — deny-overrides conflict combination (RULE-POL-006, D3 lattice)."""

from __future__ import annotations

from fce_poc.policy import evaluate, most_restrictive


def test_tst_pol_006a_permit_restrict_yields_restrict():
    assert most_restrictive(["permit", "restrict"]) == "restrict"


def test_tst_pol_006b_permit_block_yields_block():
    assert most_restrictive(["permit", "block"]) == "block"


def test_tst_pol_006c_unresolvable_quarantines_never_permit(make_request, bundle, clock, resolvable_classifications):
    obj = {"object_id": "amb-2", "classification_label": "PROJ-LEVEL-UNKNOWN",
           "domain_label": "DOMAIN-A", "release_caveat": ["PROJ-CAVEAT-X"],
           "data_origin": "SYNTHETIC", "schema_version": "0.2.0"}
    rec = evaluate(
        make_request(object=obj), bundle, clock,
        pinned_version="0.2.0", resolvable_classifications=resolvable_classifications,
    )
    assert rec["disposition"] == "quarantine"
    assert "RC-005" in rec["reason_codes"]
    assert rec["disposition"] != "permit"
