# 03 — Sprint-by-Sprint Claude Desktop Prompts

Ready-to-paste prompts for TRL 1-3 sprints M1–M7 (14 sprints). One chat per
block, one sprint per output. Sprint 1 generally locks design/spec; Sprint 2
turns that block into review evidence or minimal PoC evidence.

Corrected TRL 1-3 rule: this project is **not code-free**. After M1/GATE-A,
minimal executable PoC code is expected for schema validation, deterministic
policy evaluation, audit/provenance emission, synthetic fixtures, no-merge
behavior, and tests. Desktop may draft code/change proposals, but repo files are
written and executed only in Claude Code.

Shared guardrails (apply to every prompt below): no production or operational
code; no real/live/classified/controlled data; no real GoC markings; public
source data and synthetic data must be labelled `PUBLIC-OPEN-SOURCE`,
`SYNTHETIC-DERIVED`, or `SYNTHETIC`; no external installs unless explicitly
approved; all performance goals TARGET; no certification/ATO/endorsement/
classified-processing or measured-performance claims; keep Facts/Assumptions/
Judgment/Uncertainty labels; cite repo file paths and requirement IDs; tag every
needed repo change as `REPO-UPDATE: <file> — <change>`.
`docs/16_laptop-poc-validation-architecture.md` controls the proof method:
pre-code decisions, sealed evidence, guard tests, source trimming, and separate
held-out validation.

---

## M1 Sprint 1 — Requirements ground truth
```
Objective: Replace paraphrased outcome anchors with verbatim DND solicitation
text and draft finalized RTM rows for the FCE.
Source docs: docs/02_capability-decomposition.md, docs/03_rtm.md,
docs/00_project-context.md (OPEN-01/02).
Expected output: finalized outcome registry (verbatim + citation), RTM rows, and
acceptance criteria.
Requirement IDs: FCE-ESS-01..06, FCE-DES-01..04; all FCE-REQ-* rows.
Guardrails: do not fabricate solicitation text. Keep project taxonomy. No code
in M1. Tag repo changes REPO-UPDATE.
```

## M1 Sprint 2 — Requirements ground truth coverage audit
```
Objective: Audit outcome coverage (ESS 6/6, DES 4/4; DES-01, DES-03) and produce
a requirements-traceability review as evidence.
Source docs: docs/03_rtm.md, docs/02_capability-decomposition.md,
docs/15_trl1-3-build-plan.md.
Expected output: coverage report; gap list; verification-method assignment
review; evidence note (EVD-M1); GATE-A recommendation.
Requirement IDs: all FCE-REQ-* rows.
Guardrails: every requirement singular, testable, correctly shall/should; no
certification claims in rows. No code in M1. Tag repo changes REPO-UPDATE.
```

## M2 Sprint 1 — Data & metadata foundation design
```
Objective: Confirm and freeze the 15-field metadata schema and provenance model.
Source docs: docs/06_metadata-schema.md, docs/04_software-architecture-and-trust-boundaries.md.
Expected output: schema v1, provenance/lineage node model, validation-rule list,
and PoC file plan for schema validation.
Requirement IDs: FCE-REQ-MET-010, FCE-REQ-PRV-001, FCE-REQ-PRV-002, FCE-REQ-POL-011.
Guardrails: policy_binding_state is FCE-authority-set only (B3); fail-closed at
G2; project taxonomy only. Tag repo changes REPO-UPDATE.
```

## M2 Sprint 2 — Data & metadata foundation PoC
```
Objective: Draft the minimal schema-validation PoC and tests for Claude Code to
apply and run.
Source docs: docs/06_metadata-schema.md, docs/15_trl1-3-build-plan.md.
Expected output: REPO-UPDATE notes for local PoC schema validator, synthetic valid
object fixture, missing-field fixture, malformed fixture, source-supplied
policy_binding_state fixture, and test commands/results expected.
Requirement IDs: FCE-REQ-MET-010, FCE-REQ-PRV-001/002.
Guardrails: PoC code only; no external installs; no live operational, private,
controlled, or classified data; no production schema claims. Gate: GATE-B
(partial). Tag repo changes REPO-UPDATE.
```

