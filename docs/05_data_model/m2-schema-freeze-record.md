# M2 Sprint 3 — Schema Freeze Record: Object Metadata Schema v0.2.0

Repo home (proposed, ENGINEERING JUDGMENT): `docs/05_data_model/m2-schema-freeze-record.md`.
Owner: `data-model-engineer`. Frozen against `docs/06_metadata-schema.md` v0.2.0 at repo
HEAD 5dd2a10, 2026-07-03. Decision records FCE-DR-SCH-001 and FCE-DR-SCH-002 authored
and ratified this sprint (`docs/12_decision_records/`).

## Freeze statement

The Sahtune Fusion Compliance Engine (FCE) 15-field object metadata schema is FROZEN at
v0.2.0. Changes now require: a new schema version, a migration rule, a decision record,
and envelope-version-gate handling (GDR-006). The five audit-side fields excluded by
FCE-DR-SCH-001 shall not be re-added without a new decision record.

## Field-by-field review (all 15 fields, full text)

| # | Field | Constraint as frozen | Review result |
|---|---|---|---|
| 1 | object_id | uuid; unique; required | PASS. UNCERTAINTY flagged: uniqueness scope (global vs per-run/per-mission) is not defined in `docs/06`; duplicate-ID handling is referred to red-team review this sprint and must be resolved before Sprint 4 test assertions are final. |
| 2 | schema_version | semver; required; must be a supported version (0.2.0), else rejected by the envelope-version gate before policy (GDR-006, `docs/16` §3) | PASS. |
| 3 | data_origin | enum; required; SYNTHETIC, SYNTHETIC-DERIVED, or PUBLIC-OPEN-SOURCE; LIVE rejected fail-closed at G1 at TRL 1-3 (FCE-DR-SCH-002); SYNTHETIC banner keys off {SYNTHETIC, SYNTHETIC-DERIVED}; PUBLIC-OPEN-SOURCE requires a resolvable source-manifest reference (GDR-001 hook) | PASS. |
| 4 | source_sensor_id | string; required; authenticated at G1 (authentication itself is G1/PIP scope, not envelope-validation scope) | PASS. |
| 5 | modality | enum; required | PASS. UNCERTAINTY: the modality enum value list lives with the scenario/taxonomy docs; the PoC uses the fixture-supplied list and fails closed on values outside it. |
| 6 | acquisition_timestamp | RFC3339 plus clock_source; required | PASS. UNCERTAINTY: clock_source value set is not enumerated in `docs/06` (example: gps); PoC validates presence and non-empty string only; trusted-time evaluation is H4 scope, not M2. |
| 7 | ingest_timestamp | RFC3339; required | PASS. Note: cross-field plausibility (acquisition_timestamp not after ingest_timestamp) is NOT a frozen v0.2.0 constraint; stale/replay timestamp defence is H4 scope. Recorded so its absence is a decision, not an oversight. |
| 8 | classification_label | enum (project taxonomy per `docs/07`); required; never real Government of Canada markings | PASS, with taxonomy enum values sourced from `docs/07` at Sprint 4 (docs/07 not supplied to this chat — gap flagged; PoC loads values as a fixture, fail-closed on unknown values). |
| 9 | domain_label | enum (project taxonomy per `docs/07`); required | PASS, same taxonomy-fixture handling as field 8. |
| 10 | release_caveat | list; required; may be an empty list, never null | PASS. Null-vs-empty distinction is an explicit validation rule and fixture case. |
| 11 | handling_instructions | string; required | PASS. |
| 12 | provenance_ref | uri/graph-node-id; required | PASS. Resolvability of the reference is provenance-graph scope (M4), not envelope-validation scope; PoC validates presence and format shape only. |
| 13 | parent_object_ids | list of uuid; required non-empty for derived/merged objects, else empty list; never null | PASS. Derived/merged detection at M2 is by object lifecycle type declaration in the fixture; enforcement that fused outputs carry true parentage is M5 (FCE-REQ-KRN-011, H1). |
| 14 | integrity_hash | sha-256 (design); required | PASS with material UNCERTAINTY: `docs/06` does not define the hash input domain (which bytes/fields are hashed, canonicalization). At Sprint 4 the validator checks format only and labels hash verification EXPLICITLY DEFERRED; defining the input domain is raised as an open item this sprint. G2's "failing integrity check" clause is untestable until then. |
| 15 | policy_binding_state | enum; FCE-authority-set only; forced to `unvalidated` at G1 regardless of ingested value; ingested value ignored, never trusted from source (B3, `docs/97`; GDR-007) | PASS. Detection of a source-supplied value is recorded in the disposition output (THR-MET-003 hook); formal audit emission is M4 scope. |

Advisory attribute `ai_confidence` (float [0,1]) confirmed non-mandatory, never a gate
input, never the sole basis for a decision (shared constraint 2).

## Lifecycle applicability (11 object lifecycle types)

Checklist rule: all 15 fields present in every object type or explicitly justified N/A.

