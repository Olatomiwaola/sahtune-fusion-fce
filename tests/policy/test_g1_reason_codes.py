"""G1 reason-code dispositions RC-009/010/011/012.

MECHANISM-SIMULATED (RT-M3S5-03, H3/H4): every RC-011 source-authentication case
here is driven by a fixture flag (`source_authenticated`), NOT demonstrated
authentication. EVD-M3 must not claim authentication demonstrated.
"""

from __future__ import annotations

from fce_poc.policy import evaluate

MECHANISM_SIMULATED = "mechanism-simulated"  # label for ALL RC-011 cases (RT-M3S5-03)


def _ev(request, bundle, clock, resolvable):
    return evaluate(
        request, bundle, clock,
        pinned_version="0.2.0", resolvable_classifications=resolvable,
    )


def test_rc009_unsupported_schema_version_rejected(make_request, bundle, clock, resolvable_classifications):
    obj = {"object_id": "g1-009", "schema_version": "0.1.0", "data_origin": "SYNTHETIC",
           "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-A"}
    rec = _ev(make_request(object=obj), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "reject"
    assert "RC-009" in rec["reason_codes"]


def test_rc010_live_data_origin_rejected(make_request, bundle, clock, resolvable_classifications):
    obj = {"object_id": "g1-010", "schema_version": "0.2.0", "data_origin": "LIVE",
           "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-A"}
    rec = _ev(make_request(object=obj), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "reject"
    assert "RC-010" in rec["reason_codes"]


def test_rc011_source_authentication_failure_rejected_mechanism_simulated(make_request, bundle, clock, resolvable_classifications):
    # MECHANISM-SIMULATED: source_authenticated is a fixture flag, not real authN.
    obj = {"object_id": "g1-011", "schema_version": "0.2.0", "data_origin": "SYNTHETIC",
           "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-A",
           "source_authenticated": False}
    rec = _ev(make_request(object=obj), bundle, clock, resolvable_classifications)
    assert rec["disposition"] == "reject", MECHANISM_SIMULATED
    assert "RC-011" in rec["reason_codes"], MECHANISM_SIMULATED


def test_rc012_source_supplied_binding_state_detected_not_rejected(make_request, bundle, clock, resolvable_classifications):
    obj = {"object_id": "g1-012", "schema_version": "0.2.0", "data_origin": "SYNTHETIC",
           "classification_label": "PROJ-LEVEL-2", "domain_label": "DOMAIN-A",
           "release_caveat": ["PROJ-CAVEAT-X"], "policy_binding_state": "validated"}
    rec = _ev(make_request(object=obj), bundle, clock, resolvable_classifications)
    # RC-012 is detection, not reject: object proceeds and permits.
    assert "RC-012" in rec["detection_flags"]
    assert rec["disposition"] != "reject"
    assert rec["disposition"] == "permit"
