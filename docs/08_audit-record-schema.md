# 08 — Audit Record Schema v0 (draft)

Owner: `audit-forensics-engineer`. Skill: `fce-audit-record-design`.
W3C PROV cited for lineage concepts (reference alignment only).

## Design rules

- 18 mandatory fields (N/A must be explicit).
- 9 event classes covered.
- Append-only, hash-chained, tamper-evident.
- Decision sequence deterministically replayable from audit alone.
- Signature is a placeholder pending independent implementation and assessment;
  no production cryptographic certification is claimed.

## Schema (18 fields)

| # | Field | Type | Constraint | Example (SYNTHETIC) |
|---|---|---|---|---|
| 1 | audit_event_id | uuid | unique, required | ae-0001-SYN |
| 2 | event_type | enum (9 classes) | required | policy_decision |
| 3 | timestamp | RFC3339 + clock_source | required | 2026-01-01T00:00:02Z / gps |
| 4 | actor_identity | service/operator ID | authenticated | svc-pdp-01 |
| 5 | source_object_id | uuid | required | 9f2c-...-SYN |
| 6 | output_object_id | uuid | nullable with reason | null (deny) |
| 7 | policy_bundle_version | semver + hash | required | proj-baseline@0.1.0 / sha256(design) |
| 8 | policy_rule_ids | list | required | [RULE-POL-002] |
| 9 | decision | enum | required | block |
| 10 | reason_code | registry ref | required | RC-003 |
| 11 | enforcement_action | enum (11 actions) | required | segregate |
| 12 | disposition | enum | required | blocked |
| 13 | confidence | float [0,1] | advisory only | 0.82 |
| 14 | record_hash | sha-256 (design) | required | sha256:...(design) |
| 15 | previous_audit_hash | sha-256 (design) | chain link | sha256:...(design) |
| 16 | signature | PLACEHOLDER | pending independent impl + assessment | PLACEHOLDER |
| 17 | export_status | enum | required | not_exported |
| 18 | review_status | enum | required | pending |

## Event classes (9/9)

ingestion, transformation, policy decision, fusion decision, routing,
quarantine, downgrade, export, override. Every gate in `05` maps to at least one
class; every decision path emits at least one record.

## Chain and replay

Each record's `record_hash` includes `previous_audit_hash`, forming an
append-only chain. Any mutation or omission is detectable. Replay reconstructs
the disposition sequence deterministically from the chain plus the referenced
bundle version (FCE-REQ-AUD-003).

## Export formats

JSON, CSV, and PDF exports, each accompanied by an integrity manifest. Formats
for forensic review and accreditation-support review (labelled "support" only,
never "accredited" or "certified").

## Overflow behaviour

Backpressure, rotation, and fail-safe. Audit loss is a fail-closed trigger:
if a decision cannot be durably recorded, release halts at G7. Designed with the
architect and the Degraded-Mode Manager (ARCH-12).

## Requirement trace

FCE-REQ-AUD-001, FCE-REQ-AUD-002, FCE-REQ-AUD-003, FCE-REQ-EXP-001.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: 18 fields, 9 classes, append-only chain, replay determinism.
- Assumptions: JSON/CSV/PDF exports meet reviewer needs.
- Judgment: field typing and the overflow fail-closed policy.
- Uncertainty: signature scheme (placeholder until assessed).
