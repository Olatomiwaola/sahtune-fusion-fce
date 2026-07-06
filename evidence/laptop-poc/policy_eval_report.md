# EVD-M3 — Policy-Evaluator Unit Test Report

Evidence ID: EVD-M3. Owner: `policy-engineer` (impl) / `test-evaluation-engineer`
(V&V). Block: M3 Sprint 6 (global Sprint 6). Basis commit 270624e, 2026-07-05.
Implements the Sprint 5 evaluator file plan against docs/07 v1 (default-deny PDP,
closed RC registry RC-001..012, D3 severity lattice, D4 output contract,
RULE-POL-001..006).

## Scope and layer separation

Code-correctness evidence only — NOT a concept-validation or proof claim (docs/16
layer separation). The evaluator is a deterministic **Python** interpretation of a
JSON policy bundle fixture; OPA/Rego is a reference pattern only (no OPA, no
network, no new installs). No gate is declared by this sprint alone — GATE-B
remains partial until Sprints 4, 6, 8 are all done.

## Toolchain provenance (leadership decision #5; EVD-M2 pattern)

Python 3.12 + pinned pytest only; run from the project `.venv` only.

```text
$ .venv/bin/python --version
Python 3.12.13
$ .venv/bin/pytest --version
pytest 9.1.0
```

- Interpreter: CPython **3.12.13** (Homebrew `python@3.12`).
- Runner: **pytest 9.1.0** (pinned, `requirements.txt`), from `.venv/bin/pytest`.

## FU-M3S5-1 obligations (stated verbatim, per register / RT-M3S5)

1. **Override time-limit evaluation depends on an injected clock; trusted /
   attested time is H4, open.** `attributes.InjectedClock` and
   `override.time_limit_valid` read only the injected tick — there are no
   wall-clock reads anywhere in the evaluator. No trusted-time capability is
   claimed (RT-M3S5-02).
2. **RC-011 source-authentication cases are mechanism-simulated (fixture flags),
   not demonstrated authentication (H3/H4).** The `source_authenticated` flag is a
   fixture value; the tests prove the G1 plumbing (reject fail-closed with RC-011),
   NOT that authentication was performed. EVD-M3 makes no authentication claim
   (RT-M3S5-03).

## Result summary

**24 policy tests passed** (0 failed, 0 skipped); **68 passed** across the full
repo suite (44 M2 + 24 M3). Every listed TST-POL case and the FCE-REQ-POL-001
determinism property pass.

## Coverage (test -> rule / requirement)

| Test | Covers | Result |
|---|---|---|
| test_rules_001_003::…001 | TST-POL-001 (RULE-POL-001 same-domain permit) | PASS |
| test_rules_001_003::…002 | TST-POL-002 (RULE-POL-002 cross-domain merge → block, RC-003) | PASS |
| test_rules_001_003::…003 | TST-POL-003 (RULE-POL-003 ambiguous → quarantine, RC-005) | PASS |
| test_pip_auth::…spoofed / …unauthenticated | TST-POL-004 (RULE-POL-004 → RC-008 fail-closed at G4) | PASS |
| test_override_envelope::…005a-e | TST-POL-005a-e (RULE-POL-005; 005d RC-002 immutable; 005e expiry by injected clock) | PASS |
| test_deny_overrides::…006a-c | TST-POL-006a-c (RULE-POL-006 lattice combination) | PASS |
| test_g1_reason_codes::…009/010/011/012 | G1 reason codes (011 mechanism-simulated; 012 detection, non-reject) | PASS |
| test_determinism::… | FCE-REQ-POL-001 (identical inputs → identical record + hash) | PASS |
| test_registry_guard::… | codes/actions ⊆ docs/07; taxonomy set-equality vs D6 families; retained sha-256 pin | PASS |

## D4 decision-record shape (emitted by the evaluator)

Fields (docs/07 D4 output contract): `input_object_ids`, `pip_attributes_consumed`
(id + auth status), `bundle_version` (pinned at G4 entry), `rules_fired`,
`disposition` (D3 lattice), `reason_codes` (closed registry), `enforcement_action`,
`detection_flags`, `evaluation_timestamp` (injected clock), `deterministic_evaluation`.
All list fields are sorted so the record is content-stable; `record_hash` gives a
sha-256 over the canonical JSON, hash-compared in the determinism tests.

## Registry / taxonomy guard (test_registry_guard)

- Reason codes used = exactly RC-001..012, all present in the docs/07 closed
  registry (subset check passes).
- All 11 actions and the 9 D3 lattice dispositions appear in docs/07.
- Calibration taxonomy fixture families **set-equal** the docs/07 D6 families, AND
  the fixture still matches its retained pin
  `sha-256 = 59979c4d72b79cba6dec02892cc2940d609a705a2a724b5416ec275749bec240`.
  Both pass; the fixture file is never edited by the test.

## Negative results (verbatim dispositions asserted by tests)

