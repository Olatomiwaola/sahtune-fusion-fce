# 04 — Traceability Map (TRL 1-3, M1–M7)

Block → sprint → source docs → requirement IDs → evidence artifact → review gate
→ repo update target. Evidence IDs (EVD-*) are assigned when the artifact is
produced. Full cell text; no clipping.

| Block | Sprint | Source docs | Requirement IDs | Evidence artifact | Review gate | Repo update target |
|---|---|---|---|---|---|---|
| M1 | S1 | `02`, `03`, `00` | FCE-ESS-01..06, FCE-DES-01..04 | Draft finalized RTM rows | — | `docs/03_rtm.md`, `docs/02_capability-decomposition.md` |
| M1 | S2 | `03`, `02` | all FCE-REQ-* | Coverage report (EVD-M1) | GATE-A | `docs/03_rtm.md` |
| M2 | S1 | `06`, `04` | FCE-REQ-MET-010, PRV-001/002, POL-011 | Schema v1 + provenance model | — | `docs/06_metadata-schema.md` |
| M2 | S2 | `06`, `15` | FCE-REQ-MET-010, PRV-001/002 | Schema-validation PoC + test output (EVD-M2) | GATE-B (partial) | `docs/06_metadata-schema.md`, future PoC source/tests |
| M3 | S1 | `07`, `97` | FCE-REQ-POL-001/011/012/020, KRN-001/002/010, SEC-001 | Policy model v1 + rules | — | `docs/07_policy-decision-model.md` |
| M3 | S2 | `07`, `05`, `98`, `15` | FCE-REQ-POL-001/012/020, KRN-001/002/010, SEC-001 | Policy-evaluator PoC + determinism/red-team test output (EVD-M3) | GATE-B (partial) | `docs/07_policy-decision-model.md`, future PoC source/tests |
| M4 | S1 | `08`, `06` | FCE-REQ-AUD-001/002/003, EXP-001, PRV-001/002 | Audit schema v1 + replay spec | — | `docs/08_audit-record-schema.md` |
| M4 | S2 | `08`, `10`, `15` | FCE-REQ-AUD-001/002/003, EXP-001, PRV-001/002 | Audit/provenance PoC + JSONL/replay output (EVD-M4) | GATE-B (partial) | `docs/08_audit-record-schema.md`, future PoC source/tests |
| M5 | S1 | `05`, `07` | FCE-REQ-KRN-010, POL-012, OPS-002 | Fusion-kernel spec + merge model | — | `docs/05_seven-gate-data-flow.md`, `docs/07_policy-decision-model.md` |
| M5 | S2 | `07`, `10`, `98`, `15` | FCE-REQ-KRN-010, POL-012, OPS-002 | No-unauthorized-merge PoC + blocked-merge evidence (EVD-M5) | GATE-D (partial) | `docs/10_security-threat-model.md`, future PoC source/tests |
| M6 | S1 | `09`, `06`, `07` | FCE-REQ-ING-010, POL-011/012, KRN-010 | Scenario library (spec) | — | `docs/09_synthetic-dataset-plan.md` |
| M6 | S2 | `09`, `16`, `08`, `15` | FCE-REQ-ING-010, POL-012, KRN-010 | Source manifest + trim report + calibration/held-out fixture seal + coverage matrix (EVD-M6) | GATE-C | `docs/16_laptop-poc-validation-architecture.md`, future fixtures |
| M7 | S1 | `03`, `07`, `08`, `09` | all FCE-REQ-* | V&V matrix | — | new `docs/16_vv-plan.md` (proposed) |
| M7 | S2 | `98`, `10`, `11`, `15` | all FCE-REQ-*, H9 | Runnable PoC test harness + coverage report (EVD-M7) | GATE-D (partial) | new `docs/16_vv-plan.md` (proposed), future PoC tests |

Notes:
- "GATE-B (partial)" closes only when M2, M3, and M4 second sprints are all complete.
- "GATE-D (partial)" closes only when M5 no-merge PoC evidence and M7 test
  harness evidence are both present.
- The proposed `docs/16_vv-plan.md` is a new file target; create it via Claude Code
  when M7 outputs are approved (do not assume it exists yet).
