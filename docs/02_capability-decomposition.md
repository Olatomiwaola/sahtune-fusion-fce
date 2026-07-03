# 02 — Capability Decomposition

Owner: `requirements-traceability-engineer` with `fce-lead-systems-architect`.

## Note on outcome text [OPEN-01 resolved for Sprint 1]

The anchors below are verbatim DND IDEaS outcome text from the Canada.ca
challenge page, verified on 2026-07-03. Solicitation identifier
W7714-248676/014 is treated as verified by Kanatir. The Canada.ca page remains
the cited outcome source for this registry.

Source: Canada.ca, "Reliable AI sensor fusion for real world missions",
Defence IDEaS Competitive Projects,
https://www.canada.ca/en/department-national-defence/programs/defence-ideas/element/competitive-projects/challenges/reliable-ai-sensor-fusion-for-real-world-missions.html.

## Outcome registry (verbatim anchors)

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

FCE-DES-01 and FCE-DES-03 are explicitly present (their omission is a known
failure mode per `fce-requirements-traceability`).

## Note on Protected B [OPEN-02]

FCE-ESS-02 names Protected B as a handling target from the solicitation. The
FCE internal label set remains a project taxonomy; a mapping from the project
taxonomy to the named handling target is defined in `07`, never an invented
Government of Canada marking procedure.

## Capabilities

| ID | Capability | Primary architecture element |
|---|---|---|
| CAP-01 | Machine-readable metadata tagging and validation at ingestion | ARCH-01, ARCH-02 |
| CAP-02 | Deterministic policy decision and enforcement (default-deny) | ARCH-03, ARCH-04 |
| CAP-03 | Classification, domain, and caveat labelling and propagation | ARCH-07 |
| CAP-04 | Provenance and lineage capture | ARCH-09 |
| CAP-05 | Tamper-evident audit and chain-of-custody | ARCH-10 |
| CAP-06 | Cross-domain no-unauthorized-merge control | ARCH-08 |
| CAP-07 | Sensor-fusion compliance handoff (AI advisory, deterministic gate) | ARCH-08 |
| CAP-08 | Export and release control with integrity manifest | ARCH-11 |
| CAP-09 | Edge deployment and degraded-mode fail-closed operation | ARCH-12 |
| CAP-10 | Operator review, override, and explainability | ARCH-13 |
| CAP-11 | Adaptable, hot-updatable policy framework (no restart) | ARCH-05 |
| CAP-12 | Optional vision-acceleration benchmark track (NVIDIA) | ARCH-14 |

Synthetic data and verification-and-validation evidence support every
capability and are covered in `09`, `11`, and `12` rather than as a standalone
capability row.

## Capability-to-outcome mapping

Every Essential outcome (6/6) and every Desired outcome (4/4) has at least one
capability.

| Outcome | Capabilities | Rationale (short) |
|---|---|---|
| FCE-ESS-01 | CAP-01, CAP-02, CAP-07 | Tag, decide deterministically, gate fusion; AI advisory only |
| FCE-ESS-02 | CAP-02, CAP-03, CAP-06 | Enforce across modalities, domains, and handling levels |
| FCE-ESS-03 | CAP-01, CAP-02, CAP-07 | Programmatic checks at ingestion and fusion, no human step for predefined conditions |
| FCE-ESS-04 | CAP-04, CAP-01 | Provenance fields bound at ingestion and preserved |
| FCE-ESS-05 | CAP-05 | Audit records of rules, actions, and dispositions |
| FCE-ESS-06 | CAP-05, CAP-08 | Exportable lineage records for review and accreditation support |
| FCE-DES-01 | CAP-07, CAP-09 | Real-time enforcement at tactical latency (internal TARGET) |
| FCE-DES-02 | CAP-11, CAP-03 | Signed policy bundle hot-update without restart |
| FCE-DES-03 | CAP-09, CAP-12 | SWaP and compute limits; optional acceleration evaluated only |
| FCE-DES-04 | CAP-10 | Explainability and controlled, accountable override |

## Coverage summary

Essential: 6/6 mapped. Desired: 4/4 mapped (DES-01 and DES-03 confirmed).
Gaps: none at the outcome level. OPEN-01 text is supplied and verified for
Sprint 1. Open: project-taxonomy-to-handling-level mapping (OPEN-02).

## Facts / Assumptions / Judgment / Uncertainty

- Facts: outcome anchors are verified verbatim Canada.ca challenge text;
  capability list.
- Assumptions: solicitation numbering W7714-248676/014 remains the controlling
  procurement reference alongside the Canada.ca outcome text.
- Judgment: the 12-capability decomposition and the mapping rationale.
- Uncertainty: whether later solicitation amendments shift any mapping row.
