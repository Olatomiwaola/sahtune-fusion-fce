# 02 — Capability Decomposition

Owner: `requirements-traceability-engineer` with `fce-lead-systems-architect`.

## Note on outcome text [OPEN-01]

The anchors below are paraphrased working anchors supplied for design use. They
are NOT the verbatim DND IDEaS wording and must be replaced with the quoted
solicitation text before this mapping is final. No verbatim text is fabricated.

## Outcome registry (paraphrased anchors — authoritative until wording supplied)

### Essential outcomes
- FCE-ESS-01: Modular AI-enabled component that automatically enforces
  classification rules and policy constraints during multi-sensor fusion.
- FCE-ESS-02: Machine-readable policy enforcement across at least two sensor
  modalities, at least one network security domain, and at least Protected B
  classification handling.
- FCE-ESS-03: Programmatic compliance checks and enforcement during ingestion
  and fusion without human approval for predefined policy conditions.
- FCE-ESS-04: Provenance records for all ingested and produced data, including
  source sensor ID, classification markings, timestamps, and domain of origin.
- FCE-ESS-05: Audit logs documenting policy rules applied, enforcement actions
  taken, and resulting compliance dispositions.
- FCE-ESS-06: Exportable audit records supporting lineage traceability from
  ingestion to fusion output for compliance review, forensic analysis, or
  accreditation support.

### Desired outcomes
- FCE-DES-01: Real-time compliance enforcement across multiple sensor
  modalities and classification levels at tactical latency.
- FCE-DES-02: Adaptable policy framework where classification guides, release
  authorities, coalition caveats, and operational rules can be updated without
  system restart.
- FCE-DES-03: SWaP and compute limits accounted for in tactical edge
  deployment.
- FCE-DES-04: Explainable compliance decisions and controlled operator override
  with accountability safeguards.

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
Gaps: none at the outcome level. Open: verbatim outcome text (OPEN-01);
project-taxonomy-to-handling-level mapping (OPEN-02).

## Facts / Assumptions / Judgment / Uncertainty

- Facts: outcome anchors as supplied by the user; capability list.
- Assumptions: anchors approximate the final wording closely enough for design.
- Judgment: the 12-capability decomposition and the mapping rationale.
- Uncertainty: whether final verbatim wording shifts any mapping row.
