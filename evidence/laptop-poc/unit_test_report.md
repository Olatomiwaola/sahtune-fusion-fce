# EVD-M2 — Laptop-PoC Schema-Validation Unit Test Report

Evidence ID: EVD-M2. Owner: `data-model-engineer`. Block: M2 Sprint 4 (global
Sprint 4). Implements `docs/05_data_model/m2-poc-file-plan.md` against schema v0.2.0
(`docs/05_data_model/m2-schema-freeze-record.md`) and the validation rules
(`docs/05_data_model/m2-validation-rules.md`).

Revised 2026-07-04 on basis commit ca75497 (M2 Sprint-4 punch list): taxonomy fixture
repopulated from docs/09+docs/06 with recorded sha-256; unknown-field handling ratified
by FCE-DR-SCH-003 and covered by LAP-UNIT-010. **Self-provenance:** this revision is
recorded in the punch-list commit whose parent is ca75497 (the immediate child of
ca75497 on `main`; see git log for the child hash — a commit cannot contain its own
hash).

## Scope and layer separation

This report is **code-correctness evidence only**. It is NOT a concept-validation or
proof claim (`docs/16` layer separation). Explicit non-scope at Sprint 4: no policy
evaluation (M3), no audit writer (M4 — only a stub interface exists), no merge logic
(M5), no open-source download (M6), no held-out evaluation (M7), no performance
figures (M8 — the timing pytest prints is incidental and unreported), no
integrity-hash verification (deferred, see below), no review-queue mechanics.

## Toolchain (leadership decision #5)

Python 3.12, standard library plus pinned pytest only — no other dependency. The venv
was created fresh and its two versions verified before this evidence run; the run
executes from `.venv/bin/pytest` only.

Verified provenance (exactly two versions):

```text
$ which python3.12
/opt/homebrew/bin/python3.12
$ python3.12 --version
Python 3.12.13
$ python3.12 -m venv .venv
$ .venv/bin/python -m pip install -r requirements.txt   # pytest==9.1.0 (pinned)
$ .venv/bin/python --version
Python 3.12.13
$ .venv/bin/pytest --version
pytest 9.1.0
```

- Interpreter: CPython **3.12.13** (Homebrew `python@3.12`, `/opt/homebrew/bin/python3.12`).
- Test runner: **pytest 9.1.0** (pinned in `requirements.txt`), installed into the
  project `.venv`; no other runtime or dev dependency.
- Run command (evidence + all test runs): `.venv/bin/pytest -v` from repo root
  (`pytest.ini`, `pythonpath = src`). No system/global interpreter or pytest is used.

## Taxonomy fixture provenance (RT-M2S3-04 resolved)

