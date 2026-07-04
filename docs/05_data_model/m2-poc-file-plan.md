# M2 Sprint 3 — Validation PoC File Plan (for Sprint 4, Claude Code)

Repo home (proposed, ENGINEERING JUDGMENT): `docs/05_data_model/m2-poc-file-plan.md`.
Owner: `data-model-engineer`. File plan only — no code is written in this chat.
Tooling per leadership decision #5: Python 3.12, standard library plus pinned pytest
only; no other dependency without a new decision (aligned with FCE-DR-POC-007 intent).

## Directory layout and modules

```text
src/fce_poc/__init__.py
src/fce_poc/envelope.py        # Envelope dataclass; the SINGLE normalization function
                               # used by both the fixture builder and the runtime path
                               # (GDR-016 normalization identity)
src/fce_poc/gates.py           # G1-scope behaviour for M2: envelope-version gate
                               # (RULE-VAL-002, GDR-006), data_origin gate incl. LIVE
                               # rejection (RULE-VAL-003), policy_binding_state forcing
                               # with detection flag (RULE-VAL-017, B3/GDR-007)
src/fce_poc/validator.py       # G2 validation: RULE-VAL-001, 004-016; disposition
                               # record {disposition, reason_code, failed_rules,
                               # detection_flags, synthetic_banner} — RC-001 quarantine
                               # path; audit emission is a stub interface only (M4 owns
                               # the audit writer; no audit claims at M2)
src/fce_poc/taxonomy.py        # Loads taxonomy fixture (values to be populated from
                               # docs/07 in Claude Code; unknown value = fail closed)
data/fixtures/calibration/taxonomy.json                      # from docs/07
data/fixtures/calibration/valid_object.json                  # SYNTHETIC values only
data/fixtures/calibration/missing_field.json                 # one per-field variant set
data/fixtures/calibration/malformed_types.json               # type/enum/format/null set
data/fixtures/calibration/source_supplied_binding_state.json # B3 fixture (validated)
data/fixtures/calibration/unsupported_version.json           # schema_version 0.1.0
data/fixtures/calibration/live_data_origin.json              # data_origin = LIVE
data/fixtures/calibration/open_source_missing_manifest.json  # POS without manifest ref
tests/test_envelope.py
tests/test_gates.py
tests/test_validator.py
evidence/laptop-poc/unit_test_report.md                      # EVD-M2 target path
requirements.txt                                             # pytest==<pinned in Sprint 4>
```

All fixture values are SYNTHETIC and carry `data_origin = SYNTHETIC` with the banner
flag, except the two negative-origin fixtures whose purpose is rejection. Fixtures are
calibration-set only; no held-out material exists at M2 (held-out sealing is M6,
GDR-003/004 scope).

## Test list

| Test ID | Status | Test | Expected result | Rules |
|---|---|---|---|---|
| LAP-UNIT-001 | pre-existing (`docs/16`) | Valid envelope passes schema validation | Accepted at G2; synthetic banner flag set; repeat evaluation identical | RULE-VAL-001..018 happy path |
| LAP-UNIT-002 | pre-existing (`docs/16`) | Missing mandatory metadata (per-field variants) | Fail closed at G2; quarantined; RC-001 | RULE-VAL-001, 006, 008, 010, 013, 014 |
| LAP-UNIT-003 | pre-existing (`docs/16`) | Source-supplied binding state (`validated`) | Forced to `unvalidated`; source value not trusted; detection flag recorded | RULE-VAL-017 |
| LAP-UNIT-004 | pre-existing (`docs/16`) | Unsupported envelope version (0.1.0 fixture) | Rejected before policy | RULE-VAL-002 |
| LAP-UNIT-006 | minted in Sprint 3 | data_origin = LIVE | Rejected fail-closed at G1 | RULE-VAL-003 |
| LAP-UNIT-007 | minted in Sprint 3 | Malformed values (bad uuid, bad RFC3339, unknown taxonomy value, bad hash format, wrong types) | Fail closed at G2; quarantined; RC-001; repeat evaluation identical | RULE-VAL-001, 007-011, 014-016, 018 |
| LAP-UNIT-008 | minted in Sprint 3 | PUBLIC-OPEN-SOURCE object without a source-manifest reference | Fail closed at G2; RC-001 | RULE-VAL-004 |
| LAP-UNIT-009 | minted in Sprint 3 | Null-vs-empty: release_caveat = null and parent_object_ids = null (fail) vs empty lists (pass where lifecycle permits) | Null fails closed RC-001; empty list accepted | RULE-VAL-012, 015 |

LAP-UNIT-005 (identical input/policy determinism) remains an M3 policy-evaluator test;
validator-layer repeat-determinism assertions ride inside LAP-UNIT-001/007 per
RULE-VAL-018. LAP-UNIT-006..009 are minted in Sprint 3 — flagged per the M2 block
constraint; `docs/16` Required Laptop Tests table gains these rows at commit time.

## Explicit non-scope at Sprint 4

No policy evaluation (M3), no audit writer (M4), no merge logic (M5), no open-source
data download (M6), no held-out evaluation (M7), no performance figures (M8 — any
timing observed is incidental and unreported), no integrity-hash verification (deferred
pending input-domain definition), no review-queue mechanics. Green results here are
code-correctness evidence only, never a concept-validation or proof claim (`docs/16`
layer separation).

## EVD-M2 definition

EVD-M2 = `evidence/laptop-poc/unit_test_report.md`: pytest output for the full test
list, per-rule coverage table (RULE-VAL-001..018 → test → result), the explicit
integrity-hash deferral note, and negative results verbatim. Sprint 4 is DONE only when
EVD-M2 exists at that path and the tracker Status cell is updated (tracker standing
rule).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: fixture cases and layout derive from the M2 block instructions, `docs/16`, and
  the validation-rule list; tooling per leadership decision #5.
- ASSUMPTION: docs/07 taxonomy values are available to Claude Code at Sprint 4.
- ENGINEERING JUDGMENT: module decomposition; test-ID minting; EVD-M2 shape.
- UNCERTAINTY: unknown-field handling decision (must be made before test_validator.py
  is finalized); pytest pin chosen in Sprint 4.
