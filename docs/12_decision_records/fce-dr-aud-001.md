# FCE-DR-AUD-001 — Audit record structure: field-5 pluralization, event_detail extension, immutable status transitions, three-level replay

**Status: RATIFIED 2026-07-06** — architect-role review (recommend-ratify),
red-team review (RT-M4S7, non-blocking, claim audit clean), and project-lead
concurrence 2026-07-06 all recorded below per the DR ratification pattern.
Date: 2026-07-06. Owner: audit-forensics-engineer. Block: M4 Sprint 7.

## Context

The audit-forensics role spec fixes an 18-field record with singular "source
object ID". The docs/07 D4 output contract (the policy-decision event's field
source) carries three fields with no 18-field home (pip_attributes_consumed,
detection_flags, deterministic_evaluation); fusion-decision events require ≥2
parents; export/review status changes must not mutate an append-only chain;
G1 rejects can occur before a trusted object identity exists.

## Decision

D1. source_object_ids (field 5) is a list of uuid; the per-class requiredness
matrix (docs/08) governs cardinality. Field 5 contains ONLY trusted/validated
object IDs and is [] otherwise.

D2. The 18 common fields are extended by one closed, per-event-class typed
event_detail object (sub-schemas in docs/08, part of schema v1). Unknown
detail fields are refused fail-closed (mirrors FCE-DR-SCH-003). G1 rejection
identity: event_detail.ingest_attempt_id (uuid, writer-generated) is
MANDATORY for every ingestion-class event; untrusted source-asserted IDs
appear only as optional event_detail.source_asserted_object_id with
event_detail.object_id_authenticated=false — never in lineage/replay fields.
The export-class detail includes the manifest's own sha-256 (architect
addition) so the chain binds manifest content.

D3. export_status / review_status transitions are emitted as NEW audit
records referencing the original audit_event_id; no record is ever mutated;
current status is a derived view.

D4. Replay is split into R1 chain integrity, R2 decision-sequence
reconstruction from audit records alone (the FCE-REQ-AUD-003 demonstration),
and optional R3 re-evaluation cross-check labelled as requiring inputs beyond
the audit file. R2 lineage resolution never reads detail-asserted IDs.

Plus structural corrections: policy_bundle_version type is semver | closed
sentinel enum {N/A-PRE-G4, N/A-EXPORT} with per-class legality;
event_timestamp is a structured object {ts: RFC3339, clock_source:
non-empty string}.

## Rejected alternatives

(a) Overloading reason_codes/decision to carry D4 remainders — breaks replay
semantics and the closed registry. (b) 21 flat fields — contradicts the role
spec's 18-field core and couples every class to policy-decision internals.
(c) Mutating status fields in place — violates append-only tamper evidence
(FCE-REQ-AUD-002). (d) Placing source-asserted IDs in field 5 for G1 rejects
— pollutes lineage/replay with untrusted identity (rejected by project-lead
clarification 2026-07-06).

## Consequences

Schema v1 = 18 common fields + closed per-class detail; the writer refuses
matrix violations, illegal sentinels, unknown detail fields, and malformed
timestamps fail-closed; chain semantics unaffected (detail is inside the
hashed content); H6 signature, H7 concurrency, H4 trusted time remain open
and unclaimed.

## Ratification record

- Architect review (M4 Sprint 7, 2026-07-06): checklist pass; boundary
  classification — operates within established trust boundaries (B3,
  GDR-006/007), conditional on red-team boundary check; manifest-sha-256
  addition to export detail; RECOMMEND-RATIFY.
- Red-team review (RT-M4S7, 2026-07-06): 5 findings (2 Medium, 3 Low), none
  blocking; claim audit clean; no boundary concern — no security-assurance
  block demanded.
- Project-lead concurrence: 2026-07-06, with required contents enumerated
  (G1 identity rules, closed event_detail, immutable status transitions,
  manifest sha-256, R1/R2/R3 split) — all present above.

## Trace

FCE-REQ-AUD-001/-002/-003, FCE-REQ-EXP-001, FCE-REQ-OPS-002, FCE-REQ-SEC-002,
FCE-REQ-KRN-011. H14 hook satisfied via ingestion-class RC-011 events.
