# FCE-DR-SCH-002 — data_origin Provenance Classes and LIVE Removal at TRL 1-3

Repo home: `docs/12_decision_records/fce-dr-sch-002.md`. Owner: `data-model-engineer`.
Authored in M2 Sprint 3 (2026-07-03, chat) from the recorded evidence in
`docs/06_metadata-schema.md` (Design rules; Schema version history) and
`docs/handoff/05_open-items-and-decision-register.md` (L1 resolution); ratified in the
same block per the amended Sprint 3 objective 1 (governance record at commit 5dd2a10).
Status: RATIFIED (M2 Sprint 3).

## Context

Schema v0.1.0 defined `data_origin` as enum {SYNTHETIC, LIVE}. Open item L1 required a
provenance-class model consistent with the shared constraint that all non-live data is
labelled by provenance class and that LIVE data is out of scope at TRL 1-3. The laptop
PoC architecture (`docs/16`) additionally introduces PUBLIC-OPEN-SOURCE fixtures
governed by a source manifest (GDR-001).

## Options

1. **Keep LIVE in the enum, gate it by policy** — LIVE remains representable and a
   policy rule denies it. Consequence: a representable-but-forbidden state; policy
   misconfiguration could admit LIVE data at TRL 1-3.
2. **Remove LIVE from the enum at TRL 1-3 (chosen)** — LIVE is structurally
   unrepresentable in v0.2.0; any object presenting `data_origin = LIVE` is rejected
   fail-closed at G1 by the envelope-version/enum check.

## Decision

Option 2. `data_origin` enum at v0.2.0 is {SYNTHETIC, SYNTHETIC-DERIVED,
PUBLIC-OPEN-SOURCE}. LIVE is removed at TRL 1-3 and rejected fail-closed at G1. The
visible SYNTHETIC banner keys off `data_origin` in {SYNTHETIC, SYNTHETIC-DERIVED}.
`PUBLIC-OPEN-SOURCE` objects require a resolvable source-manifest reference per
`docs/16` (GDR-001 hook).

## Consequences

- Migration rule (`docs/06` version history): v0.1.0 objects with
  `data_origin = SYNTHETIC` are accepted unchanged; v0.1.0 objects with
  `data_origin = LIVE` are rejected by the envelope-version gate (`docs/16` §3). No
  other field changes. Change is additive/versioned; no prior sealed evidence exists.
- Reintroducing LIVE requires a new schema version, a new decision record, and is out of
  scope until beyond TRL 1-3.
- Resolves open item L1 (register `05`, marked RESOLVED 2026-07-03).

## Trace

Shared constraint 5 (`_SHARED_CONSTRAINTS.md`). L1 (`docs/handoff/05`). FCE-REQ-MET-010,
FCE-REQ-ING-010. GDR-001, GDR-006 (`docs/16`).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: the decision substance was already recorded in `docs/06` v0.2.0 and register L1
  and is restated here without semantic change.
- ENGINEERING JUDGMENT: structural unrepresentability over policy-gated representability
  for LIVE at TRL 1-3.
- UNCERTAINTY: none material at TRL 1-3.
