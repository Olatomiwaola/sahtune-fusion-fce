"""FCE-REQ-OPS-001 human-readable explanation surface (ARCH-13).

Render-only. A deterministic, side-effect-free view over the dict already
produced by ``fce_poc.policy.evaluator.evaluate()``. It introduces NO decision
logic and computes NO new policy result — it only re-presents fields the
evaluator has already decided. If a required field is absent from the decision
record it FAILS CLOSED (raises KeyError) rather than fabricating a value.

The partial-permit subset (docs/09 item 2.4) is carried by the evaluator in
``rules_fired`` and re-presented here; it is NOT recomputed and is NEVER read
from a policy-decision ``event_detail`` (RT-M6S11-01). This surface has no
``permitted_channels`` field.

Trace: FCE-REQ-OPS-001 (DES-04), docs/17 §3f, docs/09 item 2.4, FCE-REQ-KRN-002.
"""
from __future__ import annotations

from typing import Any, Mapping

# All required keys are produced by evaluate()'s record dict (M7 Sprint 14 recon).
_REQUIRED = (
    "disposition",
    "reason_codes",
    "rules_fired",
    "enforcement_action",
    "pip_attributes_consumed",
    "bundle_version",
    "deterministic_evaluation",
)


def explain(decision: Mapping[str, Any]) -> dict:
    """Return a human-readable explanation dict for a policy decision record.

    Pure function. Raises KeyError (fail closed) if the evaluator did not
    produce a required field — never invents one (no new semantics).
    """
    missing = [k for k in _REQUIRED if k not in decision]
    if missing:
        raise KeyError(
            "OPS-001 explanation cannot render; evaluator record missing "
            f"required field(s): {missing}. Fail closed (no fabricated fields)."
        )
    return {
        "disposition": decision["disposition"],
        "enforcement_action": decision["enforcement_action"],
        "reason_codes": list(decision["reason_codes"]),
        "rules_fired": list(decision["rules_fired"]),
        "pip_attributes_consumed": decision["pip_attributes_consumed"],
        "bundle_version": decision["bundle_version"],
        "deterministic_evaluation": decision["deterministic_evaluation"],
    }


def explain_text(decision: Mapping[str, Any]) -> str:
    """Deterministic single-block human-readable rendering of ``explain()``."""
    e = explain(decision)
    return "\n".join(
        [
            f"Disposition:         {e['disposition']}",
            f"Enforcement action:  {e['enforcement_action']}",
            f"Reason codes:        {', '.join(e['reason_codes']) or '(none)'}",
            f"Rules fired:         {', '.join(e['rules_fired']) or '(none)'}",
            f"PIP attributes:      {e['pip_attributes_consumed']}",
            f"Policy bundle:       {e['bundle_version']}",
            f"Deterministic eval:  {e['deterministic_evaluation']}",
        ]
    )
