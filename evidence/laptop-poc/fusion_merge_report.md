# EVD-M5 — Fusion Merge Evaluator PoC Report

Evidence ID: EVD-M5. Owners: `sensor-fusion-engineer` (impl) /
`fce-lead-systems-architect` (interface) / `test-evaluation-engineer` (V&V). Block:
M5 Sprint 10. Basis commit 6145307 (Sprint 9 close bc97289). Governing spec:
`docs/18_fusion-kernel-merge-semantics.md`.

## Scope and layer separation

Code-correctness evidence only — NOT a concept-validation claim (docs/16 layer
separation). This report is the **GATE-D PARTIAL basis** (Sprint 14 completes GATE-D);
it is **not** a self-declared gate — the declaration is the project lead's, in chat, on
review of this evidence. stdlib only; injected clock (H4); no OPA, no network, no installs.

## Toolchain provenance

```text
$ .venv/bin/python --version
Python 3.12.13
$ .venv/bin/pytest --version
pytest 9.1.0
```

## Modules (`src/fce_poc/fusion/`)

- `permits.py` — `covers()`: exact-multiset match only (docs/18 §4; no wildcards, no
  `max_parents`).
- `labels.py` — ARCH-07 pure function: HWM most-restrictive; no I/O, no clock, no state.
- `crosscheck.py` — C3 bidirectional G5-entry parentage check over the provenance graph
  (`provenance/links.py`).
- `kernel.py` — ARCH-08: ≥2 distinct object_ids; single pinned bundle version; atomic
  permit sequence (decision → HWM label → kernel-written `parent_object_ids` → provenance
  link (the fusion-decision audit record) → audit); segregation path; quarantine paths
  (RC-001 + `unrecorded_parentage`; RC-005 + `mixed_bundle_versions`).

Audit emission uses the existing `audit/writer.py` + `audit/records.py` **unchanged** save
the one approved amendment (optional quarantine `detection_flags`, below).

## Coverage (test → trace → result)

| Test | Trace | Result |
|---|---|---|
| V1 permitted same-domain merge | FCE-REQ-KRN-011, FCE-REQ-PRV-002 | PASS |
| V2 blocked cross-domain merge (RC-003, segregate) | FCE-REQ-KRN-011 | PASS |
| V3 self-declared parentage (forward) → quarantine `unrecorded_parentage` | FCE-REQ-KRN-012 | PASS |
| V4 derived-type empty parents → refused | FCE-REQ-KRN-012 | PASS |
| V5 mixed bundle versions → quarantine RC-005 `mixed_bundle_versions` | FCE-REQ-POL-012, FCE-REQ-POL-001 | PASS |
| V6 override vs RC-003 block → rejected (override_immutable) | FCE-REQ-OPS-002 | PASS |
| V7 reverse cross-check (known output presents non-derived) → quarantine | FCE-REQ-KRN-012 | PASS |
| RT-M5S9-01 [T1,T2] does not cover [T1,T1] | FCE-REQ-KRN-011/-012 | PASS |
| RT-M5S9-02 superset re-request still denied | FCE-REQ-KRN-011 | PASS |
| RT-M5S9-03 duplicate object_id refused; [T,T] permitted when enumerated | FCE-REQ-KRN-011/-012/PRV-002 | PASS |
| RT-M5S9-05 override vs RC-005 / unrecorded_parentage quarantines rejected | FCE-REQ-OPS-002, FCE-REQ-POL-012 | PASS |
| quarantine detection_flags validate / unknown refused (records) | FCE-DR-AUD-001 D2 | PASS |

## Negative / fail-closed results (verbatim behaviour)

- No covering combination → `disposition=segregate`, `RC-003`, `output_object_id=null`
  (fusion-decision record).
- Duplicate / <2 distinct object_ids → `disposition=quarantine`, `RC-001`.
- Mixed pinned bundle versions → `disposition=quarantine`, `RC-005`,
  `detection_flags=[mixed_bundle_versions]` on the quarantine-class record.
- Parentage cross-check mismatch (forward V3, empty V4, reverse V7) →
  `disposition=quarantine`, `RC-001`, `detection_flags=[unrecorded_parentage]`.
- Override vs RC-003 / RC-005 / unrecorded_parentage → rejected (override_immutable /
  permitted_envelope excludes quarantine).

## Disclosures (verbatim)

- **H3/H4:** authentication flags are MECHANISM-SIMULATED (fixture values), not
  demonstrated authentication; the clock is INJECTED — no trusted-time claim (H4 open).
- **H6:** ARCH-09 provenance-store integrity / external anchoring is open.
- **H8:** the §5 same-pinned-version rule is a TRL 1-3 narrowing, not a resolution of H8
  (general cross-object bundle-version resolution remains open).
