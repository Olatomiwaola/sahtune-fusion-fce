# 03 — Requirements Traceability Matrix (RTM) v0.3 (M3 Sprint 5: FCE-REQ-SEC-002 added; v0.2 = M1 Sprint 2 corrections RU-02..RU-04 per EVD-M1)

Owner: `requirements-traceability-engineer`. Skill: `fce-requirements-traceability`.

## Status of source wording [OPEN-01 resolved for Sprint 1]

Source outcomes now use verified verbatim DND IDEaS outcome text from the
Canada.ca challenge page. Solicitation identifier W7714-248676/014 is treated
as verified by Kanatir. The Canada.ca page remains the cited outcome source for
this RTM.

Source: Canada.ca, "Reliable AI sensor fusion for real world missions",
Defence IDEaS Competitive Projects,
https://www.canada.ca/en/department-national-defence/programs/defence-ideas/element/competitive-projects/challenges/reliable-ai-sensor-fusion-for-real-world-missions.html.

M1 Sprint 1 does not declare GATE-A. GATE-A still requires M1 Sprint 2 coverage
audit and review.

## Verbatim outcome registry

### Essential outcomes
- FCE-ESS-01: Develop a modular AI-enabled component that automatically
  enforces classification rules and policy constraints during multi-sensor (at
  least two) data fusion operations.
- FCE-ESS-02: Apply enforcement controls based on machine-readable policy
  definitions across multiple sensor modalities (at least two), security
  domains (at least Network security), and classification levels (at least
  Protected B level).
- FCE-ESS-03: Execute compliance checks and enforcement actions
  programmatically during data ingestion and fusion processing, without
  requiring human approval for predefined policy conditions.
- FCE-ESS-04: Generate and retain provenance records for all data ingested into
  and produced by the fusion pipeline including source sensor identification,
  classification markings, timestamps, and domain of origin.
- FCE-ESS-05: Produce audit logs documenting policy rules applied during fusion
  processing, enforcement actions taken (e.g., permit, restrict, downgrade,
  segregate) and resulting compliance dispositions.
- FCE-ESS-06: Produce audit records that support traceability of data lineage
  from original ingestion through fusion output and are exportable for
  compliance review, forensic analysis, or accreditation activities.

### Desired outcomes
- FCE-DES-01: Real-time compliance enforcement across multiple sensor
  modalities (at least two) and classification levels, with performance
  suitable for tactical decision-making.
- FCE-DES-02: Adaptable policy framework that allows compliance rules (e.g.
  classification guides, release authorities, coalition-specific caveats) to be
  updated or reconfigured without system restart, supporting rapid transition
  between operational contexts.
- FCE-DES-03: Incorporate Size/Weight/Power (SWaP) and compute limits into
  fusion pipelines for edge deployment and capable of maintaining compliance
  enforcement.
- FCE-DES-04: Explainability and operator trust mechanisms, including
  human-readable compliance decisions and controlled override capabilities with
  appropriate accountability safeguards.

## Verification method legend

inspection, analysis, simulation, unit test, integration test, property-based
test, red-team test, benchmark, bench test, field test, flight test,
accreditation-support review.

Status values: `draft` for M1 Sprint 1. "shall" = binding; "should" = desired.
Convention (N-03, EVD-M1): fail-closed and safeguard clauses attached to
Desired-outcome capabilities are conditional-binding — binding whenever the
capability is present (applies to FCE-REQ-POL-020, FCE-REQ-OPS-002,
FCE-REQ-EDG-011).
Acceptance criteria are drafted for traceability and will be audited in M1
Sprint 2.

## RTM rows

