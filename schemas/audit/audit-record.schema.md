# audit-record.schema (description-level) — M4 Sprint 8

Authority: `docs/08_audit-record-schema.md` v1 (FCE-DR-AUD-001, FCE-DR-SCH-004). This
file restates the shape for implementers; on any conflict, docs/08 governs — STOP and
bring the conflict to chat, do not resolve locally.

## 18 common fields (every record)

| # | Field | Shape |
|---|---|---|
| 1 | audit_event_id | uuid string, unique in chain |
| 2 | event_type | one of the 9 closed classes |
| 3 | event_timestamp | object `{ts: RFC3339 string, clock_source: non-empty string}` — exactly these two keys |
| 4 | actor_identity | non-empty string (fixture identity at TRL 1-3; authN is H3/H13) |
| 5 | source_object_ids | list of trusted/validated uuid strings; `[]` otherwise; cardinality per class |
| 6 | output_object_id | uuid string or null |
| 7 | policy_bundle_version | semver OR closed sentinel `{N/A-PRE-G4, N/A-EXPORT}`; legality per class |
| 8 | policy_rule_ids | list ⊆ docs/07 RULE-POL-001..006; may be empty |
| 9 | decision | non-empty string (raw pre-enforcement outcome) |
| 10 | reason_codes | list ⊆ RC-001..012 (closed registry) |
| 11 | enforcement_action | one of the 11 docs/07 actions |
| 12 | disposition | one of the 9 D3 lattice values |
| 13 | confidence | null at TRL 1-3 (writer refuses non-null) |
| 14 | record_content_hash | sha-256 (CANON-1) over the record minus fields 14, 16; field 15 INCLUDED |
| 15 | previous_record_hash | sha-256 chain link; genesis = 64 zeros |
| 16 | signature_placeholder | fixed placeholder string; no crypto claim (H6) |
| 17 | export_status | `{not-exported, exported}`; default `not-exported`; transitions are new records |
| 18 | review_status | `{unreviewed, reviewed}`; default `unreviewed`; transitions are new records |

Plus `event_detail`: closed per-class typed object; unknown fields refused fail-closed.

## Per-class event_detail (closed)

| Class | Required detail | Optional detail |
|---|---|---|
| ingestion | ingest_attempt_id | source_asserted_object_id, object_id_authenticated, detection_flags, validation_rule_refs |
| transformation | transformation_ref | — |
| policy-decision | pip_attributes_consumed, detection_flags, deterministic_evaluation | — |
| fusion-decision | — | merge_permit_ref, rc003_context |
| routing | destination_domain | — |
| quarantine | review_queue_ref | detection_flags (M5 Sprint 10; fusion mixed_bundle_versions / unrecorded_parentage) |
| downgrade | authority_ref, transformation_proof_ref | — |
| export | manifest_ref, record_range, manifest_sha256 | — |
| override | precondition_results, envelope_check, override_immutable_check | — |

## Requiredness matrix

Per `docs/08` (source_object_ids cardinality, output_object_id, bundle_version legality,
rule_ids). The `downgrade` row is now in the docs/08 matrix (FU-M4S8-1, 2026-07-06):
≥1 source, output required, semver, ≥1 rule, authority + transformation-proof detail.
