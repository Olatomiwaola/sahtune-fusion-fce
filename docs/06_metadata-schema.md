# 06 — Object Metadata Schema v0 (draft)

Owner: `data-model-engineer`. Canonical future home: `docs/05_data_model/`.

## Design rules

- 15 mandatory fields. Missing or malformed mandatory field fails closed at G2.
- Values in examples are SYNTHETIC.
- Classification and domain values use the project taxonomy (`07`), never real
  Government of Canada markings.
- Schema is versioned; `schema_version` travels with every object.
- `policy_binding_state` (field 15) is FCE-authority-set only: forced to
  `unvalidated` at G1 regardless of any ingested value, and never trusted from
  source input. [B3]

## Schema (15 fields)

| # | Field | Type | Constraint | Example (SYNTHETIC) |
|---|---|---|---|---|
| 1 | object_id | uuid | unique, required | 9f2c-...-SYN |
| 2 | schema_version | semver | required | 0.1.0 |
| 3 | data_origin | enum | required; SYNTHETIC or LIVE | SYNTHETIC |
| 4 | source_sensor_id | string | required; authenticated at G1 | SENSOR-EOIR-07 |
| 5 | modality | enum | required | eo_ir |
| 6 | acquisition_timestamp | RFC3339 + clock_source | required | 2026-01-01T00:00:00Z / gps |
| 7 | ingest_timestamp | RFC3339 | required | 2026-01-01T00:00:01Z |
| 8 | classification_label | enum (project taxonomy) | required | PROJ-LEVEL-2 |
| 9 | domain_label | enum (project taxonomy) | required | DOMAIN-A |
| 10 | release_caveat | list | required; may be empty list, never null | [PROJ-CAVEAT-X] |
| 11 | handling_instructions | string | required | route-domain-A-only |
| 12 | provenance_ref | uri/graph-node-id | required | prov://node/1234-SYN |
| 13 | parent_object_ids | list of uuid | required for derived/merged; else empty | [] |
| 14 | integrity_hash | sha-256 (design) | required | sha256:...(design) |
| 15 | policy_binding_state | enum | FCE-authority-set only; forced to unvalidated at G1; ingested value ignored (never trusted from source) | unvalidated |

Advisory (non-authoritative) attribute: `ai_confidence` (float [0,1]) may
accompany an object but is never a mandatory gate input and never the sole basis
for a decision.

## Signature note

A per-object signature is a design placeholder pending independent
implementation and assessment. No production cryptographic certification is
claimed.

## Label propagation

Merged or derived objects inherit the most-restrictive combination
(high-water mark) of parent labels unless an authorized downgrade transformation
with proof applies (`07`). `parent_object_ids` records all contributing parents.

## Fail-closed behaviour

At G2, an object missing any mandatory field, carrying a null where a value is
required, or failing integrity check is set to `policy_binding_state =
quarantined` and enqueued for review; it does not proceed.

## Requirement trace

FCE-REQ-MET-010, FCE-REQ-PRV-001, FCE-REQ-PRV-002, FCE-REQ-POL-011.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: 15-field mandatory shape; fail-closed on missing/malformed.
- Assumptions: field set covers all four baseline scenarios (`09`).
- Judgment: field choices and the advisory-confidence separation.
- Uncertainty: whether coalition routing needs extra caveat sub-fields.