### FCE-ESS-01 — AI-enabled enforcement during fusion

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-KRN-001 | The FCE shall render a recorded policy decision for every object before that object is released to downstream analytics. | FCE-ESS-01 | CAP-02 | ARCH-03, ARCH-04, G4 | integration test, property-based test | Every object has a policy decision before downstream release; any object without a recorded decision is blocked from release and produces an audit event. | TST-INT-001 / EVD-001 | draft |
| FCE-REQ-POL-001 | The FCE shall render policy decisions deterministically, such that identical inputs under identical policy-bundle version yield identical decisions. | FCE-ESS-01 | CAP-02 | ARCH-03 | property-based test | Repeated evaluation of identical object, PIP attributes, and policy bundle version produces the same decision, reason code, and enforcement action. | TST-PRP-001 | draft |
| FCE-REQ-KRN-002 | AI components shall be advisory only; no enforcement decision shall depend solely on AI output, and every decision shall cite at least one deterministic rule ID. | FCE-ESS-01 | CAP-07 | ARCH-08 | inspection, red-team test | Each enforcement decision cites deterministic rule ID(s); disabling advisory AI cannot convert a deny/block/quarantine into a permit. | TST-RED-001 | draft |
| FCE-REQ-KRN-011 | The FCE shall not merge, fuse, or correlate objects whose combined classification, domain, and release-caveat tuple lacks an explicit covering permit in the active policy bundle; a blocked merge attempt shall segregate the input objects and emit an audit event. | FCE-ESS-01, FCE-ESS-02 | CAP-06 | ARCH-08, G5 | property-based test, red-team test | No fused object exists whose parent label tuple lacked a covering permit; every attempted unauthorized merge results in a segregate disposition with RC-003 and an audit event; operator override cannot relax the block (B2); derived objects from permitted merges carry high-water-mark labels and full parent linkage. | TST-PRP-051 / TST-RED-051 | draft |

### FCE-ESS-02 — Enforcement across modalities, domain, and handling level

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-ING-010 | The FCE shall ingest and enforce policy on at least two sensor modalities. | FCE-ESS-02 | CAP-01 | ARCH-01, G1 | integration test | At least two synthetic modalities enter the pipeline and traverse G1-G7 under policy control, with dispositions recorded per object. | TST-INT-010 | draft |
| FCE-REQ-POL-011 | The FCE shall represent at least one network security domain and a handling level equivalent to the Protected B target using the project taxonomy, never real Government of Canada markings. | FCE-ESS-02 | CAP-03 | ARCH-03, ARCH-07 | analysis, unit test | Project taxonomy includes at least one network-security-domain value and one Protected-B-equivalent handling target; no real GoC marking procedure is rendered or applied. | TST-UNT-011 | draft |
| FCE-REQ-MET-010 | The FCE shall bind machine-readable classification, domain, and release-caveat metadata to every ingested object, rejecting objects that lack mandatory fields. | FCE-ESS-02 | CAP-01 | ARCH-02, G2 | unit test | Objects missing any mandatory classification, domain, or release-caveat field are rejected or quarantined at G2 with RC-001 and do not proceed to fusion. | TST-UNT-010 | draft |

### FCE-ESS-03 — Programmatic checks without human approval for predefined conditions

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-KRN-010 | The FCE shall perform compliance checks at ingestion and at fusion and shall auto-disposition predefined policy conditions without human approval. | FCE-ESS-03 | CAP-02 | ARCH-04, G4, G5 | integration test | Predefined policy conditions at ingestion and fusion receive automatic permit/restrict/block/quarantine disposition without human approval, and each disposition is audited. | TST-INT-011 | draft |
| FCE-REQ-POL-012 | The FCE shall default-deny and fail closed when a condition is not predefined or is ambiguous, enqueuing the object for human review. | FCE-ESS-03 | CAP-02 | ARCH-03 | property-based test, red-team test | Ambiguous, undefined, or conflicting policy conditions never produce permit-by-default; the object is denied/quarantined and queued for review with RC-005 or a more specific reason code. | TST-PRP-012 | draft |

### FCE-ESS-04 — Provenance for all ingested and produced data

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-PRV-001 | The FCE shall record provenance for every ingested and produced object, including source sensor ID, classification markings, timestamps, and domain of origin. | FCE-ESS-04 | CAP-04 | ARCH-09 | unit test, integration test | Every ingested and produced object has provenance fields for source sensor ID, project-taxonomy classification label, timestamp(s), and domain of origin. | TST-INT-040 | draft |
| FCE-REQ-PRV-002 | The FCE shall preserve provenance across transformation and fusion by linking each derived object to all parent objects. | FCE-ESS-04 | CAP-04 | ARCH-09, ARCH-07 | property-based test | Every transformed or fused object records all parent object IDs; replay of lineage reaches original ingested objects without orphaned derived outputs. | TST-PRP-040 | draft |

