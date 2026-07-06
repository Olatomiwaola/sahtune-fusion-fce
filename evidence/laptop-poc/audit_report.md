# EVD-M4 — Audit Writer PoC Report

Evidence ID: EVD-M4. Owners: `audit-forensics-engineer` (impl) /
`test-evaluation-engineer` (V&V) / `data-model-engineer` (CANON-1). Block: M4 Sprint 8.
Basis commit 7dd5b15 (Sprint 7 close 6d87c94). Authorities: docs/08 v1,
FCE-DR-AUD-001, FCE-DR-SCH-004, docs/07 v1, docs/03 v0.4.

## Scope and layer separation

Code-correctness evidence only — NOT a concept-validation claim (docs/16 layer
separation). This report is the **GATE-B closure basis** (Sprints 4, 6, 8 all DONE); it
is **not** a self-declared gate. The GATE-B declaration is the project lead's, in chat,
on review of this evidence (docs/handoff/09 governance note). stdlib only; injected clock
(H4); signature placeholder (H6); no OPA, no network, no installs.

## Toolchain provenance

```text
$ .venv/bin/python --version
Python 3.12.13
$ .venv/bin/pytest --version
pytest 9.1.0
```

## Modules (ratified docs/08 file plan)

`src/fce_poc/audit/`: `canonical.py` (CANON-1, first), `envelope_integrity.py`,
`records.py` (internal helper — see judgment below), `writer.py` (append-only JSONL +
tail-verify), `chain.py` (R1), `replay.py` (R1+R2), `export.py` (package + manifest),
`demo.py` (sample generator). `src/fce_poc/provenance/links.py` (parent-link capture).
`schemas/audit/audit-record.schema.md` (description-level, docs/08 authority).

## FU-M4S7-1 boundary statement (verbatim)

In-file edit/delete/reorder detected by chain verification; whole-file substitution
regenerated from the public genesis constant NOT detectable from the file alone; external
chain-head anchoring is H6 (open); export manifests carry chain_head_hash as partial
mitigation.

## FU-M4S7-3 statement (verbatim)

Cross-run aggregation must key on (package_id or run_id, object_id), never object_id alone.

## Disclosures (H4 / mechanism-simulated / H6 / H7)

- Timestamps use the INJECTED clock (`event_timestamp.clock_source = "injected"`); no
  trusted/attested-time claim (H4 open). No wall-clock is read anywhere.
- Authentication flags in fixtures (e.g. `object_id_authenticated`, RC-011 rejects) are
  MECHANISM-SIMULATED (EVD-M3 pattern), not demonstrated authentication (H3/H4).
- `signature_placeholder` is a fixed non-crypto string (H6). Single-writer per run; audit
  concurrency total-order is H7, open, unclaimed.
- Envelope-only hash binding: no payload field at schema v0.2.0 (payload binding needs a
  new field + version + DR — not attempted).
- R3 (re-evaluation cross-check) is NOT implemented this sprint (optional by spec).

## Engineering judgment (recorded per instruction §3)

- `records.py` is an approved internal helper (project-lead override 2026-07-06): record
  construction/validation is separated from writer I/O.
- `envelope_integrity.py` lives in `audit/` so the M2 validator stays untouched; Sprint 8
  proves the G2 integrity check via tests (T4), it does not refactor the validator.
- `downgrade` is absent from the docs/08 requiredness-matrix table; the PoC supplies
  minimal requiredness (≥1 source, output required, semver, ≥1 rule, authority +
  transformation-proof detail).
- Non-decision events (ingestion-accept, transformation, export) carry a neutral
  disposition/enforcement drawn from the closed D3/action sets (e.g. permit); the audited
  outcome is in `decision`/`event_detail`.
- Policy-decision `event_detail` fields (`pip_attributes_consumed`, `detection_flags`,
  `deterministic_evaluation`) are OPTIONAL in the Sprint 8 PoC validator; aligning them to
  the docs/07 D4 atomic-emission contract (required) and adding the docs/08 `downgrade`
  matrix row are tracked as **FU-M4S8-1** (M5 Sprint 9). Sprint 8 behaviour stands until
  that closes.

## Coverage (test → trace → result)

