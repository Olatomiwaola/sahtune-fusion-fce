# 12 — TRL Roadmap v0 (draft)

Owner: `trl-evidence-engineer`. Skill: `fce-evidence-pack`.
No accreditation, ATO, or certification is claimed. Accreditation-support
artifacts are labelled "support" only. All performance figures are TARGET.

## Band TRL 1-3 — Basic principles to analytical and experimental proof of concept

- Objectives: establish the compliance-kernel concept, schemas, policy model,
  seven-gate flow, and a minimal executable proof-of-concept (PoC) that shows
  the core software functions are feasible.
- Activities: this architecture package; policy rule examples; threat model;
  synthetic scenario specs (`09`); laptop validation architecture (`16`); PoC
  implementation of schema validation, deterministic policy evaluation,
  seven-gate orchestration, provenance records, audit-log emission, and
  no-unauthorized-merge behavior using approved public open-source-derived
  fixtures plus synthetic red-team variants.
- Exit criteria:
  1. Architecture, schemas (`06`, `08`), and policy model (`07`) documented.
  2. RTM (`03`) covers 6/6 Essential and 4/4 Desired outcomes.
  3. Threat model (`10`) covers all 8 areas with fail-closed per mode.
  4. Seven-gate flow (`05`) shows no bypass path.
  5. Synthetic scenario specs (`09`) and laptop validation architecture (`16`)
     exercise every gate/action and define the proof discipline.
  6. Minimal PoC code ingests at least two approved public open-source-derived
     source families plus synthetic red-team variants, binds project-taxonomy
     metadata, applies deterministic policy decisions, emits provenance and audit
     records, and demonstrates at least one blocked no-unauthorized-merge case.
  7. PoC tests show default-deny behavior for missing metadata, ambiguous policy,
     unauthorised merge attempts, and every invalid-proof guard in `16`.
  8. Held-out laptop validation is reported separately from code-correctness
     tests, with negative results recorded verbatim.
- Evidence types: design docs, RTM, decision records, threat register, PoC source
  code, source manifest, trim report, public-source-derived fixtures, synthetic
  red-team fixtures, guard reports, held-out validation report, test results,
  sample audit/provenance outputs.
- Status: architecture and RTM foundation are in progress; executable PoC work is
  expected during TRL 1-3 after the relevant baselines are locked.

## Band TRL 4-5 — Lab and relevant-environment validation (synthetic)

- Objectives: validate deterministic enforcement and fail-closed behaviour in a
  lab or simulated relevant environment using synthetic data.
- Activities: harden and integrate the TRL 1-3 PoC components; expand the test
  suite; run unit, integration, property-based, and red-team tests; add
  degraded-mode profiling across the six constraint classes; measure TARGETs on
  named hardware only when a benchmark rig is approved.
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

- TRL 1-3 permits executable PoC code. It does not permit production claims,
  operational deployment, live operational/private/controlled/classified data
  handling, formal accreditation,
  production cryptography, or measured-performance claims without provenance.
- Bands 4-9 activities are listed for planning and later approval; TRL 4-5 is
  where the PoC is integrated, hardened, and validated in lab/simulated
  conditions.
- Every exit criterion traces to RTM requirement IDs and is verified by a named
  method (`03`).

## Facts / Assumptions / Judgment / Uncertainty

- Facts: TRL 3 allows analytical and/or laboratory proof-of-concept work; this
  software challenge requires programmatic functions that should be demonstrated
  by a minimal PoC.
- Assumptions: named hardware becomes available for TRL 4-5 measurement.
- Judgment: exit-criteria selection per band.
- Uncertainty: operational-environment access for TRL 6-9 (out of scope here).