| Lifecycle type | Envelope applicability |
|---|---|
| Raw sensor packet | Envelope assigned at the ingestion adapter before G1; carries all 15 fields from first FCE contact (ENGINEERING JUDGMENT: packets without an assignable envelope never enter the gate path — fail closed). |
| Normalized observation | All 15 fields; produced by the shared normalization function (GDR-016). |
| Tracklet | All 15 fields; parent_object_ids non-empty. |
| Fused track | All 15 fields; parent_object_ids non-empty; labels per high-water mark. |
| Compliance decision | N/A justified: carried as an audit-side record per FCE-DR-SCH-001; audit schema (M4) applies. |
| Transformed object | All 15 fields; parent_object_ids non-empty; transformation history on audit/provenance side per FCE-DR-SCH-001. |
| Downgraded object | All 15 fields; downgrade authority and transformation proof are policy/audit-side (docs/07, M3/M4). |
| Quarantined object | All 15 fields as received (possibly incomplete — quarantine exists precisely because validation failed); policy_binding_state = quarantined. |
| Audit event | N/A justified: 18-field audit schema (M4) applies, not the object envelope. |
| Operator override | N/A justified: audit-side record (M4); override preconditions per FCE-REQ-OPS-002 and B2. |
| Exported evidence package | N/A justified: export manifest per `docs/16`; contains enveloped objects and audit records but is not itself an enveloped object. |

## G2 fail-closed specification (objective 3)

Trace: FCE-REQ-MET-010 (acceptance criteria: rejected or quarantined at G2 with RC-001,
does not proceed to fusion). Reason code RC-001 is used as supplied by the RTM
acceptance criteria and the M2 block instructions; the full reason-code registry lives
in `docs/07_policy-decision-model.md`, which is not in this chat — registry consistency
check flagged for Claude Code at commit time.

| Trigger class | Where | Disposition |
|---|---|---|
| `data_origin = LIVE` or any unsupported `schema_version` | G1 / envelope-version gate, before policy | REJECT fail-closed; object never reaches G2 evaluation (FCE-DR-SCH-002, GDR-006). |
| Missing mandatory field | G2 | policy_binding_state set to `quarantined`; RC-001; enqueued for review; does not proceed. |
| Null where a value is required (including release_caveat = null, parent_object_ids = null) | G2 | Same quarantine path, RC-001. |
| Malformed value (type, enum, uuid, semver, RFC3339 format violations; unknown taxonomy value) | G2 | Same quarantine path, RC-001. |
| Integrity check failure | G2 | Same quarantine path, RC-001 — UNTESTABLE at Sprint 4 pending hash-input-domain definition (see field 14); deferral is explicit. |
| Source-supplied policy_binding_state | G1 | Not a rejection: value forced to `unvalidated`, detection recorded in disposition output (B3, GDR-007, THR-MET-003). |

Determinism: identical envelope input yields identical disposition and reason code
(supports FCE-REQ-POL-001 at the validation layer). Quarantine review queue mechanics
are out of M2 PoC scope (design note only).

## OPEN-02 taxonomy-mapping approach confirmation (objective 2 — approach only)

CONFIRMED APPROACH (leadership decision #2 still owns approval): policy labels use the
project taxonomy exclusively (PROJ-LEVEL-*, DOMAIN-*, PROJ-CAVEAT-* value families per
`docs/07`); a documentation-level mapping table in `docs/07` maps project-taxonomy
values to named external handling targets (e.g., Protected B) as reference-only external
targets (register item L4); no real Government of Canada marking is ever rendered,
applied, or procedurally imitated (FCE-REQ-POL-011); the mapping is descriptive at
TRL 1-3 and never an enforcement input. Nothing in the frozen schema constrains or is
constrained by the mapping choice — OPEN-02 resolution requires no schema rework
(consistent with the tracker's stated assumption).

## Requirement trace

FCE-REQ-MET-010, FCE-REQ-PRV-001, FCE-REQ-PRV-002, FCE-REQ-POL-011, FCE-REQ-ING-010,
FCE-REQ-POL-001 (validation-layer determinism). Verification methods: inspection (this
record), unit test (Sprint 4, LAP-UNIT-*), with property-based and red-team closure at
H9/M7.

## Facts / Assumptions / Judgment / Uncertainty

- FACT: field set, constraints, migration rule, and fail-closed text are as recorded in
  `docs/06` v0.2.0 at HEAD 5dd2a10; B3 substance per `docs/97`; RC-001 per RTM v0.2.
- ASSUMPTION: the 15-field set covers all four baseline scenarios (`docs/09`, carried
  forward from `docs/06`); docs/07 taxonomy enums are stable through M2.
- ENGINEERING JUDGMENT: lifecycle N/A justifications; raw-packet envelope-assignment
  point; freeze-record repo placement.
- UNCERTAINTY: object_id uniqueness scope; integrity_hash input domain; clock_source
  and modality enum value lists; coalition caveat sub-fields (carried from `docs/06`).
