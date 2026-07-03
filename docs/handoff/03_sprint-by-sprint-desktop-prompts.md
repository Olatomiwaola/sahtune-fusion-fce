# 03 — Sprint-by-Sprint Claude Desktop Prompts

Ready-to-paste prompts for TRL 1-3 sprints M1–M7 (14 sprints). One chat per
block, one sprint per output. Sprint 1 = design/spec artifact; Sprint 2 =
analysis/review/evidence artifact. No code at TRL 1-3.

Shared guardrails (apply to every prompt below): docs-only; no source code; no
installs; project taxonomy only (no real GoC markings); synthetic data labelled
SYNTHETIC; all performance goals TARGET; no certification/ATO/endorsement/
classified-processing/measured-performance claims; keep Facts/Assumptions/
Judgment/Uncertainty labels; cite repo file paths and requirement IDs; tag every
needed repo change as `REPO-UPDATE: <file> — <change>`.

---

## M1 Sprint 1 — Requirements ground truth (design/spec)
```
Objective: Replace the paraphrased outcome anchors with verbatim DND solicitation
text and draft finalized RTM rows for the FCE.
Source docs: docs/02_capability-decomposition.md, docs/03_rtm.md,
docs/00_project-context.md (OPEN-01/02).
Expected output: draft finalized outcome registry (verbatim + citation) and RTM
rows; note any wording that changes a mapping.
Requirement IDs: FCE-ESS-01..06, FCE-DES-01..04; all FCE-REQ-* rows.
Guardrails: do not fabricate solicitation text — if verbatim text is not provided,
stop and request it. Keep project taxonomy. Tag repo changes REPO-UPDATE.
```

## M1 Sprint 2 — Requirements ground truth (analysis/review/evidence)
```
Objective: Audit outcome coverage (ESS 6/6, DES 4/4; DES-01, DES-03) and produce a
requirements-traceability review as evidence.
Source docs: docs/03_rtm.md, docs/02_capability-decomposition.md.
Expected output: coverage report; gap list; verification-method assignment review;
evidence note (EVD-*).
Requirement IDs: all FCE-REQ-* rows.
Guardrails: every requirement singular, testable, correctly shall/should; no
certification claims in rows. Gate: GATE-A. Tag repo changes REPO-UPDATE.
```

## M2 Sprint 1 — Data & metadata foundation (design/spec)
```
Objective: Confirm and freeze the 15-field metadata schema and provenance model.
Source docs: docs/06_metadata-schema.md, docs/04_software-architecture-and-trust-boundaries.md.
Expected output: schema v1 (design), provenance/lineage node model, validation-rule list.
Requirement IDs: FCE-REQ-MET-010, FCE-REQ-PRV-001, FCE-REQ-PRV-002, FCE-REQ-POL-011.
Guardrails: policy_binding_state is FCE-authority-set only (B3); fail-closed at G2;
project taxonomy only. Tag repo changes REPO-UPDATE.
```

## M2 Sprint 2 — Data & metadata foundation (analysis/review/evidence)
```
Objective: Review the schema and provenance model; capture a schema-freeze decision record.
Source docs: docs/06_metadata-schema.md, docs/09_synthetic-dataset-plan.md.
Expected output: data-model review; high-water-mark propagation analysis; DR for schema freeze (EVD-*).
Requirement IDs: FCE-REQ-MET-010, FCE-REQ-PRV-001/002.
Guardrails: no code; note any coalition-caveat sub-field gaps. Gate: GATE-B (partial).
Tag repo changes REPO-UPDATE.
```

## M3 Sprint 1 — Policy engine & kernel (design/spec)
```
Objective: Complete the deterministic, default-deny policy model design.
Source docs: docs/07_policy-decision-model.md, docs/97_b1-b3-closure-review.md.
Expected output: PDP model, 11 actions, reason codes (incl. RC-008), PIP authentication (B1),
override envelope (B2), Rego-style example rules with unit-test descriptions.
Requirement IDs: FCE-REQ-POL-001/011/012/020, FCE-REQ-KRN-001/002/010, FCE-REQ-SEC-001.
Guardrails: default-deny everywhere; ties fail closed; no implementation code. Tag REPO-UPDATE.
```

## M3 Sprint 2 — Policy engine & kernel (analysis/review/evidence)
```
Objective: Analyse determinism and review the policy path for security.
Source docs: docs/07_policy-decision-model.md, docs/05_seven-gate-data-flow.md, docs/98_live-gate-review.md.
Expected output: determinism analysis; conflict-resolution walkthrough; secure-architecture
review report; property-based and red-team test descriptions.
Requirement IDs: FCE-REQ-POL-001/012, FCE-REQ-KRN-001/002/010.
Guardrails: enforcement deterministic; AI advisory only. Gate: GATE-B (partial). Tag REPO-UPDATE.
```

