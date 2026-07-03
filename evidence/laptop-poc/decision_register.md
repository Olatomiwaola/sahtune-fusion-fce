# Laptop PoC Decision Register

Pre-code decisions per `docs/16_laptop-poc-validation-architecture.md` §1–§2.
Entries are append-only; superseding a decision requires a new entry, never an
edit. FCE-DR-POC-001…007 remain open until approved before M2 Sprint 2.

| DR ID | Decision | Rationale | Status | Trace |
|---|---|---|---|---|
| FCE-DR-SCH-001 | The object envelope (`06`, 15 fields) does not carry policy-bundle version, enforcement disposition, transformation history, source adapter ID, or mission ID. Policy-bundle version and disposition are carried on every audit record (`08`, which is the replay authority per FCE-REQ-AUD-003); transformation history and lineage are carried in the provenance graph via `provenance_ref` and `parent_object_ids`. | Keeps the envelope minimal for laptop-scale validation; avoids duplicating replay-critical fields in two places, which would create a consistency attack surface; audit record is the single replay source. Resolves the divergence between `.claude/agents/data-model-engineer.md` and `docs/06`. | Decided 2026-07-03 (architecture accountability review); ratify at M2 Sprint 1 | FCE-REQ-AUD-003, FCE-REQ-PRV-001/002, FCE-REQ-MET-010 |
| FCE-DR-SCH-002 | `data_origin` enum is {SYNTHETIC, SYNTHETIC-DERIVED, PUBLIC-OPEN-SOURCE} at schema v0.2.0; LIVE is removed at TRL 1-3 and rejected fail-closed at G1. | The v0.1.0 enum {SYNTHETIC, LIVE} could not represent the approved open-source-derived laptop fixtures required by `09`/`12`/`14`/`15`/`16` and GATE-C; LIVE removal resolves open item L1. | Decided 2026-07-03; ratify at M2 Sprint 1 | FCE-REQ-MET-010, FCE-REQ-POL-011, GDR-001/002 |
| FCE-DR-POC-001 | Approved open-source data sources and query windows | Prevents cherry-picking sources after results are known | OPEN — leadership decision #6 (OPEN-04) | `16` §2 |
| FCE-DR-POC-002 | Schema/envelope version used by the PoC | Prevents silent contract drift. Candidate: v0.2.0 per FCE-DR-SCH-002 | OPEN — confirm at M2 Sprint 1 | `06` |
| FCE-DR-POC-003 | Calibration vs held-out fixture split and random seed | Prevents evaluation contamination | OPEN — set at M6 Sprint 2 | `16` §2 |
| FCE-DR-POC-004 | Fixed policy bundle version for held-out evaluation | Prevents post-hoc rule tuning | OPEN — set at M3 Sprint 2 | `16` §2 |
| FCE-DR-POC-005 | Pass/fail validation criteria | Prevents moving the goalpost. Candidate: `16` §Pass/Fail criteria 1–10 | OPEN — ratify before M7 Sprint 2 | `16` |
| FCE-DR-POC-006 | Evidence write rules and sealed-artifact locations | Prevents accidental overwrite of prior evidence. Candidate: `16` §Fixture And Evidence Layout | OPEN — ratify before M6 Sprint 2 | `16` §3 |
| FCE-DR-POC-007 | Dependency boundary: standard library first, external installs only by approval | Keeps laptop proof repeatable | OPEN — confirm before M2 Sprint 2 | `_SHARED_CONSTRAINTS` #6 |

Facts: register structure and DR-POC-001…007 definitions are drawn verbatim
from `16` §2. Judgment: FCE-DR-SCH-001/002 dispositions. Uncertainty: leadership
ratification pending for all entries marked OPEN or "ratify".
