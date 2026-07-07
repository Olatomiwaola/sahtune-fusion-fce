# 08 — Audit Record Schema v1

Owner: `audit-forensics-engineer`. Skill: `fce-audit-record-design`.
v1 (M4 Sprint 7): 18 common fields + closed per-class `event_detail`
(FCE-DR-AUD-001, RATIFIED 2026-07-06); hash chain bound to CANON-1
(FCE-DR-SCH-004, RATIFIED 2026-07-06); replay spec R1/R2/R3; JSONL export +
integrity manifest. W3C PROV concepts and RFC 8785 (JSON Canonicalization
Scheme) are reference alignment only (cite w3.org/TR/prov-overview, RFC 8785).
No compliance, certification, or crypto claims. Signature fields are
placeholders (H6). Timestamps use the injected clock (H4). Single-writer per
run; concurrency serialization is H7, open, not claimed.

## Event classes (9, closed set)

| # | Class | Emitted at | Notes |
|---|---|---|---|
| 1 | ingestion | G1–G2 | Accepts AND G1/G2 rejects/quarantines. G1 source-authentication rejects (RC-011) land here — satisfies the H14 audit hook. RC-012 detection (non-reject) recorded via detection flags. |
| 2 | transformation | any transform | Parent linkage mandatory. |
| 3 | policy-decision | G4/PDP | Field source: docs/07 D4 output contract, consumed in full. |
| 4 | fusion-decision | G5/ARCH-08 | Permitted merges and blocked merges (RC-003, segregate). Multi-parent. |
| 5 | routing | route-to-higher-domain | |
| 6 | quarantine | G2/G4 quarantine paths | RC-001, RC-005. |
| 7 | downgrade | authorized downgrade | RC-006; authority + transformation-proof reference mandatory. |
| 8 | export | evidence export | References record range + manifest; includes manifest sha-256. |
| 9 | override | operator override attempts | Accepted (RC-007) AND rejected attempts both audited (FCE-REQ-OPS-002). |

## The 18 common fields (every record)

| # | Field | Type / constraint |
|---|---|---|
| 1 | audit_event_id | uuid, required, unique in chain |
| 2 | event_type | enum, the 9 classes above; closed set |
| 3 | event_timestamp | object with exactly two required sub-fields: `ts` (RFC3339 string) and `clock_source` (non-empty string; TRL 1-3 value `injected` — H4 dependency, EVD-M3 pattern). Missing/empty sub-field = malformed, refused. |
| 4 | actor_identity | string, required; service or operator ID. PoC values are fixture identities; actor authN is H3/H13, not claimed. |
| 5 | source_object_ids | list of uuid; contains ONLY trusted/validated object IDs — `[]` otherwise. Untrusted source-asserted IDs never appear here (FCE-DR-AUD-001). Cardinality per requiredness matrix. |
| 6 | output_object_id | uuid or null |
| 7 | policy_bundle_version | semver OR sentinel from the closed enum {`N/A-PRE-G4`, `N/A-EXPORT`}; sentinel legality is per-class (matrix); any other non-semver value is malformed, refused. |
| 8 | policy_rule_ids | list, may be empty; every entry must exist in docs/07. |
| 9 | decision | raw PDP/gate outcome before enforcement (e.g. permit, deny, reject). |
| 10 | reason_codes | list ⊆ closed registry RC-001..012; may be empty (clean permit). |
| 11 | enforcement_action | one of the 11 docs/07 actions. |
| 12 | disposition | D3 lattice value (FCE-DR-POL-001 total order). |
| 13 | confidence | null at TRL 1-3 (FCE-DR-SCH-004): the writer refuses a non-null value fail-closed. Advisory only, never an enforcement basis. Non-null support deferred to a later DR with a deterministic decimal representation. |
| 14 | record_content_hash | sha-256, lowercase hex, over CANON-1 canonical form of the record excluding fields 14 and 16, INCLUDING field 15 and `event_detail`. |
| 15 | previous_record_hash | sha-256 chain link; genesis constant = 64 zeros for the first record of a chain. |
| 16 | signature_placeholder | fixed placeholder string; no cryptographic claim (H6). |
| 17 | export_status | enum at emission, default `not-exported`; transitions are NEW records, never mutations (FCE-DR-AUD-001 D3). |
| 18 | review_status | enum at emission, default `unreviewed`; same immutability rule. |

## event_detail (closed, per-event-class typed object — FCE-DR-AUD-001 D2)

Unknown detail fields are refused fail-closed (mirrors FCE-DR-SCH-003 at the
envelope). Detail sub-schemas are part of schema v1:

