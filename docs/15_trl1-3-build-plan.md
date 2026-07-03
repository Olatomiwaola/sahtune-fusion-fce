# 15 — TRL 1-3 Build Plan

Owner: `fce-lead-systems-architect` with `trl-evidence-engineer`.
Source of truth: `docs/00`–`14`, `97`, `98`. Scope is **TRL 1-3 only**
(basic principles -> analytical and experimental proof of concept).

## Corrected TRL 1-3 rule

TRL 1-3 is **not production-code development**, but it is also **not code-free**
for this challenge. Because the FCE challenge asks for programmatic compliance
checks, machine-readable policy enforcement, provenance records, audit logs, and
traceable export records, TRL 3 should include a small executable software PoC.

Permitted in TRL 1-3:
- Minimal PoC code for schema validation, policy evaluation, seven-gate flow,
  provenance capture, audit-log emission, synthetic input generation, and
  no-unauthorized-merge demonstration.
- Synthetic/mock data only, clearly labelled `SYNTHETIC`.
- Local unit/integration/property-style tests that demonstrate feasibility.
- Sample machine-readable outputs: JSON objects, JSONL audit logs, manifests,
  and coverage reports.

Not permitted in TRL 1-3:
- Production, operational, classified-processing, or deployed code.
- Real DND/CAF data, live operational data, controlled data, or real GoC
  markings.
- External installs, NVIDIA components, cloud services, MCP connectors, or
  vendor dependencies unless explicitly approved.
- Production cryptography, formal accreditation, ATO, endorsement, or measured
  performance claims.

All performance goals remain TARGET until measured on named hardware with
provenance. B1-B3 are closed-in-text (`97`); H1-H14 are open maturity items
(`98`).

## Blocks in scope

M1 Requirements and Solicitation Ground Truth · M2 Data and Metadata Foundation ·
M3 Policy Engine and Compliance Kernel · M4 Provenance and Audit Chain ·
M5 Fusion Interface and No-Merge Guard · M6 Synthetic Mission Data and
Simulation · M7 Verification and Red-Team Test Harness.

Code begins only after M1 locks the RTM sufficiently for the affected block.
The PoC should stay deliberately small: a local executable path that proves the
critical functions, not a platform.

---

## M1 — Requirements and Solicitation Ground Truth
1. Objective: lock the outcome registry and RTM against verbatim solicitation
   text.
2. TRL 1-3 purpose: establish the requirement baseline every PoC module traces
   to.
3. Sprint 1: quote verbatim solicitation; replace anchors in `02`/`03`; draft
   finalized RTM rows and acceptance criteria.
4. Sprint 2: coverage audit (ESS 6/6, DES 4/4; DES-01/DES-03 present);
   requirements-traceability review; capture coverage report as evidence.
5. Artifacts to create: finalized RTM (`03` update), outcome-to-capability map,
   coverage report.
6. Code status: no PoC code in M1; requirements must lead implementation.
7. Evidence to capture: EVD-M1 coverage report, RTM baseline, citation list.
8. Definition of done: every outcome quoted + cited; every requirement has ID,
   verification method, acceptance criterion; no unsupported claim in any row.
9. Requirement IDs touched: FCE-ESS-01…06, FCE-DES-01…04; all FCE-REQ-* rows.
10. Dependencies: none.
11. Risks: later solicitation amendment changes the RTM.
12. Exit gate: GATE-A (requirements locked).

## M2 — Data and Metadata Foundation
1. Objective: freeze the 15-field object metadata schema and create the PoC
   validation contract.
2. TRL 1-3 purpose: provide the stable data contract that policy, audit, fusion,
   and tests consume.
3. Sprint 1: confirm 15-field schema (`06`), taxonomy mapping approach
   (OPEN-02), B3 authority-set binding-state rule, and fail-closed validation
   behavior at G2.
4. Sprint 2: implement a minimal local schema-validation PoC and tests for valid
   object, missing mandatory field, malformed metadata, and source-supplied
   `policy_binding_state`.
