"""TST-PRP-011 — D3 severity-lattice total-order property (RT-M3S6-03, new).

`most_restrictive()` over >=3-way and 4-way combinations: order-independent (all
permutations agree), idempotent, transitive per the FCE-DR-POL-001 total order;
authority-gated dispositions (downgrade/override) fail closed.

Trace: FCE-DR-POL-001, RT-M3S6-03, docs/17 §3e.
"""
import itertools

import pytest

from fce_poc.policy.actions import AUTHORITY_GATED, SEVERITY_ORDER, most_restrictive


def test_prp_011_order_independent_3way_and_4way():
    for combo in (
        ["permit", "block", "quarantine"],
        ["restrict", "block", "reject", "permit"],
        ["segregate", "quarantine", "permit", "block"],
    ):
        results = {most_restrictive(list(p)) for p in itertools.permutations(combo)}
        assert len(results) == 1  # order-independent over all permutations


def test_prp_011_idempotent():
    for combo in (["permit"], ["block", "permit"], ["reject", "quarantine", "block"]):
        r = most_restrictive(combo)
        assert most_restrictive([r]) == r
        assert most_restrictive([r] + combo) == r  # re-adding the result is a no-op


def test_prp_011_follows_fce_dr_pol_001_total_order():
    assert most_restrictive(["permit", "reject", "block"]) == "reject"
    assert most_restrictive(["permit", "block", "quarantine"]) == "quarantine"
    assert most_restrictive(["permit", "restrict", "block"]) == "block"
    assert most_restrictive(["permit"]) == "permit"
    # transitivity across the whole order: each item outranks its successor
    ranked = list(SEVERITY_ORDER)
    for i in range(len(ranked) - 1):
        assert most_restrictive([ranked[i], ranked[i + 1]]) == ranked[i]


def test_prp_011_authority_gated_fail_closed():
    for gated in AUTHORITY_GATED:  # downgrade, override — never lattice products
        with pytest.raises(ValueError):
            most_restrictive([gated, "permit"])