| Test | Trace | Result |
|---|---|---|
| T1 canonical determinism | FCE-DR-SCH-004 D1, FCE-REQ-POL-001 | PASS |
| T2 float refusal | D1(6) | PASS |
| T3 non-null confidence refused | D1(6), docs/08 field 13 | PASS |
| T4 envelope tamper-pair (IN fails / OUT verifies) | FCE-DR-SCH-004 D2, FU-M2S3-1, FCE-REQ-MET-010 | PASS |
| T5 per-class emission 9/9 | FCE-REQ-AUD-001 | PASS |
| T6 requiredness-matrix rejections | FCE-DR-AUD-001 D2 | PASS |
| T7 sentinel-legality rejections | RT-M4S7-04 | PASS |
| T8 chain tamper set (edit/delete/reorder) | FCE-REQ-AUD-002 | PASS |
| T9 torn-write refuses fail-closed | FU-M4S7-2, RT-M4S7-02 | PASS |
| T10 replay R2 reconstruction | FCE-REQ-AUD-003 | PASS |
| T11 replay-poisoning ignores asserted id | RT-M4S7-03 | PASS |
| T12 provenance walk | FCE-REQ-PRV-001/-002 | PASS |
| T13 export manifest | FCE-REQ-EXP-001 | PASS |
| T14 duplicate object_id quarantine path | FCE-DR-SCH-004 D5 | PASS |
| T15 full repo suite green | regression | PASS (83) |

## Negative / fail-closed results (verbatim behaviour)

- Any float in a record or envelope input → `FloatInHashDomain` → refuse (T2).
- Non-null `confidence` → `RecordValidationError` → writer refuses (T3).
- IN-field envelope tamper → `verify_integrity` False; OUT-field tamper → True (T4).
- Requiredness violations (fusion 1 parent; ingestion missing `ingest_attempt_id`;
  unknown detail field; malformed/empty `event_timestamp`) → refuse (T6).
- Illegal sentinel-for-class (N/A-PRE-G4 on policy-decision; N/A-EXPORT on ingestion;
  semver on export) → refuse (T7).
- Chain edit/delete/reorder → R1 `ok=False` (T8). Torn tail → `AuditChainError` on writer
  start + R1 `ok=False` (T9).

## Sample chain (evidence/laptop-poc/audit_sample.jsonl)

8 records, deterministic (fixed ids, injected clock now=1000):
`['ingestion','ingestion','policy-decision','ingestion','transformation','fusion-decision','fusion-decision','export']`
— accepted (ingestion + policy-decision), G1 reject (RC-011 mechanism-simulated,
attempt-ID identity, poisoning source_asserted_object_id), transformation, permitted
fusion (2 parents), blocked cross-domain merge (RC-003, segregate), export. Verified
R1 `ok=True count=8` and R2 `ok=True errors=[] decisions=8`.

## Full verbatim pytest output — tests/audit (`.venv/bin/pytest tests/audit -v`)

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.0, pluggy-1.6.0 -- /Users/olaberry/dev/Kanatir-FCE/sahtune-fusion-fce/.venv/bin/python
rootdir: /Users/olaberry/dev/Kanatir-FCE/sahtune-fusion-fce
configfile: pytest.ini
collecting ... collected 15 items

tests/audit/test_canonical.py::test_t1_canonical_determinism_key_and_list_shuffle PASSED [  6%]
tests/audit/test_canonical.py::test_t2_float_refused_anywhere PASSED     [ 13%]
tests/audit/test_envelope_integrity.py::test_t4_tamper_in_field_fails PASSED [ 20%]
tests/audit/test_envelope_integrity.py::test_t4_tamper_out_field_still_verifies PASSED [ 26%]
tests/audit/test_export.py::test_t13_export_manifest PASSED              [ 33%]
tests/audit/test_provenance.py::test_t12_provenance_walk PASSED          [ 40%]
tests/audit/test_records.py::test_t5_per_class_emission_nine_of_nine PASSED [ 46%]
tests/audit/test_records.py::test_t6_requiredness_rejections PASSED      [ 53%]
tests/audit/test_records.py::test_t7_sentinel_legality_rejections PASSED [ 60%]
tests/audit/test_records.py::test_t14_duplicate_object_id_quarantine_path PASSED [ 66%]
tests/audit/test_replay.py::test_t10_replay_r2_reconstruction PASSED     [ 73%]
tests/audit/test_replay.py::test_t11_replay_poisoning_ignores_asserted_id PASSED [ 80%]
tests/audit/test_writer_chain.py::test_t3_non_null_confidence_refused PASSED [ 86%]
tests/audit/test_writer_chain.py::test_t8_chain_tamper_edit_delete_reorder PASSED [ 93%]
tests/audit/test_writer_chain.py::test_t9_torn_write_refuses_fail_closed PASSED [100%]

============================== 15 passed in 0.05s ==============================
```

Full repo suite (regression, T15): `83 passed` from `.venv/bin/pytest` (68 prior + 15 audit).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: 15/15 audit tests and 83/83 full-suite pass on CPython 3.12.13 / pytest 9.1.0;
  output above is verbatim; the sample chain verifies R1+R2.
- ASSUMPTION: single writer per run at TRL 1-3; M3 bundle/PIP fixtures reusable.
- ENGINEERING JUDGMENT: as recorded above (records.py split, integrity placement,
  downgrade requiredness, neutral non-decision disposition).
- UNCERTAINTY (open, non-blocking): whole-file substitution / external anchoring (H6),
  trusted time (H4), audit concurrency total-order (H7), payload binding (TRL 4-5).