### FCE-ESS-05 — Audit logs of rules, actions, and dispositions

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-AUD-001 | The FCE shall emit an audit record for every policy decision documenting the policy rule IDs applied, the enforcement action taken, and the resulting disposition. | FCE-ESS-05 | CAP-05 | ARCH-10, G7 | integration test, inspection | Every policy decision has an audit record containing policy rule ID(s), enforcement action, disposition, and reason code where applicable. | TST-INT-050 | draft |
| FCE-REQ-AUD-002 | The audit chain shall be append-only and tamper-evident, with each record binding the previous record's hash. | FCE-ESS-05 | CAP-05 | ARCH-10 | property-based test, red-team test | Altering, deleting, or reordering a record is detected by chain verification through the previous-hash binding. | TST-RED-050 | draft |

### FCE-ESS-06 — Exportable lineage records

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-EXP-001 | The FCE shall export audit and lineage records in a documented format accompanied by an integrity manifest supporting compliance review, forensic analysis, and accreditation-support review. | FCE-ESS-06 | CAP-08 | ARCH-11 | integration test | Export package includes documented audit and lineage records plus an integrity manifest; language is limited to accreditation-support review and does not claim accreditation status. | TST-INT-060 | draft |
| FCE-REQ-AUD-003 | The FCE shall make the decision sequence deterministically reconstructible (replayable) from audit records alone. | FCE-ESS-06 | CAP-05 | ARCH-10 | integration test, analysis | Given audit records and referenced policy-bundle versions, the decision sequence can be reconstructed with the same dispositions and reason codes. | TST-INT-061 | draft |

### FCE-DES-01 — Real-time enforcement suitable for tactical decision-making (desired)

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-EDG-001 | The FCE should meet an internal end-to-end latency TARGET across multiple modalities and handling levels under a defined synthetic workload on named hardware. All figures are internal targets to be verified. | FCE-DES-01 | CAP-09 | ARCH-12, all gates | benchmark, analysis | Benchmark plan defines synthetic workload, named hardware, per-gate timing, and end-to-end latency target; no measured-performance claim is made until execution with provenance. | TST-PRF-001 / EVD-BENCH-001 | draft |

### FCE-DES-02 — Adaptable policy framework without restart (desired)

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-POL-020 | The FCE should load signed policy-bundle updates (classification guides, release authorities, coalition caveats, operational rules) without system restart, with version pinning and rollback, rejecting invalid or unsigned bundles fail-closed. | FCE-DES-02 | CAP-11 | ARCH-05 | integration test, red-team test | Valid signed bundle update is accepted without restart; invalid or unsigned bundle is rejected fail-closed; in-flight objects remain pinned to a deterministic bundle version. | TST-RED-020 | draft |

### FCE-DES-03 — SWaP and compute limits at the edge (desired)

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-EDG-010 | The FCE should operate within defined SWaP and compute limits on a named edge-class device. All figures are internal targets to be verified. | FCE-DES-03 | CAP-09 | ARCH-12 | benchmark, analysis | Benchmark plan defines SWaP and compute limits (TARGET) for a named edge-class device; no measured-performance claim is made until execution with provenance. | TST-EDG-010 | draft |
| FCE-REQ-EDG-011 | The FCE shall fail closed under resource exhaustion across all six degraded-mode constraint classes (conditional-binding under FCE-DES-03 per legend convention N-03). | FCE-DES-03 | CAP-09 | ARCH-12 | bench test, red-team test | Each of the six degraded-mode constraint classes has a defined fail-closed response; resource exhaustion never produces permit-by-default or ungoverned release; at TRL 1-3 demonstrated via simulated resource limits on the laptop PoC. | TST-EDG-011 | draft |

