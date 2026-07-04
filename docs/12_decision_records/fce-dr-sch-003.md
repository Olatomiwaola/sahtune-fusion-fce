# FCE-DR-SCH-003 — Unknown Envelope Fields: Reject Fail-Closed at G2

Repo home: `docs/12_decision_records/fce-dr-sch-003.md`. Owner: `architect`
(disposition authority; data-model-engineer implements). Authored and ratified in
M2 Sprint 4 (2026-07-04, chat) on the basis commit ca75497. Status: RATIFIED
(M2 Sprint 4).

## Context

Schema v0.2.0 (`docs/06`, FCE-DR-SCH-001/002) freezes the 15 mandatory fields but does
not define how an envelope carrying **unknown or extra** fields is handled. The M2
Sprint 3 red-team review raised this as RT-M2S3-03 and the freeze package flagged it as
an explicit gap (`docs/05_data_model/m2-validation-rules.md`: "unknown/extra envelope
fields — accept-and-ignore vs reject is not defined … default fail-closed"); it was
tracked as follow-up FU-M2S3-2 (owner architect, before Sprint 4-final tests). The
Sprint 4 PoC implemented an interim fail-closed behaviour pending this decision. This
record resolves the disposition.

## Options

1. **Reject fail-closed at G2 (chosen)** — any envelope with a field outside the frozen
   known-field set is not accepted; it fails closed at G2 with reason code RC-001 and
   does not proceed to fusion. Consequence: no unmodelled field can carry data past the
   gate; a smuggling / version-drift channel is closed; strictness may reject
   forward-compatible producers until the schema version is bumped (acceptable at
   TRL 1-3, where the FCE owns both sides).
2. **Strip-and-record** — drop unknown fields, record their names in the disposition /
   audit, and continue evaluating the known fields. Consequence: more permissive and
   forward-compatible, but it silently discards data the producer thought meaningful and
   depends on the M4 audit writer (which does not exist at M2) to make the strip
   auditable; at TRL 1-3 that audit guarantee cannot yet be met.

## Decision

Option 1. **Unknown/extra envelope fields cause the object to be rejected fail-closed at
G2 with reason code RC-001.** At the M2 validator this is realized through the G2
fail-closed disposition (quarantine with RC-001, per the freeze-record G2 specification,
`docs/05_data_model/m2-schema-freeze-record.md`); the object does not proceed. The
unknown-field trigger is recorded in the disposition `failed_rules` as `UNKNOWN-FIELD`.
This supersedes the interim behaviour noted in the validation-rule list and closes
FU-M2S3-2.

## Consequences

- The Sprint 4 PoC's unknown-field handling is now a ratified requirement, not an interim
  choice; test `LAP-UNIT-010` (`docs/16`) verifies it and references this record.
- Resolves RT-M2S3-03. RULE-VAL-* keep their existing IDs; unknown-field rejection is
  carried as the `UNKNOWN-FIELD` disposition marker rather than a new RULE-VAL number
  (the validation-rule list is not renumbered).
- **Revisit trigger:** this decision is to be revisited at the **first external ingest
  adapter** (a producer the FCE does not control) **or at TRL 4-5**, whichever comes
  first, when forward-compatibility and a real audited strip-and-record path may become
  preferable. Reintroducing strip-and-record requires a new decision record and a
  working audit writer (M4).

## Trace

FCE-REQ-MET-010. RT-M2S3-03 (`docs/06_security/red_team_findings/RT-M2S3.md`); FU-M2S3-2
(`docs/handoff/05_open-items-and-decision-register.md`). Freeze record G2 specification
(`docs/05_data_model/m2-schema-freeze-record.md`). Verified by LAP-UNIT-010 (`docs/16`,
`tests/test_validator.py`).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: schema v0.2.0 does not define unknown-field handling; the Sprint 4 PoC already
  fails closed on unknown fields and 44/44 tests pass (EVD-M2).
- ENGINEERING JUDGMENT: at TRL 1-3, where the FCE owns both producer and consumer,
  reject-fail-closed is safer than a strip that cannot yet be audited.
- UNCERTAINTY: the strip-and-record trade-off becomes live at the first external adapter
  / TRL 4-5 (revisit trigger above).
