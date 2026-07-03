# 09 — Synthetic Dataset Plan v0 (draft)

Owner: `sensor-fusion-engineer` with `data-model-engineer`.
Skill: `fce-synthetic-sensor-data`.

## Ground rules

- DND will not provide data; controlled synthetic scenarios remain required for
  red-team conflict cases.
- Public open-source-derived laptop fixtures are governed separately by
  `16_laptop-poc-validation-architecture.md`.
- Every synthetic object in this file carries `data_origin: SYNTHETIC` and every
  rendered synthetic artifact carries a visible SYNTHETIC banner. Non-negotiable.
- "-like" discipline: radar-like, AIS-like, SIGINT-like, acoustic-like — never
  claimed as emulation of any real system.
- Classification and domain values use the project taxonomy only.
- Specification only; no synthetic dataset is generated until approved.

## Baseline scenarios

### Scenario 1 — Joint ISR Fusion — ALL DATA SYNTHETIC
- Modalities: EO/IR detections, radar-like tracks, SIGINT-like metadata.
- Object schema: `06`.
- Classification labels (project taxonomy): PROJ-LEVEL-1..3. Domains: DOMAIN-A, DOMAIN-B.
- Policy conflicts embedded: (1) cross-domain merge with no permit; (2) caveat
  mismatch; (3) ambiguous classification.
- Expected decisions: (1) block + segregate, RC-003; (2) restrict, RC-002;
  (3) quarantine + require-human-review, RC-005.
- Expected audit: fusion_decision, transformation, quarantine records.
- Success: all conflicts dispositioned per `07`; Failure cases: missing metadata
  object rejected at G2. Red-team: tampered classification label.
- Trace: FCE-REQ-KRN-010, FCE-REQ-POL-012.

### Scenario 2 — Maritime Domain Awareness — ALL DATA SYNTHETIC
- Modalities: radar-like, AIS-like, EO/IR, anomaly events.
- Conflicts: (1) domain mismatch; (2) caveat violation; (3) stale timestamp.
- Expected decisions: block RC-003; restrict RC-002; quarantine RC-004.
- Expected audit: policy_decision, routing, quarantine.
- Red-team: spoofed AIS-like source identity.
- Trace: FCE-REQ-POL-011, FCE-REQ-ING-010.

### Scenario 3 — Tactical Edge Dismounted — ALL DATA SYNTHETIC
- Modalities: wearable events, UAS telemetry, EO/IR detections; degraded network.
- Conflicts: (1) resource exhaustion during decision; (2) network loss mid-flow.
- Expected behaviour: fail-closed under degraded mode; audit backpressure holds
  release; no object bypasses gates.
- Expected audit: ingestion, policy_decision, quarantine.
- Red-team: replay of stale packets; audit-write starvation.
- Trace: FCE-REQ-EDG-010, FCE-REQ-AUD-002.

### Scenario 4 — UAV Mission Support — ALL DATA SYNTHETIC
- Modalities: EO/IR payload observations, platform telemetry, target-track
  estimates, operator requests, mission replay.
- Conflicts: (1) operator override request; (2) downgrade request.
- Expected decisions: override only with full preconditions (RC-007) else reject;
  downgrade only with valid proof (RC-006).
- Expected audit: override, downgrade, export records; full replay exercised.
- Red-team: override without authority; invalid downgrade proof.
- Trace: FCE-REQ-OPS-001, FCE-REQ-OPS-002, FCE-REQ-AUD-003.

## Modality coverage

Minimum: EO/IR + radar-like (2 modalities). Stretch: EO/IR + radar-like +
acoustic-like + SIGINT-like + UAS telemetry. All scenarios collectively
exercise every gate and every policy action at least once.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: DND will not provide data; SYNTHETIC labelling rule; "-like" rule;
  public-source-derived laptop fixtures are governed by `16`.
- Assumptions: four synthetic scenarios cover the red-team conflict space pending
  laptop source selection under OPEN-04.
- Judgment: the specific conflict cases per scenario.
- Uncertainty: whether additional coalition scenarios are needed.