5. Artifacts to create: schema v1, provenance model spec, validation-rule list,
   schema-validation PoC, schema test results.
6. PoC output examples: accepted object JSON, rejected object JSON, validation
   error reason code, G2 quarantine disposition.
7. Evidence to capture: EVD-M2 schema-freeze DR, validation test output,
   provenance model.
8. Definition of done: mandatory-field rejection works in the PoC;
   `policy_binding_state` is forced to `unvalidated` at G1/G2 boundary;
   provenance covers FCE-ESS-04.
9. Requirement IDs touched: FCE-REQ-MET-010, FCE-REQ-PRV-001/002,
   FCE-REQ-POL-011.
10. Dependencies: M1.
11. Risks: coalition caveat sub-fields may require schema extension.
12. Exit gate: contributes to GATE-B.

## M3 — Policy Engine and Compliance Kernel
1. Objective: implement a minimal deterministic policy evaluator for PoC use.
2. TRL 1-3 purpose: prove default-deny, deterministic policy enforcement, B1
   PIP-attribute handling, and B2 override envelope at software-feasibility
   level.
3. Sprint 1: finalize PDP/PEP/PAP/PIP model, 11 actions, reason codes
   including RC-008, deny-overrides, and rule examples.
4. Sprint 2: implement a small machine-readable policy file and local evaluator
   that returns permit/restrict/block/quarantine/review decisions for synthetic
   objects.
5. Artifacts to create: policy model v1, policy fixture, evaluator PoC,
   determinism tests, PIP-auth failure tests, override-envelope tests.
6. PoC output examples: decision JSON with rule ID, action, disposition, reason
   code, policy bundle version.
7. Evidence to capture: EVD-M3 policy review report, deterministic replay of
   identical input, red-team test notes for PIP spoofing and override abuse.
8. Definition of done: identical inputs produce identical decisions; ambiguous
   or unverifiable attributes fail closed; override cannot create a permit or
   relax a G5 block.
9. Requirement IDs touched: FCE-REQ-POL-001/011/012/020,
   FCE-REQ-KRN-001/002/010, FCE-REQ-SEC-001.
10. Dependencies: M1, M2.
11. Risks: policy model becomes too broad for a minimal PoC; keep rules narrow.
12. Exit gate: contributes to GATE-B.

## M4 — Provenance and Audit Chain
1. Objective: implement minimal provenance and audit-log emission for PoC
   decisions.
2. TRL 1-3 purpose: prove each decision can emit traceable, replayable evidence
   at PoC scale.
3. Sprint 1: finalize 18-field audit schema (`08`), 9 event classes, chain
   semantics, replay fields, and export/manifest shape.
4. Sprint 2: implement local JSONL audit emission and provenance parent-link
   capture for accepted, rejected, transformed, and fused synthetic objects.
5. Artifacts to create: audit schema v1, provenance model, audit writer PoC,
   sample JSONL audit log, sample lineage export, replay-check test.
6. PoC output examples: audit event JSONL, provenance node JSON, simple
   integrity manifest placeholder.
7. Evidence to capture: EVD-M4 audit review report, replay analysis, chain
   integrity test output.
8. Definition of done: each PoC decision has an audit event; derived/fused
   objects link to parents; audit-loss path is specified as fail-closed.
9. Requirement IDs touched: FCE-REQ-AUD-001/002/003, FCE-REQ-EXP-001,
   FCE-REQ-PRV-001/002.
10. Dependencies: M2, M3.
11. Risks: production crypto is out of scope; hash/signature fields remain PoC
   placeholders until H6 matures.
12. Exit gate: contributes to GATE-B.

## M5 — Fusion Interface and No-Merge Guard
1. Objective: implement a minimal no-unauthorized-merge PoC around synthetic
   multi-sensor inputs.
2. TRL 1-3 purpose: prove the core FCE differentiator: fusion cannot combine
   inputs unless the active policy explicitly permits the combined
   classification/domain/caveat tuple.
