"""TST-PRP-001 breadth extension — evaluate() determinism across ALL reachable
disposition classes (RT-M3S6-02), not only permit/reject.

Each reachable class is evaluated twice and the FULL decision tuple (the canonical
record: decision, reason_codes, enforcement_action, disposition, detection_flags,
rules_fired, ...) must be byte-identical. Reachable evaluate() classes:
permit (RULE-POL-001), reject (G1 unsupported schema), reject+RC-004 (RULE-ING-011
staleness — distinct reason-code set), block (cross-domain merge / default-deny),
quarantine (ambiguous classification).

Trace: FCE-REQ-POL-001, RT-M3S6-02, docs/17 §3e.
"""
from fce_poc.policy import evaluate
from fce_poc.policy.evaluator import record_canonical


def _ev(request, bundle, clock, resolvable):
    return evaluate(request, bundle, clock, pinned_version="0.2.0", resolvable_classifications=resolvable)


def test_prp_001_breadth_all_classes_deterministic(make_request, bundle, clock, resolvable_classifications):
    permit_req = make_request()
    reject_req = make_request(object={
        "object_id": "r-1", "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-A",
        "release_caveat": ["PROJ-CAVEAT-X"], "data_origin": "SYNTHETIC", "schema_version": "9.9.9"})
    stale_req = make_request(object_timestamp_tick=0)  # RULE-ING-011 -> reject + RC-004
    block_req = make_request(inputs=[
        {"object_id": "in-a", "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-A", "release_caveat": ["PROJ-CAVEAT-X"]},
        {"object_id": "in-b", "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-B", "release_caveat": ["PROJ-CAVEAT-X"]}])
    quarantine_req = make_request(object={
        "object_id": "q-1", "classification_label": "PROJ-LEVEL-9", "domain_label": "DOMAIN-A",
        "release_caveat": ["PROJ-CAVEAT-X"], "data_origin": "SYNTHETIC", "schema_version": "0.2.0"})

    cases = [("permit", permit_req, "permit"), ("reject_schema", reject_req, "reject"),
             ("stale_rc004", stale_req, "reject"), ("block", block_req, "block"),
             ("quarantine", quarantine_req, "quarantine")]

    canon = {}
    reason_codes = {}
    for name, req, expected in cases:
        r1 = _ev(req, bundle, clock, resolvable_classifications)
        r2 = _ev(req, bundle, clock, resolvable_classifications)
        assert r1["disposition"] == expected, (name, r1["disposition"])
        assert record_canonical(r1) == record_canonical(r2)  # full tuple byte-identical
        canon[name] = record_canonical(r1)
        reason_codes[name] = r1["reason_codes"]

    # breadth: five distinct canonical records (incl. two reject cases with different RCs)
    assert len(set(canon.values())) == 5
    assert reason_codes["stale_rc004"] == ["RC-004"]
    assert "RC-004" not in reason_codes["reject_schema"]
