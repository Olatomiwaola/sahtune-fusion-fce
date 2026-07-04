# FCE-DR-SCH-001 — Envelope Minimalism: Audit Record as Replay Authority

Repo home: `docs/12_decision_records/fce-dr-sch-001.md`. Owner: `data-model-engineer`.
Authored in M2 Sprint 3 (2026-07-03, chat) from the recorded evidence in
`docs/06_metadata-schema.md` (Judgment section) and `docs/97_b1-b3-closure-review.md`;
ratified in the same block per the amended Sprint 3 objective 1 (leadership note,
governance record `docs/handoff/09_governance-note-gates.md`, commit 5dd2a10).
Status: RATIFIED (M2 Sprint 3).

## Context

The Sahtune Fusion Compliance Engine (FCE) object envelope (`docs/06_metadata-schema.md`)
must decide which per-object state travels on the object itself and which is carried by
the audit chain and provenance graph. Candidate envelope additions were: policy-bundle
version evaluated, enforcement disposition, transformation history, source adapter ID,
and mission ID. A fat envelope duplicates authoritative state; a minimal envelope keeps
one replay authority.

## Options

1. **Fat envelope** — carry policy-bundle version, enforcement disposition,
   transformation history, adapter ID, and mission ID on every object. Consequence:
   duplicated authoritative state; envelope and audit chain can disagree; tamper surface
   on the object itself grows; every schema change touches every object type.
2. **Minimal envelope (chosen)** — the 15 mandatory fields only; policy-bundle version,
   enforcement disposition, transformation history, adapter ID, and mission ID are
   carried on audit records (`docs/08`) and the provenance graph. The audit record is
   the single replay authority.

## Decision

Option 2. The object envelope is frozen at the 15 mandatory fields of
`docs/06_metadata-schema.md` v0.2.0. Policy-bundle version, enforcement disposition,
transformation history, source adapter ID, and mission ID are carried on audit records
and the provenance graph, not on the object envelope. These fields shall not be re-added
to the envelope without a new decision record.

## Consequences

- The M4 audit schema (18 fields, `docs/08`) is the mandatory carrier of policy-bundle
  version and disposition; replay (FCE-REQ-AUD-003) depends on audit records alone, which
  this decision makes structurally necessary.
- `policy_binding_state` (field 15) remains the only policy-adjacent envelope field, and
  it is FCE-authority-set only per B3 (`docs/97`): forced to `unvalidated` at G1,
  ingested value never trusted.
- The envelope-version gate (`docs/16` §3, GDR-006) governs envelope evolution; audit
  schema evolution is governed separately in M4.

## Trace

FCE-REQ-PRV-001, FCE-REQ-PRV-002, FCE-REQ-AUD-001, FCE-REQ-AUD-003, FCE-REQ-POL-011.
B3 (`docs/97`). GDR-006, GDR-007 (`docs/16`).

## Pointer correction

`docs/06_metadata-schema.md` currently cites this decision at
`evidence/laptop-poc/decision_register.md`, which does not exist as a standalone record
at HEAD 5dd2a10 (FACT per leadership note, 2026-07-03). This file is the canonical
record; `docs/06` must be amended to point here (REPO-UPDATE listed in the Sprint 3
handoff).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: the decision substance was already recorded in `docs/06` (Judgment section) and
  is restated here without semantic change.
- ENGINEERING JUDGMENT: minimal envelope with audit-side replay authority.
- UNCERTAINTY: none material; the M4 audit schema must confirm field carriage (tracked
  to Sprint 7).
