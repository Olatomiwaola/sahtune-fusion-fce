# 03 — Requirements Traceability Matrix (RTM) v0 (draft)

Owner: `requirements-traceability-engineer`. Skill: `fce-requirements-traceability`.

## Status of source wording [OPEN-01]

Source outcomes use the paraphrased anchors in `02`. These are NOT verbatim DND
IDEaS wording. Replace with quoted solicitation text before RTM is final. No
verbatim text is fabricated here.

## Verification method legend

inspection, analysis, simulation, unit test, integration test, property-based
test, red-team test, benchmark, bench test, field test, flight test,
accreditation-support review.

Status values: draft (all rows at v0). "shall" = binding; "should" = desired.

## RTM rows

### FCE-ESS-01 — AI-enabled enforcement during fusion

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-KRN-001 | The FCE shall render a recorded policy decision for every object before that object is released to downstream analytics. | FCE-ESS-01 | CAP-02 | ARCH-03, ARCH-04, G4 | integration test, property-based test | TST-INT-001 / EVD-001 | draft |
| FCE-REQ-POL-001 | The FCE shall render policy decisions deterministically, such that identical inputs under identical policy-bundle version yield identical decisions. | FCE-ESS-01 | CAP-02 | ARCH-03 | property-based test | TST-PRP-001 | draft |
| FCE-REQ-KRN-002 | AI components shall be advisory only; no enforcement decision shall depend solely on AI output, and every decision shall cite at least one deterministic rule ID. | FCE-ESS-01 | CAP-07 | ARCH-08 | inspection, red-team test | TST-RED-001 | draft |

### FCE-ESS-02 — Enforcement across modalities, domain, and handling level

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-ING-010 | The FCE shall ingest and enforce policy on at least two sensor modalities. | FCE-ESS-02 | CAP-01 | ARCH-01, G1 | integration test | TST-INT-010 | draft |
| FCE-REQ-POL-011 | The FCE shall represent at least one network security domain and a handling level equivalent to the Protected B target using the project taxonomy, never real Government of Canada markings. | FCE-ESS-02 | CAP-03 | ARCH-03, ARCH-07 | analysis, unit test | TST-UNT-011 | draft |
| FCE-REQ-MET-010 | The FCE shall bind machine-readable classification, domain, and release-caveat metadata to every ingested object, rejecting objects that lack mandatory fields. | FCE-ESS-02 | CAP-01 | ARCH-02, G2 | unit test | TST-UNT-010 | draft |

### FCE-ESS-03 — Programmatic checks without human approval for predefined conditions

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-KRN-010 | The FCE shall perform compliance checks at ingestion and at fusion and shall auto-disposition predefined policy conditions without human approval. | FCE-ESS-03 | CAP-02 | ARCH-04, G4, G5 | integration test | TST-INT-011 | draft |
| FCE-REQ-POL-012 | The FCE shall default-deny and fail closed when a condition is not predefined or is ambiguous, enqueuing the object for human review. | FCE-ESS-03 | CAP-02 | ARCH-03 | property-based test, red-team test | TST-PRP-012 | draft |

### FCE-ESS-04 — Provenance for all ingested and produced data

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-PRV-001 | The FCE shall record provenance for every ingested and produced object, including source sensor ID, classification markings, timestamps, and domain of origin. | FCE-ESS-04 | CAP-04 | ARCH-09 | unit test, integration test | TST-INT-040 | draft |
| FCE-REQ-PRV-002 | The FCE shall preserve provenance across transformation and fusion by linking each derived object to all parent objects. | FCE-ESS-04 | CAP-04 | ARCH-09, ARCH-07 | property-based test | TST-PRP-040 | draft |

### FCE-ESS-05 — Audit logs of rules, actions, and dispositions

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-AUD-001 | The FCE shall emit an audit record for every policy decision documenting the policy rule IDs applied, the enforcement action taken, and the resulting disposition. | FCE-ESS-05 | CAP-05 | ARCH-10, G7 | integration test, inspection | TST-INT-050 | draft |
| FCE-REQ-AUD-002 | The audit chain shall be append-only and tamper-evident, with each record binding the previous record's hash. | FCE-ESS-05 | CAP-05 | ARCH-10 | property-based test, red-team test | TST-RED-050 | draft |

### FCE-ESS-06 — Exportable lineage records

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-EXP-001 | The FCE shall export audit and lineage records in a documented format accompanied by an integrity manifest supporting compliance review, forensic analysis, and accreditation-support review. | FCE-ESS-06 | CAP-08 | ARCH-11 | integration test | TST-INT-060 | draft |
| FCE-REQ-AUD-003 | The FCE shall make the decision sequence deterministically reconstructible (replayable) from audit records alone. | FCE-ESS-06 | CAP-05 | ARCH-10 | integration test, analysis | TST-INT-061 | draft |

### FCE-DES-01 — Real-time enforcement at tactical latency (desired)

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-EDG-001 | The FCE should meet an internal end-to-end latency TARGET across multiple modalities and handling levels under a defined synthetic workload on named hardware. All figures are internal targets to be verified. | FCE-DES-01 | CAP-09 | ARCH-12, all gates | benchmark | TST-PRF-001 / EVD-BENCH-001 | draft |

### FCE-DES-02 — Adaptable policy framework without restart (desired)

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-POL-020 | The FCE should load signed policy-bundle updates (classification guides, release authorities, coalition caveats, operational rules) without system restart, with version pinning and rollback, rejecting invalid or unsigned bundles fail-closed. | FCE-DES-02 | CAP-11 | ARCH-05 | integration test, red-team test | TST-RED-020 | draft |

### FCE-DES-03 — SWaP and compute limits at the edge (desired)

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-EDG-010 | The FCE should operate within defined SWaP and compute limits on a named edge-class device and shall fail closed under resource exhaustion across all six degraded-mode constraint classes. | FCE-DES-03 | CAP-09 | ARCH-12 | benchmark, edge/degraded test | TST-EDG-010 | draft |

### FCE-DES-04 — Explainability and controlled override (desired)

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-OPS-001 | The FCE should present a human-readable explanation for each decision, including the rules applied, the attributes consumed, and the reason code. | FCE-DES-04 | CAP-10 | ARCH-13 | explainability test | TST-EXP-001 | draft |
| FCE-REQ-OPS-002 | Operator override shall require authenticated authority, a reason code, a time limit, and an audit signature placeholder; override lacking any precondition shall be rejected fail-closed. | FCE-DES-04 | CAP-10 | ARCH-13, ARCH-10 | red-team test, integration test | TST-RED-002 | draft |

### Cross-cutting security

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| FCE-REQ-SEC-001 | The FCE shall enforce zero-trust authentication and authorization on every service-to-service and operator interface; unauthenticated or unauthorized requests shall be denied fail-closed. | FCE-ESS-01, FCE-ESS-02 | CAP-02 | all ARCH | red-team test, inspection | TST-RED-SEC-001 | draft |

## Coverage

Essential: 6/6 (ESS-01…06 all have >= 1 shall). Desired: 4/4 (DES-01…04;
DES-01 and DES-03 confirmed present). Gaps: none at outcome level. Every row has
an ID, a verification method, and a design-element trace.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: requirement IDs, verification-method assignments, capability and
  element traces.
- Assumptions: anchors approximate final wording; acceptance thresholds for
  latency and SWaP are placeholders (TARGET) pending named hardware.
- Judgment: decomposition granularity (one testable statement per row).
- Uncertainty: verbatim wording (OPEN-01) may add or split rows.