## M3 Sprint 1 — Policy engine & kernel design
```
Objective: Complete the deterministic, default-deny policy model design.
Source docs: docs/07_policy-decision-model.md, docs/97_b1-b3-closure-review.md.
Expected output: PDP model, 11 actions, reason codes (incl. RC-008), PIP
authentication (B1), override envelope (B2), machine-readable policy fixture
shape, and evaluator file plan.
Requirement IDs: FCE-REQ-POL-001/011/012/020, FCE-REQ-KRN-001/002/010,
FCE-REQ-SEC-001.
Guardrails: default-deny everywhere; ties fail closed; AI advisory only. Tag
REPO-UPDATE.
```

## M3 Sprint 2 — Policy engine & kernel PoC
```
Objective: Draft the minimal deterministic policy evaluator PoC and tests for
Claude Code to apply and run.
Source docs: docs/07_policy-decision-model.md, docs/05_seven-gate-data-flow.md,
docs/98_live-gate-review.md.
Expected output: REPO-UPDATE notes for policy fixture, evaluator, deterministic
decision tests, PIP-spoof fail-closed test, default-deny test, and override
envelope test.
Requirement IDs: FCE-REQ-POL-001/012/020, FCE-REQ-KRN-001/002/010,
FCE-REQ-SEC-001.
Guardrails: enforcement deterministic; AI advisory only; no external policy
engine install unless approved. Gate: GATE-B (partial). Tag REPO-UPDATE.
```

## M4 Sprint 1 — Provenance & audit chain design
```
Objective: Complete the 18-field, hash-chained, append-only audit and export
design.
Source docs: docs/08_audit-record-schema.md, docs/06_metadata-schema.md.
Expected output: audit schema v1, 9 event classes, chain + replay spec,
export/manifest spec, and PoC audit/provenance file plan.
Requirement IDs: FCE-REQ-AUD-001/002/003, FCE-REQ-EXP-001, FCE-REQ-PRV-001/002.
Guardrails: signatures are placeholders; no production-crypto claim; audit loss
= fail-closed. Tag repo changes REPO-UPDATE.
```

## M4 Sprint 2 — Provenance & audit chain PoC
```
Objective: Draft the minimal JSONL audit/provenance PoC and replay check for
Claude Code to apply and run.
Source docs: docs/08_audit-record-schema.md, docs/10_security-threat-model.md.
Expected output: REPO-UPDATE notes for audit writer, provenance parent-link
capture, sample JSONL outputs, replay check, overflow/fail-closed handling note,
and H14 forward-link.
Requirement IDs: FCE-REQ-AUD-001/002/003, FCE-REQ-EXP-001, FCE-REQ-PRV-001/002.
Guardrails: no production crypto; hash/signature fields are PoC placeholders.
Gate: GATE-B (partial). Tag repo changes REPO-UPDATE.
```

## M5 Sprint 1 — Fusion interface & no-merge guard design
```
Objective: Complete the Fusion Compliance Kernel (G5) and no-unauthorized-merge
design.
Source docs: docs/05_seven-gate-data-flow.md, docs/07_policy-decision-model.md.
Expected output: fusion-kernel interface spec, merge decision model,
high-water-mark propagation rules, and no-merge PoC file plan.
Requirement IDs: FCE-REQ-KRN-010, FCE-REQ-POL-012, FCE-REQ-OPS-002.
Guardrails: no merge without covering permit; override cannot relax invariant
(B2). Tag REPO-UPDATE.
```