- **ingestion**: `ingest_attempt_id` (uuid, writer-generated, REQUIRED — the
  FCE-authoritative identity of the attempt); `source_asserted_object_id`
  (optional, untrusted); `object_id_authenticated` (bool; false for G1
  rejects); detection flags (incl. `source_supplied_policy_binding_state` for
  RC-012, `duplicate_object_id` naming a colliding ID per FCE-DR-SCH-004);
  validation-rule references.
- **transformation**: transformation record reference.
- **policy-decision**: the D4 remainder exactly — `pip_attributes_consumed`
  (IDs + auth status; values never stored), `detection_flags`,
  `deterministic_evaluation` (all three REQUIRED per D4 atomic emission —
  FU-M4S8-1).
- **fusion-decision**: merge-permit reference (permitted) or RC-003 context
  (blocked).
- **routing**: destination domain.
- **quarantine**: review-queue reference; OPTIONAL `detection_flags` (M5 Sprint 10
  amendment — carries `mixed_bundle_versions` / `unrecorded_parentage` for the
  fusion quarantine outcomes, docs/18 §1/§5). Unknown detail fields still refused.
- **downgrade**: authority reference + transformation-proof reference.
- **export**: manifest reference, record range, and the manifest's own
  sha-256 (architect addition 2026-07-06: the chain binds manifest content,
  not merely a pointer to it).
- **override**: the four precondition results (authority, reason code, time
  limit, signature placeholder), envelope check outcome, override_immutable
  check outcome.

## D4 mapping (policy-decision class)

input_object_ids→5; bundle_version→7; rules_fired→8; disposition→12;
reason_codes→10; enforcement_action→11; evaluation_timestamp→3;
pip_attributes_consumed, detection_flags, deterministic_evaluation→event_detail.

## Per-class requiredness matrix

| Class | source_object_ids | output_object_id | bundle_version | rule_ids | detail |
|---|---|---|---|---|---|
| ingestion | ≥0 (trusted IDs only; `ingest_attempt_id` in detail is MANDATORY) | null | `N/A-PRE-G4` only | may be empty | ingestion detail |
| transformation | ≥1 | required | required semver | ≥0 | transform ref |
| policy-decision | ≥1 | null or set | required semver | ≥1, or empty with G-level reason | D4 remainder |
| fusion-decision | ≥2 | required if permitted; null if blocked | required semver | ≥1 | merge ref / RC-003 |
| routing | ≥1 | optional | required semver | ≥1 | destination domain |
| quarantine | ≥1 | null | required semver post-G4; `N/A-PRE-G4` if G2 | ≥0 | queue ref |
| downgrade | ≥1 | required | required semver | ≥1 | authority + transformation-proof reference |
| export | empty | null | `N/A-EXPORT` only | empty | manifest ref + range + manifest sha-256 |
| override | ≥1 | null | required semver | ≥1 | precondition results |

Sentinels are explicit values, never null-by-omission; a record violating the
matrix (including illegal sentinel-for-class) is malformed and the writer
refuses it fail-closed. Sentinel-legality rejection tests are an explicit
Sprint 8 obligation (RT-M4S7-04).

Amendment 2026-07-06 (FU-M4S8-1, closed): the `downgrade` row was added to the
matrix above (previously absent — the Sprint 8 PoC supplied it by engineering
judgment), and policy-decision `event_detail` is now REQUIRED (D4 atomic
emission). The M4 writer/validator enforces both; regression tests added.

Amendment 2026-07-06 (M5 Sprint 10, lead concurrence — no new DR): quarantine
`event_detail` gains an OPTIONAL `detection_flags` field so the fusion quarantine
outcomes (mixed pinned bundle versions → `mixed_bundle_versions`; parentage
cross-check mismatch → `unrecorded_parentage`, docs/18 §1/§5) record their flag on
the quarantine-class record itself. No policy-decision record is fabricated for
these; unknown-field refusal is unchanged.

## Hash chain and append-only semantics

- Storage: append-only JSONL, one record per line, one chain per run at
  TRL 1-3. Single-writer stated; H7 (concurrency total-order) open, unclaimed.
- record_content_hash per field 14 above; inclusion of field 15 in the hashed
  content is what makes deletion/reorder detectable (FCE-REQ-AUD-002).
- Canonicalization: CANON-1 (FCE-DR-SCH-004) — the single shared profile with
  the envelope integrity_hash. See docs/06 field-14 annotation and the DR.
- Tamper evidence scope at TRL 1-3 (RT-M4S7-01 disclosure, FU-M4S7-1):
  in-file edit, deletion, and reorder are detected by chain verification.
  Whole-file substitution regenerated from the public genesis constant is NOT
  detectable from the file alone; external chain-head anchoring is H6 (open).
  Export manifests carry the chain head hash, partially mitigating for
  exported packages. EVD-M4 must state this boundary.