`data/fixtures/calibration/taxonomy.json` values come from the **docs/09 + docs/06
enumerations (the docs/07 registry does not yet exist)**: classification labels
`PROJ-LEVEL-1..3` and domains `DOMAIN-A, DOMAIN-B` and the modality set from
`docs/09_synthetic-dataset-plan.md`; `release_caveat` value `PROJ-CAVEAT-X` from the
`docs/06_metadata-schema.md` example. Token form is lower_snake per the docs/06 schema
example convention (field 5 example `eo_ir`); docs/09's `EO/IR` is prose. `docs/07`
carries the project-taxonomy disclaimer only and enumerates no values — authoring the
enumerated registry there is tracked as **FU-M2S4-1** (owner policy-engineer, due M3
Sprint 5, consumes OPEN-02 / leadership decision #2).

Recorded fixture hash (resolves RT-M2S3-04 by hash + provenance):

```text
sha-256(data/fixtures/calibration/taxonomy.json) =
  59979c4d72b79cba6dec02892cc2940d609a705a2a724b5416ec275749bec240
```

## Result summary

**44 passed, 0 failed, 0 skipped.** All Required Laptop Tests minted for M2
(LAP-UNIT-001..004, 006..010) and the RULE-VAL-018 determinism property pass.
LAP-UNIT-010 (unknown/extra field rejected fail-closed, FCE-DR-SCH-003) is new this
revision. LAP-UNIT-005 (identical input/policy determinism) remains an M3
policy-evaluator test; its validator-layer repeat-determinism assertions ride inside
LAP-UNIT-001/007 per RULE-VAL-018.

## Per-rule coverage (RULE-VAL-001..018 -> test -> result)

| Rule | Constraint (abridged) | Layer | Test(s) | Result |
|---|---|---|---|---|
| RULE-VAL-001 | object_id present, valid uuid (duplicate-ID handling pending scope) | G2 | LAP-UNIT-001/002/007 | PASS |
| RULE-VAL-002 | schema_version supported semver; unsupported rejected before policy | G1 | LAP-UNIT-004 | PASS |
| RULE-VAL-003 | data_origin in {SYNTHETIC, SYNTHETIC-DERIVED, PUBLIC-OPEN-SOURCE}; LIVE rejected fail-closed at G1 | G1 | LAP-UNIT-006 | PASS |
| RULE-VAL-004 | PUBLIC-OPEN-SOURCE requires source-manifest reference (presence) | G2 | LAP-UNIT-008 | PASS |
| RULE-VAL-005 | synthetic banner flag set on disposition output | G2 (output) | LAP-UNIT-001 | PASS |
| RULE-VAL-006 | source_sensor_id present, non-empty string | G2 | LAP-UNIT-002/007 | PASS |
| RULE-VAL-007 | modality within taxonomy fixture; unknown fails closed | G2 | LAP-UNIT-007 | PASS |
| RULE-VAL-008 | acquisition_timestamp RFC3339 + clock_source present | G2 | LAP-UNIT-002/007 | PASS |
| RULE-VAL-009 | ingest_timestamp RFC3339 | G2 | LAP-UNIT-007 | PASS |
| RULE-VAL-010 | classification_label within taxonomy fixture; no real GoC marking | G2 | LAP-UNIT-002/007 | PASS |
| RULE-VAL-011 | domain_label within taxonomy fixture | G2 | LAP-UNIT-007 | PASS |
| RULE-VAL-012 | release_caveat is list (empty ok, null fails); members in taxonomy | G2 | LAP-UNIT-009 | PASS |
| RULE-VAL-013 | handling_instructions present, non-empty string | G2 | LAP-UNIT-002 | PASS |
| RULE-VAL-014 | provenance_ref present, uri/graph-node-id shape | G2 | LAP-UNIT-002/007 | PASS |
| RULE-VAL-015 | parent_object_ids list of uuid (null fails); non-empty for derived/merged | G2 | LAP-UNIT-007/009 | PASS |
| RULE-VAL-016 | integrity_hash sha-256 **format only** — verification DEFERRED | G2 | LAP-UNIT-007 | PASS (format); verification DEFERRED |
| RULE-VAL-017 | policy_binding_state forced to `unvalidated` at G1; source value detected | G1 | LAP-UNIT-003 | PASS |
| RULE-VAL-018 | identical envelope input -> identical disposition/reason/flags | property | LAP-UNIT-001/007 | PASS |

Unknown/extra envelope fields (not a RULE-VAL id): reject fail-closed at G2 with RC-001,
**ratified by FCE-DR-SCH-003** (resolves RT-M2S3-03, closes FU-M2S3-2). Carried as the
`UNKNOWN-FIELD` disposition marker. Tested: `test_lap_unit_010_unknown_field_rejected`
(LAP-UNIT-010) — PASS.

## Integrity-hash deferral (explicit)

RULE-VAL-016 checks the sha-256 **format only**. Hash **verification is EXPLICITLY
DEFERRED** pending the hash-input-domain definition (which bytes/fields are hashed,
canonicalization) — `docs/06` does not define it (freeze record field 14; RT-M2S3-02;
follow-up FU-M2S3-1, owner data-model-engineer, due M4). The G2 "integrity check
failure" disposition clause is therefore **UNTESTABLE at Sprint 4** and no
hash-verification claim is made here.

## Negative results (verbatim disposition records)

Disposition record shape: `{disposition, reason_code, failed_rules, detection_flags,
synthetic_banner}`. G1 rejections carry `disposition='rejected'`; G2 fail-closed carries
`disposition='quarantined'`, both with reason code RC-001 (the only fail-closed reason
code available at M2 per RTM v0.2; full registry in `docs/07`, consistency check
deferred). Multi-failure determinism: all failed rules reported, sorted, no
first-failure short-circuit.

```text
[LAP-UNIT-001] valid_object.json
    disposition   = 'accepted'
    reason_code   = None
    failed_rules  = []
    detection     = []
    synthetic_banner = True

[LAP-UNIT-002] missing_field.json          (handling_instructions omitted)
    disposition   = 'quarantined'
    reason_code   = 'RC-001'
    failed_rules  = ['RULE-VAL-013']
    detection     = []
    synthetic_banner = True

[LAP-UNIT-007] malformed_types.json        (all failures reported, no short-circuit)
    disposition   = 'quarantined'
    reason_code   = 'RC-001'
    failed_rules  = ['RULE-VAL-001', 'RULE-VAL-006', 'RULE-VAL-007', 'RULE-VAL-008',
                     'RULE-VAL-009', 'RULE-VAL-010', 'RULE-VAL-011', 'RULE-VAL-012',
                     'RULE-VAL-013', 'RULE-VAL-014', 'RULE-VAL-015', 'RULE-VAL-016']
    detection     = []
    synthetic_banner = True

[LAP-UNIT-003] source_supplied_binding_state.json   (policy_binding_state='validated')
    disposition   = 'accepted'
    reason_code   = None
    failed_rules  = []
    detection     = ['policy_binding_state_source_supplied']   # forced to unvalidated
    synthetic_banner = True

[LAP-UNIT-004] unsupported_version.json    (schema_version 0.1.0)
    disposition   = 'rejected'             # before policy, never reaches G2
    reason_code   = 'RC-001'
    failed_rules  = ['RULE-VAL-002']
    detection     = []
    synthetic_banner = True

[LAP-UNIT-006] live_data_origin.json       (data_origin=LIVE)
    disposition   = 'rejected'             # fail-closed at G1 (FCE-DR-SCH-002)
    reason_code   = 'RC-001'
    failed_rules  = ['RULE-VAL-003']
    detection     = []
    synthetic_banner = False

[LAP-UNIT-008] open_source_missing_manifest.json    (PUBLIC-OPEN-SOURCE, no manifest ref)
    disposition   = 'quarantined'
    reason_code   = 'RC-001'
    failed_rules  = ['RULE-VAL-004']
    detection     = []
    synthetic_banner = False
```

## Full pytest output (verbatim)

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.0, pluggy-1.6.0 -- /Users/olaberry/dev/Kanatir-FCE/sahtune-fusion-fce/.venv/bin/python
rootdir: /Users/olaberry/dev/Kanatir-FCE/sahtune-fusion-fce
configfile: pytest.ini
testpaths: tests
collecting ... collected 44 items

tests/test_envelope.py::test_normalize_is_deterministic PASSED           [  2%]
tests/test_envelope.py::test_normalization_identity_fixture_vs_runtime PASSED [  4%]
tests/test_envelope.py::test_valid_object_has_all_mandatory_fields_present PASSED [  6%]
tests/test_envelope.py::test_absent_field_is_missing_sentinel PASSED     [  9%]
tests/test_envelope.py::test_null_is_preserved_and_distinct_from_missing PASSED [ 11%]
tests/test_envelope.py::test_empty_list_is_preserved PASSED              [ 13%]
tests/test_envelope.py::test_unknown_fields_are_captured_sorted PASSED   [ 15%]
tests/test_envelope.py::test_known_companion_fields_are_not_unknown PASSED [ 18%]
tests/test_gates.py::test_forcing_sets_unvalidated_and_flags_source_supplied PASSED [ 20%]
tests/test_gates.py::test_forcing_without_source_value_sets_no_flag PASSED [ 22%]
tests/test_gates.py::test_forcing_overrides_any_ingested_value PASSED    [ 25%]
tests/test_gates.py::test_supported_version_and_allowed_origin_pass PASSED [ 27%]
tests/test_gates.py::test_unsupported_version_fails_rule_002 PASSED      [ 29%]
tests/test_gates.py::test_live_origin_fails_rule_003 PASSED              [ 31%]
tests/test_gates.py::test_allowed_origins_all_pass_gate PASSED           [ 34%]
tests/test_gates.py::test_unknown_origin_fails_gate PASSED               [ 36%]
tests/test_validator.py::test_lap_unit_001_valid_object_accepted PASSED  [ 38%]
tests/test_validator.py::test_lap_unit_002_missing_field_quarantined PASSED [ 40%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[acquisition_timestamp-RULE-VAL-008] PASSED [ 43%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[classification_label-RULE-VAL-010] PASSED [ 45%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[clock_source-RULE-VAL-008] PASSED [ 47%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[domain_label-RULE-VAL-011] PASSED [ 50%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[handling_instructions-RULE-VAL-013] PASSED [ 52%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[ingest_timestamp-RULE-VAL-009] PASSED [ 54%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[integrity_hash-RULE-VAL-016] PASSED [ 56%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[modality-RULE-VAL-007] PASSED [ 59%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[object_id-RULE-VAL-001] PASSED [ 61%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[parent_object_ids-RULE-VAL-015] PASSED [ 63%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[provenance_ref-RULE-VAL-014] PASSED [ 65%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[release_caveat-RULE-VAL-012] PASSED [ 68%]
tests/test_validator.py::test_lap_unit_002_per_field_variants[source_sensor_id-RULE-VAL-006] PASSED [ 70%]
tests/test_validator.py::test_lap_unit_003_source_supplied_binding_state PASSED [ 72%]
tests/test_validator.py::test_lap_unit_004_unsupported_version_rejected PASSED [ 75%]
tests/test_validator.py::test_lap_unit_006_live_origin_rejected_fail_closed PASSED [ 77%]
tests/test_validator.py::test_lap_unit_007_malformed_values_quarantined PASSED [ 79%]
tests/test_validator.py::test_lap_unit_008_open_source_missing_manifest_quarantined PASSED [ 81%]
tests/test_validator.py::test_lap_unit_009_null_release_caveat_fails PASSED [ 84%]
tests/test_validator.py::test_lap_unit_009_null_parent_object_ids_fails PASSED [ 86%]
tests/test_validator.py::test_lap_unit_009_empty_lists_accepted PASSED   [ 88%]
tests/test_validator.py::test_derived_lifecycle_requires_nonempty_parents PASSED [ 90%]
tests/test_validator.py::test_lap_unit_010_unknown_field_rejected PASSED [ 93%]
tests/test_validator.py::test_integrity_hash_format_only PASSED          [ 95%]
tests/test_validator.py::test_rule_val_018_determinism_accepted PASSED   [ 97%]
tests/test_validator.py::test_rule_val_018_determinism_multifailure PASSED [100%]

============================== 44 passed in 0.05s ==============================
```

## Open items carried from this run

- FU-M2S3-1 — integrity_hash input-domain definition (owner data-model-engineer, due
  M4). RULE-VAL-016 stays format-only until then.
- FU-M2S3-2 — **CLOSED** by FCE-DR-SCH-003 (unknown/extra fields reject fail-closed at
  G2; LAP-UNIT-010). RT-M2S3-03 resolved.
- FU-M2S3-3 — object_id uniqueness scope + duplicate-ID disposition (owner
  data-model-engineer). RULE-VAL-001 enforces presence/format only.
- FU-M2S4-1 — author the enumerated project-taxonomy registry in `docs/07` (owner
  policy-engineer, due M3 Sprint 5, consumes OPEN-02 / leadership decision #2). Until
  then the fixture is sourced from docs/09+docs/06 with the recorded hash above.
- RT-M2S3-04 — **RESOLVED** by hash + provenance (taxonomy section above).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: 44/44 tests pass on CPython 3.12.13 with pinned pytest 9.1.0; outputs above are
  verbatim.
- FACT: the taxonomy fixture values are the docs/09 + docs/06 enumerations (the docs/07
  registry does not yet exist); token form follows the docs/06 example convention. The
  fixture is hash-pinned (sha-256 above); unknown values fail closed.
- ENGINEERING JUDGMENT: module decomposition, fixture design, and (now ratified by
  FCE-DR-SCH-003) the unknown-field reject-fail-closed disposition.
- UNCERTAINTY: FU-M2S3-1 (integrity-hash input domain) and FU-M2S3-3 (object_id
  uniqueness scope) remain open; integrity-hash verification stays deferred to M4.

## Annotation 2026-07-05

FU-M2S4-1 completed under decision #2 (approved 2026-07-04); the `docs/07` registry
now exists and is authoritative; the fixture `_provenance` line stating otherwise is
historical, retained to preserve the pinned hash. The FU-M2S4-1 scheduling note above
is superseded by the register (`docs/handoff/05_open-items-and-decision-register.md`).
