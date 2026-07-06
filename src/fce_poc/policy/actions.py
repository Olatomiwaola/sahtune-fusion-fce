"""Policy actions and the D3 disposition severity lattice.

Verbatim from docs/07_policy-decision-model.md:
  - "Policy actions (all 11 representable)"
  - "Disposition severity lattice [D3, FCE-DR-POL-001 — RATIFIED 2026-07-04]"

The lattice is a TOTAL order over the nine combinable dispositions, most -> least
restrictive. `downgrade` and `override` are authority-gated actions and are NEVER
products of lattice combination (RC-006 / RC-007 only), so they are not in the
severity order.
"""

from __future__ import annotations

# 11 policy actions (docs/07 "Policy actions (all 11 representable)").
ACTIONS: tuple[str, ...] = (
    "permit",
    "restrict",
    "block",
    "segregate",
    "quarantine",
    "reject",
    "transform",
    "route-to-higher-domain",
    "require-human-review",
    "downgrade",
    "override",
)

# D3 total order, most -> least restrictive (docs/07 lattice section).
SEVERITY_ORDER: tuple[str, ...] = (
    "reject",
    "quarantine",
    "block",
    "segregate",
    "require-human-review",
    "restrict",
    "transform",
    "route-to-higher-domain",
    "permit",
)

# Authority-gated actions excluded from lattice combination (D3).
AUTHORITY_GATED: frozenset[str] = frozenset({"downgrade", "override"})

_RANK = {disposition: index for index, disposition in enumerate(SEVERITY_ORDER)}


def most_restrictive(dispositions):
    """Return the most restrictive disposition per the D3 total order (RULE-POL-006).

    Deterministic: the order is total, so there is never a tie.
    """
    items = list(dispositions)
    if not items:
        raise ValueError("most_restrictive() requires at least one disposition")
    for d in items:
        if d not in _RANK:
            raise ValueError(f"{d!r} is not a lattice disposition (authority-gated or unknown)")
    return min(items, key=lambda d: _RANK[d])