- Tail verification on startup (RT-M4S7-02, FU-M4S7-2): before accepting new
  events the writer verifies the chain tail — last line is a complete record
  and hash-links correctly; a trailing partial line or broken link refuses
  fail-closed. Torn-write corruption test is a Sprint 8 obligation.
- Status transitions (fields 17/18): a transition is a NEW record referencing
  the original audit_event_id; current status is a derived view; the chain is
  never rewritten.
- Overflow/backpressure: audit-write failure halts the pipeline fail-closed —
  an object whose audit event cannot be persisted does not proceed. Rotation:
  segment files, chain continuing across segments, boundary recorded in the
  manifest (design note at TRL 1-3).

## Replay spec

- **R1 — chain integrity**: recompute every content hash, verify every
  previous-hash link from genesis. Pure audit-file input.
- **R2 — decision-sequence reconstruction** (the FCE-REQ-AUD-003
  demonstration): from audit records alone + referenced bundle versions,
  reconstruct the ordered decision sequence and verify internal consistency
  (dispositions ∈ D3 lattice; codes ∈ closed registry; bundle-version
  continuity; lattice consistency between fired rules and disposition).
  Read-only (register L3): replay never re-traverses G1–G7. Lineage
  resolution reads `source_object_ids` / `output_object_id` ONLY — never
  `event_detail.source_asserted_object_id` (RT-M4S7-03 test hook, Sprint 8).
- **R3 — re-evaluation cross-check (optional, labelled)**: re-run the
  evaluator on recorded inputs where bundle/PIP fixtures are available;
  compare disposition and reason codes. Requires inputs beyond the audit
  file; it is a cross-check, not the FCE-REQ-AUD-003 demonstration.

## Export package and manifest

Sprint 8 implements JSONL export + JSON integrity manifest; CSV and PDF are
documented designs only at TRL 1-3 (FCE-REQ-EXP-001 requires a documented
format + integrity manifest — JSONL + manifest satisfies it; no three-format
implementation claim). Manifest fields: package_id, created (injected clock),
format_version, record_count, first_event_id, last_event_id, chain_head_hash,
per-file sha-256 list, bundle_versions_referenced, segment_links. Every
export emits an export-class audit record whose detail carries the manifest
sha-256. Cross-run aggregation disclosure (RT-M4S7-05, FU-M4S7-3): object_id
uniqueness is per-run (FCE-DR-SCH-004); any aggregation across runs/packages
must key on (package_id or run_id, object_id), never object_id alone.

## Sprint 8 PoC file plan (plan only — no implementation in Sprint 7)

schemas/audit/audit-record.schema.md; src/fce_poc/audit/canonical.py (CANON-1
— first, all else depends on it); writer.py (append-only JSONL, tail-verify
on start, fail-closed on write error and non-null confidence); chain.py
(hash, link, verify); replay.py (R1+R2; R3 flag); export.py (JSONL package +
manifest); src/fce_poc/provenance/links.py (parent-link capture:
accepted/rejected/transformed/fused); tests/audit/ (per-class emission,
requiredness + sentinel-legality rejections, chain tamper set incl. torn
tail, envelope integrity_hash IN/OUT tamper pair, detail-ID replay-poisoning
fixture, float-free hash determinism, replay R1/R2, export manifest);
evidence/laptop-poc/audit_report.md (EVD-M4). Toolchain: existing .venv only
(Python 3.12.13, pytest 9.1.0), stdlib only, no network.

## Requirement trace

FCE-REQ-AUD-001, FCE-REQ-AUD-002, FCE-REQ-AUD-003, FCE-REQ-EXP-001,
FCE-REQ-PRV-001, FCE-REQ-PRV-002, FCE-REQ-OPS-002, FCE-REQ-KRN-001,
FCE-REQ-KRN-011, FCE-REQ-SEC-002, FCE-REQ-POL-001, FCE-REQ-MET-010 (G2
integrity now testable via CANON-1), FCE-REQ-ING-011 (RC-004 emission path,
RTM v0.4).

## Facts / Assumptions / Judgment / Uncertainty

- Facts: D4 field set, closed RC registry, D3 lattice, 15-field envelope,
  ratified FCE-DR-AUD-001 / FCE-DR-SCH-004 contents.
- Assumptions: single writer per run at TRL 1-3; M3 bundle/PIP fixtures
  reusable for Sprint 8.
- Judgment: event_detail sub-schema shapes; requiredness matrix; three-level
  replay split; manifest field set; file plan.
- Uncertainty: H4 trusted time, H6 anchoring/crypto, H7 concurrency — all
  open, disclosed, unclaimed. Payload binding absent at TRL 1-3 (envelope-only
  hash; schema change + DR required later).