### FCE-DES-04 — Explainability and controlled override (desired)

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-OPS-001 | The FCE should present a human-readable explanation for each decision, including the rules applied, the attributes consumed, and the reason code. | FCE-DES-04 | CAP-10 | ARCH-13 | inspection, integration test | Each decision explanation lists rule ID(s), attributes consumed, decision, disposition, and reason code in human-readable form. | TST-EXP-001 | draft |
| FCE-REQ-OPS-002 | Operator override shall require authenticated authority, a reason code, a time limit, and an audit signature placeholder; override lacking any precondition shall be rejected fail-closed. | FCE-DES-04 | CAP-10 | ARCH-13, ARCH-10 | red-team test, integration test | Override is accepted only when all preconditions are present and cannot relax the no-unauthorized-merge invariant or a cross-domain block (B2); missing preconditions fail closed. | TST-RED-002 | draft |

### Cross-cutting security

| Req ID | Requirement (full text) | Source | Capability | Design element | Verification | Acceptance criteria | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FCE-REQ-SEC-001 | The FCE shall enforce zero-trust authentication and authorization on every service-to-service and operator interface; unauthenticated or unauthorized requests shall be denied fail-closed. | FCE-ESS-01, FCE-ESS-02 | CAP-02 | all ARCH | red-team test, inspection | Every service-to-service and operator interface has an authN/authZ story; unauthenticated or unauthorized requests are denied fail-closed and do not advance through gates. | TST-RED-SEC-001 | draft |
| FCE-REQ-SEC-002 | The FCE shall authenticate and integrity-bind every PIP-sourced attribute before the PDP consumes it; any unverifiable or unauthenticated attribute shall fail closed at G4 with reason code RC-008 and shall produce an audit event. | FCE-ESS-01, FCE-ESS-03 | CAP-02 | ARCH-06, ARCH-03, G4 | property-based test, red-team test | No PDP decision consumes an unauthenticated or non-integrity-bound attribute; a spoofed or unauthenticated attribute yields a fail-closed disposition with RC-008 and an audit event; disabling attribute authentication cannot yield a permit. | TST-PRP-013 / TST-RED-003 | draft |

## Coverage

Essential: 6/6 (ESS-01...06 all have >= 1 shall). Desired: 4/4 (DES-01...04;
DES-01 and DES-03 confirmed present). Gaps: none at outcome level. Every row has
an ID, a capability trace, a design-element trace, verification method(s), and
M1 Sprint 1 acceptance criteria. Capability-level note: FCE-REQ-KRN-011 was
added 2026-07-03 after an accountability review found the no-unauthorized-merge
invariant (CAP-06) had no dedicated requirement row and downstream artifacts
(`12`, M5, GDR-011) were tracing it by proxy through FCE-REQ-KRN-010.
FCE-REQ-EDG-011 was added 2026-07-03 by the M1 Sprint 2 audit (EVD-M1, RU-03)
to host the resource-exhaustion fail-closed invariant previously mixed into
FCE-REQ-EDG-010. FCE-REQ-SEC-002 was added 2026-07-04 (M3 Sprint 5, RTM v0.3)
closing the `docs/97` B1 RTM follow-up — PIP attribute authentication /
integrity-binding as a dedicated row (was traced by proxy through
FCE-REQ-SEC-001). RTM row count is now 23.

## M1 Sprint 1 handoff status

- OPEN-01: resolved for Sprint 1 by verified verbatim Canada.ca outcome text.
- RTM rows: drafted with acceptance criteria using existing FCE-REQ IDs only.
- GATE-A: not declared; M1 Sprint 2 coverage audit and review remain required.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: requirement IDs, verification-method assignments, capability traces,
  design-element traces, and verbatim outcome anchors.
- Assumptions: solicitation numbering W7714-248676/014 remains the controlling
  procurement reference alongside the Canada.ca outcome text.
- Judgment: acceptance criteria are drafted at analysis depth for TRL 1-3 and
  will be refined during V&V planning.
- Uncertainty: later solicitation amendments, project-taxonomy mapping
  (OPEN-02), and named edge hardware (OPEN-03) may refine rows.
