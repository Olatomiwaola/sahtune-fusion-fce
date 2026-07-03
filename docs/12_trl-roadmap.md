# 12 — TRL Roadmap v0 (draft)

Owner: `trl-evidence-engineer`. Skill: `fce-evidence-pack`.
No accreditation, ATO, or certification is claimed. Accreditation-support
artifacts are labelled "support" only. All performance figures are TARGET.

## Band TRL 1-3 — Basic principles to analytical proof of concept

- Objectives: establish the compliance-kernel concept, schemas, policy model,
  and the seven-gate flow as analytical designs.
- Activities: this architecture package; policy rule examples; threat model;
  synthetic scenario specs.
- Exit criteria:
  1. Architecture, schemas (`06`, `08`), and policy model (`07`) documented.
  2. RTM (`03`) covers 6/6 Essential and 4/4 Desired outcomes.
  3. Threat model (`10`) covers all 8 areas with fail-closed per mode.
  4. Seven-gate flow (`05`) shows no bypass path.
  5. Synthetic scenario specs (`09`) exercise every gate and action.
- Evidence types: design docs, RTM, decision records, threat register.
- Status: this package targets these exit criteria (design-only).

## Band TRL 4-5 — Lab and relevant-environment validation (synthetic)

- Objectives: validate deterministic enforcement and fail-closed behaviour in a
  lab using synthetic data.
- Activities (post-approval, not in this package): implement gates, policy
  evaluation, audit chain; run unit, integration, property-based, and red-team
  tests; degraded-mode profiling across the six constraint classes.
- Exit criteria:
  1. Determinism demonstrated (FCE-REQ-POL-001) by property-based tests.
  2. No-unauthorized-merge invariant demonstrated (FCE-REQ-KRN-010).
  3. Audit replay reproduces dispositions (FCE-REQ-AUD-003).
  4. Fail-closed verified for all six degraded-mode classes.
  5. Internal latency TARGET measured on a named rig (MEASURED, provenance).
- Evidence types: test logs, benchmark reports (labelled), coverage matrix.

## Band TRL 6-9 — Relevant/operational-environment demonstration

- Objectives: demonstrate the capability in progressively more representative
  environments and integrate with Sahtune Fusion.
- Activities (post-approval): integrated demonstrations; hardened deployment on
  named edge hardware; accreditation-support package assembly.
- Exit criteria:
  1. End-to-end demonstration across multiple modalities and handling levels.
  2. Hot-reload without restart demonstrated (FCE-REQ-POL-020).
  3. Full audit export and lineage traceability demonstrated (FCE-REQ-EXP-001).
  4. Sustained fail-closed behaviour under representative load.
  5. Accreditation-support evidence assembled (labelled "support"; no ATO claim).
- Evidence types: integration/field logs, demonstration records, evidence pack.

## Notes

- Bands 4-9 activities are listed for planning only; no implementation is
  produced in this package.
- Every exit criterion traces to RTM requirement IDs and is verified by a named
  method (`03`).

## Facts / Assumptions / Judgment / Uncertainty

- Facts: TRL banding and the design-only status of this package.
- Assumptions: named hardware becomes available for TRL 4-5 measurement.
- Judgment: exit-criteria selection per band.
- Uncertainty: operational-environment access for TRL 6-9 (out of scope here).
