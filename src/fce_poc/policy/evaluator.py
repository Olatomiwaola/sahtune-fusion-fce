"""Deterministic policy evaluator — a Python interpretation of a JSON bundle.

Reference model: docs/07 v1 (PDP/PEP, default-deny, RULE-POL-001..006, D3 lattice,
D4 output contract). OPA/Rego is a reference pattern only; this is a plain
deterministic Python evaluator over a JSON bundle fixture — no OPA, no network.

Flow: bundle validity -> G1 screen (RC-009/010/011 reject; RC-012 detection) ->
PIP authentication (RULE-POL-004, RC-008 fail-closed at G4) -> release rules
(RULE-POL-003 ambiguous, RULE-POL-002 merge, RULE-POL-001 permit) with default
deny -> deny-overrides lattice combination (RULE-POL-006) -> D4 decision record.

Determinism (FCE-REQ-POL-001): identical inputs yield an identical decision
record; `record_hash` gives a stable content hash for comparison.
"""

from __future__ import annotations

import hashlib
import json

from .actions import most_restrictive
from .attributes import InjectedClock, all_attributes_valid, failing_attribute_ids
from .bundle import PolicyBundle, bundle_is_valid, covers_merge

ALLOWED_DATA_ORIGINS = frozenset({"SYNTHETIC", "SYNTHETIC-DERIVED", "PUBLIC-OPEN-SOURCE"})

ENFORCEMENT = {
    "permit": "release",
    "restrict": "restrict-release",
    "block": "block-release",
    "segregate": "segregate-inputs",
    "quarantine": "quarantine-and-review",
    "reject": "reject-fail-closed",
    "require-human-review": "enqueue-review",
    "transform": "transform",
    "route-to-higher-domain": "route-to-higher-domain",
}


def _record(
    *,
    input_object_ids,
    pip_attributes,
    bundle_version,
    rules_fired,
    disposition,
    reason_codes,
    detection_flags,
    clock,
):
    return {
        "input_object_ids": sorted(input_object_ids),
        "pip_attributes_consumed": sorted(
            [a.attr_id, bool(a.authenticated)] for a in pip_attributes
        ),
        "bundle_version": bundle_version,
        "rules_fired": sorted(set(rules_fired)),
        "disposition": disposition,
        "reason_codes": sorted(set(reason_codes)),
        "enforcement_action": ENFORCEMENT[disposition],
        "detection_flags": sorted(set(detection_flags)),
        "evaluation_timestamp": clock.now,
        "deterministic_evaluation": True,
    }


def record_canonical(record: dict) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def record_hash(record: dict) -> str:
    return hashlib.sha256(record_canonical(record).encode("utf-8")).hexdigest()


def _stale(request, clock: InjectedClock) -> bool:
    tick = request.get("object_timestamp_tick")
    window = request.get("freshness_window")
    if tick is None or window is None:
        return False  # freshness not asserted in this request
    return (clock.now - tick) > window


def evaluate(
    request: dict,
    bundle: PolicyBundle,
    clock: InjectedClock,
    *,
    pinned_version: str,
    resolvable_classifications,
    supported_schema_versions=frozenset({"0.2.0"}),
) -> dict:
    obj = request["object"]
    pip = list(request.get("pip_attributes", []))
    obj_ids = [obj.get("object_id", "UNKNOWN")] + [
        o.get("object_id", "UNKNOWN") for o in request.get("inputs", [])
    ]

    # --- bundle validity (version pinning + signature placeholder) ---
    if not bundle_is_valid(bundle, pinned_version):
        return _record(
            input_object_ids=obj_ids, pip_attributes=pip, bundle_version=bundle.version,
            rules_fired=["bundle-invalid"], disposition="reject", reason_codes=[],
            detection_flags=[], clock=clock,
        )

    # --- G1 screen ---
    g1_reject_codes = []
    detection_flags = []
    if obj.get("schema_version") not in supported_schema_versions:
        g1_reject_codes.append("RC-009")
    if obj.get("data_origin") == "LIVE" or obj.get("data_origin") not in ALLOWED_DATA_ORIGINS:
        g1_reject_codes.append("RC-010")
    # RC-011 is MECHANISM-SIMULATED at TRL 1-3 (fixture flag; not real authN).
    if obj.get("source_authenticated", True) is False:
        g1_reject_codes.append("RC-011")
    # RC-012 detection (non-reject): source pre-marked policy_binding_state.
    binding = obj.get("policy_binding_state")
    if binding is not None and binding != "unvalidated":
        detection_flags.append("RC-012")

    if g1_reject_codes:
        return _record(
            input_object_ids=obj_ids, pip_attributes=pip, bundle_version=bundle.version,
            rules_fired=["G1"], disposition="reject", reason_codes=g1_reject_codes,
            detection_flags=detection_flags, clock=clock,
        )

    # --- PIP attribute authentication (RULE-POL-004, B1) at G4 ---
    if not all_attributes_valid(pip):
        return _record(
            input_object_ids=obj_ids, pip_attributes=pip, bundle_version=bundle.version,
            rules_fired=["RULE-POL-004"], disposition="block", reason_codes=["RC-008"],
            detection_flags=detection_flags + [f"pip-failed:{fid}" for fid in failing_attribute_ids(pip)],
            clock=clock,
        )

    # --- release rules ---
    rules_fired = []
    reason_codes = []
    dispositions = []

    # RULE-POL-003 — ambiguous / unresolvable classification.
    if obj.get("classification_label") not in set(resolvable_classifications):
        rules_fired.append("RULE-POL-003")
        reason_codes.append("RC-005")
        dispositions.append("quarantine")

    # RULE-POL-002 — cross-domain merge without covering permit.
    inputs = request.get("inputs")
    if inputs:
        if not covers_merge(bundle, inputs):
            rules_fired.append("RULE-POL-002")
            reason_codes.append("RC-003")
            dispositions.append("block")

    # RULE-POL-001 — same-domain permit.
    mission = request.get("mission")
    permit = bundle.permits.get(mission, {})
    permit_ok = (
        obj.get("classification_label") in set(permit.get("classifications", []))
        and obj.get("domain_label") == request.get("channel", {}).get("domain")
        and set(obj.get("release_caveat", [])) <= set(permit.get("caveats", []))
        and not _stale(request, clock)
    )
    if permit_ok:
        rules_fired.append("RULE-POL-001")
        dispositions.append("permit")

    # Default deny (base disposition is deny) when nothing else fired.
    if not dispositions:
        rules_fired.append("default-deny")
        dispositions.append("block")

    disposition = most_restrictive(dispositions)

    return _record(
        input_object_ids=obj_ids, pip_attributes=pip, bundle_version=bundle.version,
        rules_fired=rules_fired, disposition=disposition, reason_codes=reason_codes,
        detection_flags=detection_flags, clock=clock,
    )
