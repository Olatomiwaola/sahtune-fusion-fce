"""GDR-009 (policy-version) rejection test + GDR-010 (no-bypass) deferral.

GDR-009: a policy bundle whose version does not match the pin fails closed (reject),
never permit — docs/16 GDR-009 "Missing policy bundle version aborts held-out run".
The L1-testable mechanism is `bundle_is_valid` version-pinning; the held-out abort is
Layer 2 (docs/17 §3c "L2 open").

GDR-010 (no-bypass): docs/17 §3c maps it to integration tests TST-PRP-010 / TST-INT-001
("object without complete G1-G7 trace blocked"). There is no unit-level no-bypass
surface in src/fce_poc/; per build guardrail 7 it is NOT forced here and is deferred to
the Layer-2 harness — recorded as an explicit skip.

Trace: FCE-REQ-POL-020 (GDR-009), FCE-REQ-KRN-001 (GDR-010), docs/17 §3c/§6.
"""
import pytest

from fce_poc.policy import evaluate


def test_gdr009_bundle_version_mismatch_fails_closed_never_permit(make_request, bundle, clock, resolvable_classifications):
    # `bundle` is proj-baseline@0.2.0; pin a different version -> bundle-invalid -> reject.
    rec = evaluate(make_request(), bundle, clock, pinned_version="9.9.9",
                   resolvable_classifications=resolvable_classifications)
    assert rec["disposition"] == "reject"
    assert "bundle-invalid" in rec["rules_fired"]
    assert rec["disposition"] != "permit"


@pytest.mark.skip(reason="GDR-010 no-bypass has no unit surface in src/fce_poc/ "
                         "(integration/harness: object without complete G1-G7 trace). "
                         "Deferred to Layer 2 per docs/17 §3c (TST-PRP-010 / TST-INT-001) and build guardrail 7.")
def test_gdr010_no_bypass_deferred_to_layer2():
    pass
