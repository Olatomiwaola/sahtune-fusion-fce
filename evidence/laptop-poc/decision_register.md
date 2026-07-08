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

**Reconciliation 2026-07-07 (M6 open, lead concurrence in-chat; append-only — original rows above retained unmodified):**

- FCE-DR-SCH-001 / -002: RATIFIED M2 Sprint 3 per the standalone records in
  `docs/12_decision_records/`; the "ratify at M2 Sprint 1" rows above are
  superseded by those files, which are authoritative.
- FCE-DR-POC-001: PARTIALLY RESOLVED — source families fixed by leadership
  decision #6 (2026-07-07): USGS (OSD-01) + Sentinel-2 STAC (OSD-04). Query
  windows/AOI finalize in the trim manifest at Sprint 11/12, recorded before
  download.
- FCE-DR-POC-002: RESOLVED — envelope v0.2.0 per FCE-DR-SCH-002.
- FCE-DR-POC-003: OPEN — split decided (70/30 stratified, keyed on stable source
  record IDs, lead concurrence 2026-07-07); seed to be minted blind and committed
  at Sprint 11 close, before any data download. The Sprint 11 mint deliberately
  supersedes this row's "set at M6 Sprint 2" (= Sprint 12) target: early, not
  conflicting.
- FCE-DR-POC-004: OPEN — milestone corrected: the original "set at M3 Sprint 2"
  target is stale; the pinned held-out bundle version is recorded in the Sprint 12
  seal record alongside fixture hashes (lead concurrence 2026-07-07).
- FCE-DR-POC-005: OPEN, unchanged — register target "ratify before M7 Sprint 2"
  stands; pass/fail candidate is docs/16 criteria 1–10; ratify at M7 Sprint 13
  (V&V plan).
- FCE-DR-POC-006: RESOLUTION PROPOSED (due before Sprint 12 per its own register
  target) — evidence write rules = working convention rule 9 (RATIFIED
  2026-07-07) + docs/16 §3 prior-artifact seal; sealed-artifact locations =
  docs/16 fixture-and-evidence layout (`data/fixtures/heldout/`,
  `evidence/laptop-poc/`). Ratify at Sprint 11 close, before any fixture build.
- FCE-DR-POC-007: RESOLVED — leadership decision #5 (2026-07-03): Python 3.12.13
  + pinned pytest 9.1.0, stdlib-first, installs by approval only.
- Note: `docs/12_decision_records/fce-dr-sch-001.md` states this register "does
  not exist as a standalone record at HEAD 5dd2a10"; the register file did exist —
  the defensible reading is that no standalone DR *file* existed at that HEAD.
  Clarified here; the ratified DR file itself is not edited.

**Sprint 11 close 2026-07-07 (append-only; lead concurrence in-chat):**

- FCE-DR-POC-003: RESOLVED — calibration/held-out split: 70/30 stratified per
  source family and modality; deterministic key = sha-256 over (stable source
  record ID, seed); seed = 12918724377571503927, minted blind 2026-07-07 at Sprint 11 close,
  before any data download (network unapproved until Sprint 12). Held-out set
  seals at Sprint 12 close per FCE-DR-POC-004/-006.
- FCE-DR-POC-006: RATIFIED — evidence write rules = working-conventions rule 9
  (RATIFIED 2026-07-07) + docs/16 §3 prior-artifact seal; sealed-artifact
  locations = docs/16 fixture-and-evidence layout (`data/fixtures/heldout/`,
  `evidence/laptop-poc/`). Sprint 12 seal record names fixture hashes AND the
  pinned policy-bundle version (FCE-DR-POC-004 pairing, lead concurrence
  2026-07-07).
- Transform-action fixture gap: ACCEPTED at M6 (lead concurrence 2026-07-07) —
  representability demonstrated in docs/07; fixture-level exercise deferred to
  Sprint 13 / M7 V&V planning.


**Sprint 12 close 2026-07-08 (append-only; lead concurrence in-chat):**

- FCE-DR-POC-004: RESOLVED — pinned bundle for held-out evaluation =
  proj-baseline@0.2.0, recorded in the Sprint 12 seal record
  (evidence/laptop-poc/sprint12_seal.md) alongside the held-out fixture
  hashes and aggregate digest. Re-pin protocol: explicit, pre-evaluation,
  recorded; no silent evaluation under a different bundle; no post-seal
  mutation.
- FCE-DR-POC-001: RESOLVED (from PARTIALLY RESOLVED) — query windows/AOI
  finalized and recorded in the source manifest before download; the
  Sentinel-2 corrective slice-alignment re-query is recorded with verbatim
  supersession rationale (data/fixtures/source_manifest.json).

**Sprint 13 open 2026-07-08 (append-only; lead ratification in-chat):**

- FCE-DR-POC-005: RATIFIED — pass/fail validation criteria = docs/16 Pass/Fail criteria 1–10, adopted verbatim. Binding readings recorded at ratification: (1) criterion 6 ("held-out validation runs without changing the policy bundle or thresholds") is satisfied only under the seal re-pin protocol — any re-pin is explicit, pre-held-out (pre-evaluation), recorded, and names a new sealed bundle reference; the sealed proj-baseline@0.2.0 is never mutated in place. (2) Failure of any of criteria 1–10 on the held-out run forces the outcome label "engineering progress; PoC validation gate not passed", never "PoC validated". Ratified at M7 Sprint 13 (V&V plan docs/17 §1); register target "ratify before M7 Sprint 2" met. Trace: docs/16 §Pass/Fail, docs/17_vv-plan.md §1.


**Sprint 13 close 2026-07-08 (append-only; lead decision in-chat) — Scenario 4 covers() resolution:**

- Scenario 4 (UAV) fused-track positive-merge parent labels FIXED before Sprint 14 build (recorded pre-build; no post-hoc tuning): eo_ir observation = (PROJ-LEVEL-1, DOMAIN-A, [PROJ-CAVEAT-X]); uas_telemetry observation = (PROJ-LEVEL-2, DOMAIN-A, [PROJ-CAVEAT-X]). Parent tuple-multiset [(PROJ-LEVEL-1, DOMAIN-A, [PROJ-CAVEAT-X]), (PROJ-LEVEL-2, DOMAIN-A, [PROJ-CAVEAT-X])] is covered EXACTLY by MP-V1-SAME-DOMAIN in the sealed proj-baseline@0.2.0 (exact-multiset covers() = True); fused track carries the high-water-mark label (PROJ-LEVEL-2, DOMAIN-A, [PROJ-CAVEAT-X]). Result: NO re-pin required; the sealed bundle (sha 6a830b24…c53502; held-out aggregate 059829…63e) is used unchanged for the held-out run. Negative case 4.3 (override vs an uncovered cross-domain merge) remains intentionally uncovered → RC-003 block, override-immune (B2). Finding of record: no S4 calibration envelopes exist on disk; S4 observation fixtures are materialized in the Sprint 14 build to the labels fixed here (train/serve identity, GDR-016). Trace: docs/09 Scenario 4, docs/18 §4, docs/17_vv-plan.md §4, FCE-DR-POC-004 (pin-before-evaluation), seal record re-pin protocol.