- G1 `data_origin=LIVE` → `disposition=reject`, `RC-010` (never reaches policy).
- G1 unsupported `schema_version` → `reject`, `RC-009`.
- G1 `source_authenticated=false` (mechanism-simulated) → `reject`, `RC-011`.
- Spoofed / unauthenticated PIP attribute → `block`, `RC-008` (fail-closed at G4).
- Unpermitted cross-domain merge → `block`, `RC-003`.
- Ambiguous classification → `quarantine`, `RC-005`.
- Override vs RC-002 / RC-003 (override_immutable) → override rejected; block stands.
- Expired override (injected clock) → override rejected.

## Full pytest output — policy suite (verbatim, `.venv/bin/pytest tests/policy -v`)

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.0, pluggy-1.6.0 -- /Users/olaberry/dev/Kanatir-FCE/sahtune-fusion-fce/.venv/bin/python
rootdir: /Users/olaberry/dev/Kanatir-FCE/sahtune-fusion-fce
configfile: pytest.ini
collecting ... collected 24 items

tests/policy/test_deny_overrides.py::test_tst_pol_006a_permit_restrict_yields_restrict PASSED [  4%]
tests/policy/test_deny_overrides.py::test_tst_pol_006b_permit_block_yields_block PASSED [  8%]
tests/policy/test_deny_overrides.py::test_tst_pol_006c_unresolvable_quarantines_never_permit PASSED [ 12%]
tests/policy/test_determinism.py::test_permit_evaluation_is_deterministic PASSED [ 16%]
tests/policy/test_determinism.py::test_reject_evaluation_is_deterministic PASSED [ 20%]
tests/policy/test_g1_reason_codes.py::test_rc009_unsupported_schema_version_rejected PASSED [ 25%]
tests/policy/test_g1_reason_codes.py::test_rc010_live_data_origin_rejected PASSED [ 29%]
tests/policy/test_g1_reason_codes.py::test_rc011_source_authentication_failure_rejected_mechanism_simulated PASSED [ 33%]
tests/policy/test_g1_reason_codes.py::test_rc012_source_supplied_binding_state_detected_not_rejected PASSED [ 37%]
tests/policy/test_override_envelope.py::test_tst_pol_005a_valid_override_accepted PASSED [ 41%]
tests/policy/test_override_envelope.py::test_tst_pol_005b_override_vs_rc003_cross_domain_block_rejected PASSED [ 45%]
tests/policy/test_override_envelope.py::test_tst_pol_005c_missing_precondition_rejected PASSED [ 50%]
tests/policy/test_override_envelope.py::test_tst_pol_005d_override_vs_rc002_immutable_rejected PASSED [ 54%]
tests/policy/test_override_envelope.py::test_tst_pol_005e_expired_override_rejected PASSED [ 58%]
tests/policy/test_pip_auth.py::test_tst_pol_004_spoofed_attribute_fails_closed PASSED [ 62%]
tests/policy/test_pip_auth.py::test_tst_pol_004_unauthenticated_attribute_fails_closed PASSED [ 66%]
tests/policy/test_pip_auth.py::test_valid_pip_does_not_trip_rule_004 PASSED [ 70%]
tests/policy/test_registry_guard.py::test_reason_codes_subset_of_docs07_registry PASSED [ 75%]
tests/policy/test_registry_guard.py::test_actions_and_lattice_present_in_docs07 PASSED [ 79%]
tests/policy/test_registry_guard.py::test_taxonomy_fixture_set_equals_docs07_d6_families PASSED [ 83%]
tests/policy/test_registry_guard.py::test_taxonomy_fixture_matches_retained_sha256_pin PASSED [ 87%]
tests/policy/test_rules_001_003.py::test_tst_pol_001_same_domain_permit PASSED [ 91%]
tests/policy/test_rules_001_003.py::test_tst_pol_002_cross_domain_merge_blocked PASSED [ 95%]
tests/policy/test_rules_001_003.py::test_tst_pol_003_ambiguous_classification_quarantined PASSED [100%]

============================== 24 passed in 0.01s ==============================
```

Full repo suite: `68 passed` (44 M2 + 24 M3) from `.venv/bin/pytest`.

## Facts / Assumptions / Judgment / Uncertainty

- FACT: 24/24 policy tests and 68/68 full-suite pass on CPython 3.12.13 / pytest
  9.1.0; output above is verbatim.
- ASSUMPTION: the JSON bundle fixture and PIP fixtures are synthetic; the
  signature check is a placeholder (no crypto; real root-of-trust is H6).
- ENGINEERING JUDGMENT: module decomposition, request/decision-record shaping,
  and the mapping of rule outcomes to lattice dispositions.
- UNCERTAINTY (open, non-blocking): trusted/attested time (H4, RT-M3S5-02) and
  real source authentication (H3/H4, RT-M3S5-03) are out of scope at TRL 1-3;
  EVD-M3 claims neither. Tracked under FU-M3S5-1.
