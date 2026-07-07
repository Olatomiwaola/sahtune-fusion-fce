"""FCE deterministic policy evaluator (M3 Sprint 6).

Python interpretation of docs/07 v1: default-deny PDP, closed reason-code
registry (RC-001..012), D3 disposition severity lattice, D4 decision-record
output contract, RULE-POL-001..006. OPA/Rego is a reference pattern only — no OPA,
no network. Clock is injected (H4); PIP auth flags are mechanism-simulated (H3/H4).
"""

from .actions import ACTIONS, SEVERITY_ORDER, most_restrictive
from .attributes import InjectedClock, PIPAttribute, all_attributes_valid
from .bundle import PolicyBundle, bundle_is_valid, load_bundle
from .evaluator import evaluate, record_canonical, record_hash
from .override import OverrideRequest, override_valid, time_limit_valid
from .reason_codes import REASON_CODES, ReasonCode, is_override_immutable

__all__ = [
    "ACTIONS",
    "SEVERITY_ORDER",
    "most_restrictive",
    "InjectedClock",
    "PIPAttribute",
    "all_attributes_valid",
    "PolicyBundle",
    "bundle_is_valid",
    "load_bundle",
    "evaluate",
    "record_canonical",
    "record_hash",
    "OverrideRequest",
    "override_valid",
    "time_limit_valid",
    "REASON_CODES",
    "ReasonCode",
    "is_override_immutable",
]