## M5 Sprint 2 — Fusion interface & no-merge guard PoC
```
Objective: Draft the minimal no-unauthorized-merge PoC and tests for Claude Code
to apply and run.
Source docs: docs/07_policy-decision-model.md, docs/10_security-threat-model.md,
docs/98_live-gate-review.md.
Expected output: REPO-UPDATE notes for merge evaluator, permitted same-domain
merge fixture, blocked cross-domain merge fixture, override-over-merge red-team
test, high-water-mark output, and audit/provenance expected output.
Requirement IDs: FCE-REQ-KRN-010, FCE-REQ-POL-012, FCE-REQ-OPS-002.
Guardrails: THR-KRN-001 remains maturity risk until stronger testing; PoC must
demonstrate at least one blocked merge. Gate: GATE-D (partial). Tag REPO-UPDATE.
```

## M6 Sprint 1 — Synthetic mission data design
```
Objective: Finalize the four synthetic scenario specifications and embedded
conflicts.
Source docs: docs/09_synthetic-dataset-plan.md, docs/16_laptop-poc-validation-architecture.md,
docs/06_metadata-schema.md, docs/07_policy-decision-model.md.
Expected output: scenario specs (Joint ISR, Maritime, Tactical Edge, UAV),
approved open-source source choices, trim protocol, calibration/held-out split
plan, expected dispositions, and fixture-file plan.
Requirement IDs: FCE-REQ-ING-010, FCE-REQ-POL-011/012, FCE-REQ-KRN-010.
Guardrails: every object labelled PUBLIC-OPEN-SOURCE, SYNTHETIC-DERIVED, or
SYNTHETIC; "-like" discipline; project taxonomy only. Tag repo changes
REPO-UPDATE.
```

## M6 Sprint 2 — Open-source-derived and synthetic mission fixtures
```
Objective: Draft source manifest, trim report, calibration fixtures, held-out
fixtures, synthetic red-team fixtures, and expected-audit tables for Claude Code
to apply.
Source docs: docs/16_laptop-poc-validation-architecture.md,
docs/09_synthetic-dataset-plan.md, docs/08_audit-record-schema.md.
Expected output: REPO-UPDATE notes for public data source manifest, trim report,
fixture files covering at least two approved source families, calibration/held-out
split, red-team variants, expected dispositions, expected audit records, fixture
seal, and coverage matrix.
Requirement IDs: FCE-REQ-ING-010, FCE-REQ-POL-012, FCE-REQ-KRN-010.
Guardrails: no real GoC markings; no real/live operational data; no policy tuning
after held-out exposure; labels verified as PUBLIC-OPEN-SOURCE,
SYNTHETIC-DERIVED, or SYNTHETIC. Gate: GATE-C. Tag REPO-UPDATE.
```

## M7 Sprint 1 — V&V and red-team planning
```
Objective: Produce the requirement-linked V&V matrix and test harness plan.
Source docs: docs/03_rtm.md, docs/07_policy-decision-model.md,
docs/08_audit-record-schema.md, docs/09_synthetic-dataset-plan.md.
Expected output: bidirectional V&V matrix across unit/integration/property-style/
explainability/red-team classes and test-harness file plan.
Requirement IDs: all FCE-REQ-*.
Guardrails: every requirement mapped to >=1 planned or executed test. Tag
REPO-UPDATE.
```

## M7 Sprint 2 — V&V and red-team PoC evidence
```
Objective: Draft/run-plan the local PoC validation harness in two layers: code
correctness tests and held-out laptop concept validation. Cover B1/B2/B3,
no-bypass, no-merge, default-deny, audit emission, provenance parent linkage,
and every guard in docs/16.
Source docs: docs/16_laptop-poc-validation-architecture.md,
docs/98_live-gate-review.md, docs/10_security-threat-model.md,
docs/11_failure-modes-and-mitigations.md.
Expected output: REPO-UPDATE notes for runnable test harness, guard rejection
tests, code-correctness report, held-out validation report, source/trim evidence,
coverage report, and evidence IDs. If Claude Code has run the tests, summarize
actual results; otherwise mark results as planned.
Requirement IDs: all FCE-REQ-*; H9.
Guardrails: no expected result depends solely on AI output; public-source and
synthetic fixtures only; report negative held-out results verbatim. Gate: GATE-D
(partial). Tag REPO-UPDATE.
```
