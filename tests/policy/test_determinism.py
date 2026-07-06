"""FCE-REQ-POL-001 — deterministic evaluation.

Repeated evaluation of identical inputs yields an identical decision record and
an identical content hash.
"""

from __future__ import annotations

from fce_poc.policy import evaluate, record_hash


def _ev(request, bundle, clock, resolvable):
    return evaluate(
        request, bundle, clock,
        pinned_version="0.1.0", resolvable_classifications=resolvable,
    )


def test_permit_evaluation_is_deterministic(make_request, bundle, clock, resolvable_classifications):
    r1 = _ev(make_request(), bundle, clock, resolvable_classifications)
    r2 = _ev(make_request(), bundle, clock, resolvable_classifications)
    assert r1 == r2
    assert record_hash(r1) == record_hash(r2)
    assert r1["deterministic_evaluation"] is True


def test_reject_evaluation_is_deterministic(make_request, bundle, clock, resolvable_classifications):
    obj = {"object_id": "det-r", "schema_version": "0.1.0", "data_origin": "SYNTHETIC",
           "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-A"}
    r1 = _ev(make_request(object=obj), bundle, clock, resolvable_classifications)
    r2 = _ev(make_request(object=obj), bundle, clock, resolvable_classifications)
    assert r1 == r2
    assert record_hash(r1) == record_hash(r2)
    assert r1["disposition"] == "reject"