3. Sprint 1: finalize high-water-mark propagation, explicit-permit merge check,
   segregation-on-block, and fusion-kernel interface.
4. Sprint 2: implement local merge evaluation over two or more synthetic parent
   objects, including permitted same-domain merge and blocked cross-domain merge.
5. Artifacts to create: fusion-kernel PoC, merge decision model, propagation
   rules, invariant analysis, blocked-merge audit examples.
6. PoC output examples: fused object with parent links and high-water mark;
   blocked merge with RC-003 and segregated inputs.
7. Evidence to capture: EVD-M5 invariant analysis, no-merge test output,
   forced-merge red-team notes.
8. Definition of done: no merge without covering permit; override cannot relax
   the invariant; derived objects carry high-water-mark labels and parent links.
9. Requirement IDs touched: FCE-REQ-KRN-010, FCE-REQ-POL-012,
   FCE-REQ-OPS-002.
10. Dependencies: M3, M4.
11. Risks: THR-KRN-001 remains blocking-until-verified until stronger tests in
   later maturity.
12. Exit gate: contributes to GATE-D.

## M6 — Synthetic Mission Data and Simulation
1. Objective: create synthetic/mock inputs that drive the PoC through every
   gate and main policy action.
2. TRL 1-3 purpose: compensate for the challenge’s no-DND-data condition by
   producing controlled synthetic fixtures and expected dispositions.
3. Sprint 1: finalize scenario specs (Joint ISR, Maritime, Tactical Edge, UAV)
   with embedded metadata conflicts.
4. Sprint 2: create local synthetic fixture files for at least two modalities
   and red-team variants: missing metadata, stale timestamp, PIP spoofing,
   source-supplied binding state, and unauthorized merge attempt.
5. Artifacts to create: scenario library, synthetic fixture set, expected
   decision table, expected audit-record table.
6. PoC output examples: `SYNTHETIC` input objects, expected disposition matrix,
   generated audit/provenance examples.
7. Evidence to capture: EVD-M6 scenario specs, fixture manifest, coverage matrix,
   labelling review.
8. Definition of done: every object is labelled `SYNTHETIC`; every gate and
   policy action is exercised; project taxonomy only.
9. Requirement IDs touched: FCE-REQ-ING-010, FCE-REQ-POL-011/012,
   FCE-REQ-KRN-010.
10. Dependencies: M2, M3.
11. Risks: unrepresentative scenarios (THR-SIM-001) give false confidence.
12. Exit gate: GATE-C.

## M7 — Verification and Red-Team Test Harness
1. Objective: run the local PoC through requirement-linked tests and produce
   evidence, not just test descriptions.
2. TRL 1-3 purpose: close the requirement-to-evidence loop for analytical and
   experimental PoC feasibility.
3. Sprint 1: finalize V&V matrix across unit, integration, property-style,
   explainability, and red-team classes.
4. Sprint 2: implement/run a minimal local test harness covering B1/B2/B3,
   no-bypass, no-unauthorized-merge, default-deny, audit emission, and
   provenance parent linkage.
5. Artifacts to create: V&V matrix, red-team test specs, runnable PoC test
   harness, coverage report, sample test output.
6. PoC output examples: test summary, failed/passed cases, coverage matrix,
   sample audit/provenance files from test runs.
7. Evidence to capture: EVD-M7 test output, red-team notes, coverage report.
8. Definition of done: every requirement has at least one planned or executed
   test; core PoC tests execute locally; no expected result depends solely on
   AI output.
9. Requirement IDs touched: all FCE-REQ-*.
10. Dependencies: M3, M4, M5, M6.
11. Risks: untestable requirements return to M1; live/real data remains
   disallowed.
12. Exit gate: contributes to GATE-D.

---

## TRL 1-3 Master Schedule