- **Fresh-uuid forgery residual (docs/18 §1):** an object forged entirely outside FCE
  custody under a fresh `object_id` is invisible to ARCH-09 and is bounded only by G1
  source authentication (mechanism-simulated at TRL 1-3).

## RT-M3S6-06 / H1 test closure

RT-M3S6-06 / H1 (no-unauthorized-merge as label-coverage-only, not verified parentage)
reach **test closure** here: V3 (forward self-declared parentage → quarantine), V4
(derived-type empty parents → refused), and V7 (reverse known-output-as-non-derived →
quarantine) all PASS. Design-level discharge was Sprint 9 (docs/18 §1, FCE-REQ-KRN-012);
this is the test-level closure.

## Engineering judgment / amendments (M5 Sprint 10, lead concurrence 2026-07-06, no new DR)

- **docs/18 §5 correction:** the `mixed_bundle_versions` flag is recorded on the
  **quarantine-class** record's `event_detail.detection_flags`, not on a fabricated
  policy-decision record; the same routing applies to the §1 `unrecorded_parentage` flag.
- **docs/08 quarantine-detail amendment:** quarantine `event_detail` gains an OPTIONAL
  `detection_flags` field (schema mirror + `records.py` `DETAIL_SCHEMA["quarantine"]`);
  unknown-field refusal is unchanged. Rationale: the two fusion quarantine outcomes must
  record their detection flag on the emitted quarantine record without inventing a
  policy-decision record and without weakening the closed-detail refusal.
- MERGE-PERMIT coverage is delegated to `fusion.permits.covers` (exact-multiset); the M3
  evaluator's old label-subset `covers_merge` was removed (no fallback/adapter).
- `RULE-POL-002` is used as the fired rule id for both permit and block fusion-decision
  records (docs/07 cross-domain merge rule); non-decision label values are neutral.

## Full verbatim pytest output — tests/fusion (`.venv/bin/pytest tests/fusion -v`)

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.0, pluggy-1.6.0 -- /Users/olaberry/dev/Kanatir-FCE/sahtune-fusion-fce/.venv/bin/python
rootdir: /Users/olaberry/dev/Kanatir-FCE/sahtune-fusion-fce
configfile: pytest.ini
collecting ... collected 11 items

tests/fusion/test_hooks.py::test_rt_m5s9_01_combination_not_membership PASSED [  9%]
tests/fusion/test_hooks.py::test_rt_m5s9_02_superset_denied PASSED       [ 18%]
tests/fusion/test_hooks.py::test_rt_m5s9_03_duplicate_id_and_tt_enumeration PASSED [ 27%]
tests/fusion/test_hooks.py::test_rt_m5s9_05_override_vs_quarantines PASSED [ 36%]
tests/fusion/test_vectors.py::test_v1_permitted_same_domain_merge PASSED [ 45%]
tests/fusion/test_vectors.py::test_v2_blocked_cross_domain_merge PASSED  [ 54%]
tests/fusion/test_vectors.py::test_v3_self_declared_parentage_quarantined PASSED [ 63%]
tests/fusion/test_vectors.py::test_v4_derived_empty_parents_refused PASSED [ 72%]
tests/fusion/test_vectors.py::test_v5_mixed_bundle_versions_quarantined PASSED [ 81%]
tests/fusion/test_vectors.py::test_v6_override_vs_rc003_rejected PASSED  [ 90%]
tests/fusion/test_vectors.py::test_v7_reverse_crosscheck_quarantined PASSED [100%]

============================== 11 passed in 0.03s ==============================
```

Full repo suite: **98 passed** from `.venv/bin/pytest` (85 prior + 11 fusion + 2 quarantine-detail records tests).

HOLD 1 RELEASED: fusion/permits.py exact-multiset covers(); M3 evaluator delegates merge coverage to it, old-shape logic REMOVED (no fallback, no adapter); bundle fixture rewritten to permit_id / permitted_combinations / output_authority=HWM; tests/policy/test_rule_pol_002 updated, semantics unchanged.

## Facts / Assumptions / Judgment / Uncertainty

- FACT: 11/11 fusion tests and 98/98 full-suite pass on CPython 3.12.13 / pytest 9.1.0;
  output above is verbatim.
- ASSUMPTION: the M3 bundle/PIP fixture layout extends to `permitted_combinations`
  without evaluator rework beyond the delegated `covers()` (confirmed by this sprint).
- ENGINEERING JUDGMENT: exact-multiset covers; HWM ordering (classification by trailing
  level, caveat union); ARCH-09 realized as the provenance graph over audit records; the
  amendments recorded above.
- UNCERTAINTY (open, disclosed): H4 trusted time, H6 anchoring, H7 concurrency, H8
  cross-version resolution; combination-enumeration scale at M6 (DR if it breaks);
  G5-entry cross-check cost (TARGET only, M8).
