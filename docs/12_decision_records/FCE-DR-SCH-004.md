# FCE-DR-SCH-004 — CANON-1 shared canonicalization profile, integrity_hash input domain, audit content-hash domain, object_id uniqueness scope

**Status: RATIFIED 2026-07-06** — architect-role review (recommend-ratify,
incl. the no-version-bump ruling), red-team review (RT-M4S7, non-blocking),
and project-lead concurrence 2026-07-06 recorded below.
Date: 2026-07-06. Owner: data-model-engineer. Block: M4 Sprint 7.
Closes: FU-M2S3-1 (integrity_hash input domain), FU-M2S3-3 (object_id
uniqueness scope).

## Decision

D1. **CANON-1** is the single canonical serialization profile shared by the
envelope integrity_hash and the audit record_content_hash. Defined against
RFC 8785 (JSON Canonicalization Scheme) as reference alignment only:
(1) input is a JSON object per the domain definitions below; (2) object keys
sorted by Unicode code point, recursively; (3) no insignificant whitespace
(separators "," and ":"), UTF-8, non-ASCII emitted literally; (4) minimal
JSON string escaping; (5) lists preserve order EXCEPT declared
order-insensitive fields, sorted before serialization: release_caveat,
parent_object_ids, reason_codes, policy_rule_ids, source_object_ids;
(6) the hashed value domain at TRL 1-3 contains integers and null only — no
floats (project-lead direction 2026-07-06): audit field 13 confidence shall
be null and the writer refuses a non-null value fail-closed; non-null
confidence support is deferred to a later DR with a deterministic decimal
representation; (7) null is serialized as null; absent ≠ null — absence of a
required field is malformed and refused before hashing; (8) hash = sha-256
over the UTF-8 bytes, lowercase hex. PoC realization: Python stdlib
json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
plus explicit pre-sort of rule-5 fields; no new dependencies (leadership
decision #5 posture).

D2. **Envelope integrity_hash input domain** (resolves freeze-record field-14
deferral): sha-256 over CANON-1 of fields 1–6 and 8–13 (12 fields). Excluded:
field 7 ingest_timestamp (FCE-assigned at ingest), field 14 (self), field 15
policy_binding_state (FCE-authority-set only, B3 — forced at G1 by design).
G2 integrity check = recompute and compare; mismatch → quarantine, RC-001
path per the freeze record's G2 table. The G2 integrity clause is now
TESTABLE; Sprint 8 gains the deferred tamper-pair test (tamper an IN field →
mismatch; tamper an OUT field → hash verifies, other gates own protection).
Stated gap: schema v0.2.0 has no payload field; the hash binds the envelope
only. Payload binding requires a new field, new version, and a new DR
(TRL 4-5 design note, not attempted).

D3. **No version bump.** Architect ruling: the freeze record (field 14)
recorded "PASS with material UNCERTAINTY" and raised the input-domain
definition as an open item within v0.2.0 — the deferral is part of the frozen
state. Completing it changes no field, type, format, or wire representation;
GDR-006's supported set is untouched; no migration exists because no v0.2.0
object becomes invalid. Disposition: this DR + a dated annotation to docs/06
field 14. Rejected alternative: patch bump to 0.2.1 (stricter freeze-statement
reading) — mechanically noisy (validator supported-set update, fixture
regeneration) with zero semantic content.

D4. **Audit record_content_hash domain**: sha-256 over CANON-1 of all 18
common fields + event_detail, EXCLUDING field 14 (self) and field 16
(signature_placeholder), INCLUDING field 15 (previous_record_hash) — the
inclusion that makes deletion/reorder detectable (FCE-REQ-AUD-002). One
profile, two domain definitions, zero divergence.

D5. **object_id uniqueness scope: per-run** (one run = one audit chain at
TRL 1-3). Global uniqueness is unenforceable without unclaimed
infrastructure. Duplicate object_id detected at G2 → quarantine via the
RC-001 path with detail detection flag duplicate_object_id naming the
colliding ID. No new reason code: the registry is CLOSED (docs/07);
policy-engineer assesses at M7 whether duplicates warrant a dedicated code.
Cross-run aggregation must key on (package_id or run_id, object_id) —
FU-M4S7-3 disclosure.

## Ratification record

- Architect review (2026-07-06): checklist pass; no-bump ruling as D3;
  RECOMMEND-RATIFY.
- Red-team review (RT-M4S7, 2026-07-06): non-blocking; claim audit clean
  (RFC 8785 reference-alignment phrasing verified).
- Project-lead concurrence: 2026-07-06 — no-bump approved; CANON-1 approved;
  both hash domains approved as stated; confidence-null rule directed;
  per-run uniqueness + RC-001-with-flag approved.

## Trace

FCE-REQ-MET-010 (G2 testability), FCE-REQ-POL-001 (validation-layer
determinism), FCE-REQ-AUD-002 (chain), FCE-REQ-AUD-003 (R2 lineage
determinism), FCE-REQ-PRV-002 (lineage resolution).

## Facts / Assumptions / Judgment / Uncertainty

Facts: freeze-record field-14 deferral text; B3 forcing; EVD-M3 sorted-list
precedent; closed RC registry. Assumption: fixtures remain metadata-only at
TRL 1-3. Judgment: IN/OUT split; per-run scope; no-bump ruling; RFC 8785 as
reference profile. Uncertainty: payload binding (TRL 4-5); duplicate-ID
dedicated reason code (policy-engineer, M7).