| Block | Sprint | Objective | Output | Review gate |
|---|---|---|---|---|
| M1 | S1 | Quote solicitation; draft finalized RTM | RTM rows with acceptance criteria | — |
| M1 | S2 | Coverage audit + traceability review | Coverage report | GATE-A |
| M2 | S1 | Freeze 15-field schema + provenance | Schema v1 | — |
| M2 | S2 | Implement schema-validation PoC | Validation tests + sample outputs | GATE-B (partial) |
| M3 | S1 | Policy model + PIP-auth (B1) + override envelope (B2) | Policy model v1 | — |
| M3 | S2 | Implement deterministic policy evaluator PoC | Policy decisions + tests | GATE-B (partial) |
| M4 | S1 | 18-field audit + chain + replay design | Audit schema v1 | — |
| M4 | S2 | Implement audit/provenance PoC | JSONL audit + replay check | GATE-B (partial) |
| M5 | S1 | Fusion kernel + no-merge design | Fusion-kernel spec | — |
| M5 | S2 | Implement no-unauthorized-merge PoC | Permitted/blocked merge evidence | GATE-D (partial) |
| M6 | S1 | Four scenario specs | Scenario library spec | — |
| M6 | S2 | Create synthetic fixture set | Fixture manifest + coverage matrix | GATE-C |
| M7 | S1 | V&V matrix | Requirement-linked test plan | — |
| M7 | S2 | Run minimal PoC test harness | Test output + coverage report | GATE-D (partial) |

GATE-B closes only when M2, M3, and M4 second sprints are all complete and
coherent. GATE-D closes only when M5 and M7 PoC evidence are both present.

## TRL 1-3 PoC boundary

The PoC is a local technical feasibility artifact. It should prove:
- at least two synthetic modalities can enter the pipeline;
- metadata is validated and fail-closed;
- policy decisions are deterministic and default-deny;
- provenance and audit records are emitted;
- unauthorized merge attempts are blocked and audited;
- B1, B2, and B3 failure cases are represented in tests.

The PoC does **not** prove:
- operational deployment;
- classified or controlled-data processing authority;
- production crypto;
- tactical latency on named hardware;
- accreditation, ATO, certification, or endorsement;
- integration with real CAF/DND systems.

## What is intentionally deferred

Deferred beyond TRL 1-3 or requiring explicit approval:
- Production architecture hardening and operational deployment.
- Real sensor adapters or live sensor integrations.
- Real DND/CAF-provided data or any live, operational, controlled, or classified
  data.
- External dependency installation, NVIDIA component installation, or hardware
  benchmark rig setup.
- Field or flight testing.
- Formal accreditation, certification, ATO, endorsement, or government approval
  claims.
- Production cryptography, secure boot, key management, and external audit-chain
  anchoring (H6/H10/H11 maturity work).
- Measured latency/SWaP claims on named hardware.

## Decision gates before TRL 4-5

All of the following must be satisfied before TRL 4-5 execution begins:
- Solicitation text finalized (verbatim, cited) — OPEN-01 resolved for M1
  Sprint 1; Sprint 2 coverage audit still required.
- RTM finalized (6/6 Essential, 4/4 Desired; every row testable).
- Schema frozen and schema-validation PoC evidence captured.
- Policy model reviewed and policy-evaluator PoC evidence captured.
- Audit model reviewed and audit/provenance PoC evidence captured.
- Synthetic fixture set approved (every gate/action exercised; `SYNTHETIC`
  labelled).
- V&V plan approved and minimal PoC test harness executed.
- B1-B3 closed in text (`97`) and represented in PoC tests; stronger test
  closure remains tracked under H9.
- H1-H14 triaged (owners and target band assigned; blocking items identified).
- No unsupported claims (red-team claim audit clean; no prohibited vocabulary).

## Facts / Assumptions / Judgment / Uncertainty

- Facts: Canada TRL Level 3 includes analytical and/or laboratory
  proof-of-concept work; FCE essential outcomes are programmatic software
  functions.
- Assumptions: minimal local PoC code can be built without external installs and
  without real data.
- Judgment: the sprint split now treats M1 as requirements lock and M2-M7 as
  design plus executable PoC evidence.
- Uncertainty: exact implementation language, directory structure, and test
  runner remain to be selected by the build agent after GATE-A.