## M4 Sprint 1 — Provenance & audit chain (design/spec)
```
Objective: Complete the 18-field, hash-chained, append-only audit and export design.
Source docs: docs/08_audit-record-schema.md, docs/06_metadata-schema.md.
Expected output: audit schema v1, 9 event classes, chain + replay spec, export/manifest spec.
Requirement IDs: FCE-REQ-AUD-001/002/003, FCE-REQ-EXP-001, FCE-REQ-PRV-001/002.
Guardrails: signatures are placeholders (no crypto-cert claim); audit loss = fail-closed.
Tag repo changes REPO-UPDATE.
```

## M4 Sprint 2 — Provenance & audit chain (analysis/review/evidence)
```
Objective: Analyse replay determinism and overflow behaviour; review the audit design.
Source docs: docs/08_audit-record-schema.md, docs/10_security-threat-model.md.
Expected output: replay-determinism analysis; overflow fail-closed review; review report (EVD-*);
note H14 (unauthenticated-rejection audit) forward-link.
Requirement IDs: FCE-REQ-AUD-001/002/003, FCE-REQ-EXP-001.
Guardrails: no production-crypto claim. Gate: GATE-B (partial). Tag repo changes REPO-UPDATE.
```

## M5 Sprint 1 — Fusion interface & no-merge guard (design/spec)
```
Objective: Complete the Fusion Compliance Kernel (G5) and no-unauthorized-merge design.
Source docs: docs/05_seven-gate-data-flow.md, docs/07_policy-decision-model.md.
Expected output: fusion-kernel interface spec, merge decision model, high-water-mark propagation rules.
Requirement IDs: FCE-REQ-KRN-010, FCE-REQ-POL-012, FCE-REQ-OPS-002.
Guardrails: no merge without covering permit; override cannot relax invariant (B2). Tag REPO-UPDATE.
```

## M5 Sprint 2 — Fusion interface & no-merge guard (analysis/review/evidence)
```
Objective: Walk through the invariant and override-envelope interaction; design red-team tests.
Source docs: docs/07_policy-decision-model.md, docs/10_security-threat-model.md, docs/98_live-gate-review.md.
Expected output: invariant analysis; sole-fusion-authority note (H1 forward-link); property-based and
red-team test descriptions (forced merge, override-over-merge).
Requirement IDs: FCE-REQ-KRN-010, FCE-REQ-OPS-002.
Guardrails: THR-KRN-001 stays blocking-until-verified (H9, TRL 4-5). Gate: GATE-D (partial). Tag REPO-UPDATE.
```

## M6 Sprint 1 — Synthetic mission data (design/spec)
```
Objective: Finalize the four synthetic scenario specifications and embedded conflicts.
Source docs: docs/09_synthetic-dataset-plan.md, docs/06_metadata-schema.md, docs/07_policy-decision-model.md.
Expected output: scenario specs (Joint ISR, Maritime, Tactical Edge, UAV) with expected dispositions.
Requirement IDs: FCE-REQ-ING-010, FCE-REQ-POL-011/012, FCE-REQ-KRN-010.
Guardrails: every object labelled SYNTHETIC; "-like" discipline; project taxonomy; specification only
(no data generated). Tag repo changes REPO-UPDATE.
```

## M6 Sprint 2 — Synthetic mission data (analysis/review/evidence)
```
Objective: Add red-team variants and expected audit records; review labelling and coverage.
Source docs: docs/09_synthetic-dataset-plan.md, docs/08_audit-record-schema.md.
Expected output: red-team data specs; expected-audit tables; coverage matrix (every gate/action exercised).
Requirement IDs: FCE-REQ-POL-012, FCE-REQ-KRN-010.
Guardrails: no real GoC markings; SYNTHETIC labelling verified. Gate: GATE-C. Tag repo changes REPO-UPDATE.
```

## M7 Sprint 1 — V&V and red-team planning (design/spec)
```
Objective: Produce the requirement-linked V&V test matrix (descriptions only).
Source docs: docs/03_rtm.md, docs/07_policy-decision-model.md, docs/08_audit-record-schema.md, docs/09_synthetic-dataset-plan.md.
Expected output: bidirectional V&V matrix across unit/integration/property-based/explainability classes.
Requirement IDs: all FCE-REQ-* (verification coverage).
Guardrails: test descriptions only, no code; every requirement mapped to >=1 test. Tag repo changes REPO-UPDATE.
```

## M7 Sprint 2 — V&V and red-team planning (analysis/review/evidence)
```
Objective: Design the red-team suite (10 categories incl. B1/B2/B3, no-bypass, no-merge) and coverage report.
Source docs: docs/98_live-gate-review.md, docs/10_security-threat-model.md, docs/11_failure-modes-and-mitigations.md.
Expected output: red-team test specs; fail-closed cases per gate; coverage report (n/total, named gaps).
Requirement IDs: all FCE-REQ-*; H9 (demonstrate B1-B3, no-bypass, no-merge).
Guardrails: no expected result depends solely on AI output; synthetic-first. Gate: GATE-D (partial). Tag REPO-UPDATE.
```
