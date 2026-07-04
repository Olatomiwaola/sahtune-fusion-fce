# FCE-DR-POL-001 — Disposition Severity Lattice (Deny-Overrides Total Order)

Repo home: `docs/12_decision_records/fce-dr-pol-001.md`. Owner: `policy-engineer`
(authored); `architect` ratified. Authored M3 Sprint 5 (2026-07-04, chat)
on basis commit 7d981fd. Status: **RATIFIED 2026-07-04**.
Architect review executed in-chat (M3 Sprint 5 architect block); project lead
concurrence 2026-07-04. Any change to the lattice ordering requires a successor
decision record.

## Context

The policy model (`docs/07`) specifies "deny-overrides by default" for conflict
resolution, but that phrase is underspecified over the 11 policy actions: when several
rules fire with different dispositions, which one wins, and are ties possible? Without a
defined order the combination outcome is nondeterministic at the disposition level,
which FCE-REQ-POL-001 forbids and which would corrupt audit/replay fidelity.

## Options

1. **Total severity order (chosen)** — a single total order over dispositions; the
   combined outcome is the most restrictive fired disposition. Ties are structurally
   impossible.
2. **Partial order with tie → fail-closed** — rank only some dispositions and resolve
   ties by failing closed. Rejected: leaves a nondeterministic surface (which of two
   incomparable outcomes is "the" disposition is unresolved except by the tie rule,
   which is itself a disposition change).
3. **Single binary deny** — collapse everything to permit/deny. Rejected: loses
   disposition fidelity (segregate vs quarantine vs block vs review) that audit, replay,
   and operator workflows depend on.

## Decision

Option 1. The disposition severity lattice is the **total order**, most → least
restrictive:

reject > quarantine > block > segregate > require-human-review > restrict >
transform > route-to-higher-domain > permit.

When multiple rules fire, the final disposition is the most restrictive among the fired
outcomes. `downgrade` and `override` are **authority-gated actions** and are never
products of lattice combination — they arise only from explicit authorized paths
(RC-006 authorized downgrade with proof; RC-007 authenticated envelope-bounded
override). Residual ambiguity (an unresolvable condition or attribute) is **not** a tie:
it quarantines with RC-005 (FCE-REQ-POL-012). Middle-entry ordering is ENGINEERING
JUDGMENT.

## Consequences

- Conflict combination in `docs/07` (RULE-POL-006) is deterministic and tie-free
  (FCE-REQ-POL-001); the "deny-overrides" phrase now has a precise meaning.
- The final disposition is a well-defined function of the fired rule set — a prerequisite
  for the decision-record output contract (D4) and M4 audit replay.
- Because the order is total, no "tie → fail-closed" escape hatch is needed; the only
  fail-closed-on-ambiguity path is the RC-005 quarantine for unresolvable inputs.

## Trace

FCE-REQ-POL-001 (deterministic evaluation), FCE-REQ-POL-012 (ambiguity → review).
`docs/07` Disposition severity lattice section (D3); RULE-POL-006. Verified by
TST-POL-006a/b/c (Sprint 6 evaluator).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: `docs/07` specifies deny-overrides and default-deny; the 11 actions are fixed.
- ENGINEERING JUDGMENT: the middle-entry ordering (block > segregate >
  require-human-review > restrict > transform > route-to-higher-domain) is a judgment
  call; the endpoints (reject most restrictive, permit least) are not.
- UNCERTAINTY: the endpoints are settled; the middle ordering, now ratified, may still be
  revisited if a concrete rule set demonstrates a counter-intuitive combination — any such
  change requires a successor decision record.
