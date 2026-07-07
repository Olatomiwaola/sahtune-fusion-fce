# 09 — Mission Scenario Library v1

Owner: `sensor-fusion-engineer` with `data-model-engineer`.
Skill: `fce-synthetic-sensor-data`.
v1 (M6 Sprint 11, close): finalizes v0 on the decided source families
(leadership decision #6: USGS OSD-01 + Sentinel-2 STAC OSD-04), applies the
M6-open modality rulings (eafb980), embeds M2–M5 conflict coverage, and folds
the Sprint 11 review chain: data-model amendments A1–A4, policy rulings
(RC-002 → block; items 2.4, 2.5), T&E minting (LAP-RED-005/-006,
TST-POL-007/-008), and red-team dispositions RT-M6S11-01..05 (lead concurrence
2026-07-07 throughout). Supersedes v0.

## Ground rules

- DND will not provide data; controlled synthetic scenarios remain required for
  red-team conflict cases.
- Public open-source-derived laptop fixtures are governed by `docs/16`
  (trim protocol, split, guards); this file defines what the fixtures must
  exercise, never how they are built.
- Provenance classes per schema v0.2.0: every object carries `data_origin` in
  {SYNTHETIC, SYNTHETIC-DERIVED, PUBLIC-OPEN-SOURCE}. SYNTHETIC and
  SYNTHETIC-DERIVED artifacts carry the visible SYNTHETIC banner — always.
  PUBLIC-OPEN-SOURCE objects require a resolvable source-manifest reference
  (GDR-001); LIVE is rejected fail-closed at G1 (RC-010). Propagation of
  `data_origin` through fusion is governed by FCE-DR-SCH-005 (RATIFIED
  2026-07-07): any SYNTHETIC/SYNTHETIC-DERIVED ancestry → SYNTHETIC-DERIVED;
  all-SYNTHETIC parents → SYNTHETIC; all-PUBLIC parents → PUBLIC-OPEN-SOURCE
  only under transitive manifest resolvability (construction-time check,
  fail-closed re-verification at any G2 re-entry); the field on
  kernel-constructed objects is written only by ARCH-08.
- "-like" discipline: radar-like, AIS-like, SIGINT-like, acoustic-like — never
  claimed as emulation of any real system.
- Modalities use ONLY the closed D6 registry (docs/07): eo_ir, radar_like,
  sigint_like, acoustic_like, ais_like, uas_telemetry. M6-open modality ruling
  applies (register entry 2026-07-07, eafb980).
- Classification/domain/caveat values use the project taxonomy only (D6).
- Specification only; fixture build is Sprint 12 under docs/16.

## Fixture-source assignments (decision #6 integration)

| Source | Fixture modality | Assignment basis | Scenario |
|---|---|---|---|
| Sentinel-2 STAC items (OSD-04) | eo_ir | direct fit | Scenario 1 |
| USGS seismic events (OSD-01) | acoustic_like | policy-engineer ruling 2026-07-07 (fixture role, not a sensing claim; disclosed in source manifest + trim report) | Scenario 1 |
| All other scenario elements | per scenario | SYNTHETIC (banner) | Scenarios 1–4 |
| Red-team variants mutated from public fixtures | inherits per FCE-DR-SCH-005 | SYNTHETIC-DERIVED (banner; derivation recorded in the fixture-generation manifest) | per variant matrix |

## Scenario 1 — Joint ISR Fusion

- Modalities: eo_ir (PUBLIC-OPEN-SOURCE, Sentinel-2), acoustic_like
  (PUBLIC-OPEN-SOURCE, USGS), radar_like (SYNTHETIC), sigint_like (SYNTHETIC).
- Role: the cross-source association scenario — public fixtures from both
  families are co-registered by AOI/time window (docs/16 trim protocol) so G5
  merge evaluation runs on real heterogeneous metadata (LAP-INT-001/-002/-003).
- Embedded conflicts and expected dispositions (closed registry):

| # | Conflict | Expected disposition | Reason/flag | Trace |
|---|---|---|---|---|
| 1.1 | Cross-domain merge, no covering combination in bundle | block + segregate; null output; inputs individually valid | RC-003 (override-immutable) | FCE-REQ-KRN-011, FCE-REQ-KRN-010 |
| 1.2 | Caveat/domain mismatch with release channel | block; override-immune (lead ruling 2026-07-07 per B2 and RULE-POL-005d; supersedes v0 "restrict") | RC-002 (override-immutable) | FCE-REQ-POL-011 |
| 1.3 | Ambiguous classification (unresolvable label) | quarantine + require-human-review | RC-005 | FCE-REQ-POL-012 |
| 1.4 | Mixed pinned bundle versions in a MergeRequest | quarantine + review queue (NOT block) | RC-005 + detection flag mixed_bundle_versions on the quarantine record (docs/18 §5) | FCE-REQ-POL-012, FCE-REQ-POL-001 |
| 1.5 | Permitted same-domain merge (positive case) | permit; fused object with kernel-written parentage and HWM label; `data_origin` per FCE-DR-SCH-005 | — (clean permit; exact-multiset covers(); Sprint 12 note: the covering combination is enumerated in the bundle fixture BEFORE fixture evaluation, per FCE-DR-POC-004 spirit) | FCE-REQ-KRN-011, FCE-REQ-PRV-002 |

- Red-team variants applied here (matrix below): forged parentage, tampered
  classification label, PIP-spoof (RC-008 at G4), unauthorized merge
  (exercises 1.1).
- Expected audit classes: ingestion, policy-decision, fusion-decision,
  quarantine (with detection_flags where applicable).
- Trace: FCE-REQ-KRN-010/-011/-012, FCE-REQ-POL-012, FCE-REQ-PRV-002,
  FCE-REQ-ING-010, FCE-REQ-SEC-002.

## Scenario 2 — Maritime Domain Awareness

- Modalities: radar_like, ais_like, eo_ir — ALL SYNTHETIC (banner).
- Derived labels: anomaly-like event annotations are derived event/labels
  computed over radar_like/ais_like observations (M6 modality ruling — never a
  source modality); advisory metadata only; never present in any rule
  predicate (shared constraint 2).
- Embedded conflicts and expected dispositions:

| # | Conflict | Expected disposition | Reason/flag | Trace |
|---|---|---|---|---|
| 2.1 | Cross-domain merge attempt without permit (maritime track + restricted-domain object) | block + segregate | RC-003 | FCE-REQ-KRN-011 |
| 2.2 | Caveat violation against release channel | block; override-immune (same lead ruling as 1.2) | RC-002 (override-immutable) | FCE-REQ-POL-011 |
| 2.3 | Stale acquisition timestamp under the staleness policy | fail-closed disposition | RC-004 — FIXTURE ONLY at M6: the emission demonstration is an M7 obligation (RT-M3S6-05); EVD-M6 must not claim RC-004 demonstrated | FCE-REQ-ING-011 |
| 2.4 | Broad release request spanning caveat-compatible and caveat-incompatible channels | restrict — partial permit: release proceeds only to the caveat-compatible subset | reason_codes empty (partial permit, not a denial); rules fired cited; permitted subset carried in the rules-fired citation and the FCE-REQ-OPS-001 human-readable explanation, NEVER in policy-decision event_detail (RT-M6S11-01 disposition path (b) — closed D2 sub-schema unchanged) | FCE-REQ-POL-011, FCE-REQ-OPS-001 |
| 2.5 | Higher-classification object arriving on a lower-level channel | route-to-higher-domain — DELIVERY DISPOSITION ONLY (RT-M6S11-02): object envelope and all labels unchanged; not released on the original channel; destination domain recorded only in the routing-class audit record event_detail | reason_codes empty unless the registry explicitly requires one; rules fired cited | FCE-REQ-POL-011, FCE-REQ-AUD-001 |

- Red-team variant applied here: spoofed AIS-like source identity → G1 reject,
  RC-011, labelled MECHANISM-SIMULATED (FU-M3S5-1 pattern; no
  source-authentication claim, H3/H4 open).
- Expected audit classes: ingestion, policy-decision, routing, quarantine.
- Trace: FCE-REQ-POL-011, FCE-REQ-ING-010, FCE-REQ-ING-011, FCE-REQ-KRN-011,
  FCE-REQ-AUD-001, FCE-REQ-OPS-001.

## Scenario 3 — Tactical Edge Dismounted

- Modalities: acoustic_like dismounted event stream (SYNTHETIC — REPLACES v0
  "wearable events" per the M6 modality ruling: replacement chosen over a
  uas_telemetry reframe; purpose preserved — low-SWaP passive event sources at
  the edge), uas_telemetry (SYNTHETIC — supporting small-UAS feed), eo_ir
  (SYNTHETIC).
- Context: degraded network; constrained compute.
- Embedded conflicts and expected behaviour:

| # | Conflict | Expected disposition | Reason/flag | Trace |
|---|---|---|---|---|
| 3.1 | Resource exhaustion during decision (simulated limits per RTM acceptance) | fail-closed; no permit-by-default; no ungoverned release | degraded-mode classes per FCE-REQ-EDG-011 (TRL 1-3: simulated) | FCE-REQ-EDG-011 (v0's EDG-010 trace corrected — the fail-closed invariant moved at RTM v0.2) |
| 3.2 | Audit-write starvation at G7 | pipeline halts; object does not proceed (audit loss = fail-closed) | G7 rule (docs/08 overflow/backpressure) | FCE-REQ-AUD-001, FCE-REQ-AUD-002 |
| 3.3 | Network loss mid-flow | in-flight objects complete under pinned bundle or fail closed; no gate bypass | GDR-010 no-bypass | FCE-REQ-KRN-001 |
| 3.4 | G1-reject family (hosted here): unsupported schema_version; data_origin=LIVE; source-supplied policy_binding_state | reject (RC-009); reject (RC-010); accept-with-detection — forced unvalidated | RC-009; RC-010; RC-012 + detection flag source_supplied_policy_binding_state | FCE-REQ-ING-010, FCE-REQ-MET-010 |

- Red-team variants applied here: replay of stale packets (RC-004 fixture —
  same M7 claim boundary as 2.3), malformed-envelope family (RC-001 at G2:
  bad uuid/RFC3339/hash, unknown taxonomy value, unknown extra field per
  FCE-DR-SCH-003, and an explicit duplicate object_id case → quarantine via
  RC-001 path + duplicate_object_id flag per FCE-DR-SCH-004 D5 — RT-M6S11-04
  disposition), pre-marking (exercises 3.4's RC-012 case).
- Expected audit classes: ingestion, policy-decision, quarantine.
- Trace: FCE-REQ-EDG-011, FCE-REQ-AUD-001/-002, FCE-REQ-MET-010,
  FCE-REQ-ING-010/-011, FCE-REQ-KRN-001.

## Scenario 4 — UAV Mission Support

- Modalities: eo_ir payload observations, uas_telemetry platform feed — both
  SYNTHETIC (banner). Target-track estimates appear as DERIVED LIFECYCLE
  OBJECTS (tracklet, fused track — 11-type model), not as a modality; they are
  CONSTRUCTED IN-RUN by ARCH-08 from observation-level fixtures — no
  derived-type object is authored as a fixture input outside the deliberate
  forged-parentage variant (data-model amendment A2). Operator requests and
  mission replay are workflow elements, not data modalities.
- Embedded conflicts and expected dispositions:

| # | Conflict | Expected disposition | Reason/flag | Trace |
|---|---|---|---|---|
| 4.1 | Operator override, all four preconditions present, in-envelope decision | accepted; audited | RC-007 | FCE-REQ-OPS-002 |
| 4.2 | Override missing any precondition | rejected fail-closed; rejection audited | override class (docs/08 #9) | FCE-REQ-OPS-002 |
| 4.3 | Override vs an RC-003 blocked merge (immunity case, V6 pattern) | rejected; block stands | B2 / override_immutable | FCE-REQ-OPS-002, FCE-REQ-KRN-011 |
| 4.4 | Override vs RC-005 quarantine and vs unrecorded_parentage quarantine (RT-M5S9-05 pair) | both rejected (permitted_envelope excludes quarantine) | RULE-POL-005 envelope check | FCE-REQ-OPS-002, FCE-REQ-POL-012, FCE-REQ-KRN-012 |
| 4.5 | Downgrade with valid authority + transformation proof | authorized downgrade | RC-006 (downgrade audit row: authority + proof reference mandatory, FU-M4S8-1) | FCE-REQ-OPS-002 path, docs/08 downgrade matrix |
| 4.6 | Downgrade with invalid/missing proof (red-team) | rejected fail-closed | downgrade preconditions | FCE-REQ-OPS-002 |

- Workflow coverage: export package emitted for the scenario's audit chain
  (export-class record with manifest sha-256); replay R1 + R2 exercised over
  the chain read-only (register L3).
- Expected audit classes: policy-decision, fusion-decision, downgrade,
  override (accepted AND rejected), export.
- Trace: FCE-REQ-OPS-001/-002, FCE-REQ-AUD-003, FCE-REQ-EXP-001,
  FCE-REQ-KRN-012.

## Red-team variant matrix (Sprint 12 build set — seven variants)

Lead concurrence 2026-07-07: "forged parentage" is the seventh variant,
distinct from "tampered" because it exercises FCE-REQ-KRN-012 / C3.

Lineage carrier rule (data-model amendment A1): SYNTHETIC-DERIVED variants
record their derivation (source record ID + mutation applied) in the
FIXTURE-GENERATION MANIFEST; envelope `parent_object_ids` stays empty — EXCEPT
the forged-parentage variant, where envelope-claimed parentage IS the test
payload. This prevents non-parentage variants from tripping the C3 cross-check
before reaching the gate they test.

data_origin values below are DEFAULTS (data-model amendment A4): the
fixture-generation manifest records the actual class per fixture, assigned by
construction method under FCE-DR-SCH-005.

| Variant | data_origin (default) | Lineage carrier | Applied in | Expected outcome | Trace |
|---|---|---|---|---|---|
| tampered (label/hash mutation of a public fixture) | SYNTHETIC-DERIVED | manifest | S1 | G2/G3 integrity fail-closed (RC-001 path) | FCE-REQ-MET-010 |
| malformed (envelope family incl. unknown field AND explicit duplicate object_id case) | SYNTHETIC or SYNTHETIC-DERIVED per construction | manifest | S3 | G2 reject, RC-001 (FCE-DR-SCH-003); duplicate object_id → quarantine via RC-001 path + duplicate_object_id flag (FCE-DR-SCH-004 D5) | FCE-REQ-MET-010 |
| stale (timestamp beyond staleness policy) | SYNTHETIC-DERIVED | manifest | S2, S3 | RC-004 fail-closed — fixture at M6, demonstration M7 | FCE-REQ-ING-011 |
| PIP spoof (unauthenticated attribute) | SYNTHETIC | manifest | S1 | G4 fail-closed, RC-008 | FCE-REQ-SEC-002 |
| pre-marking (source-supplied policy_binding_state) | SYNTHETIC-DERIVED | manifest | S3 | forced unvalidated + RC-012 detection flag | FCE-REQ-MET-010 (B3) |
| unauthorized merge (no covering combination) | SYNTHETIC + PUBLIC parents (request only; no output object exists on block) | manifest | S1 | RC-003 block + segregate | FCE-REQ-KRN-011 |
| forged parentage (caller-supplied/self-declared, both cross-check directions) | SYNTHETIC-DERIVED | ENVELOPE parent_object_ids (deliberately — the test payload) | S1 | quarantine + unrecorded_parentage flag (docs/18 §1) | FCE-REQ-KRN-012 |

## Minted test descriptions (Sprint 11; implementation Sprint 12/M7 per class)

- LAP-RED-005 (GDR-005): a fixture build where one declared modality's record
  set is empty or all-null after trim → build aborts before any test report is
  emitted; abort recorded in the guard report; no EVD-M6 artifact producible
  from the aborted state. Trace: FCE-REQ-ING-010.
- LAP-RED-006 (GDR-016): the same trimmed source record passed through the
  fixture-builder path and the runtime ingestion path yields byte-identical
  envelopes post-CANON-1; any divergence fails the build. Trace:
  FCE-REQ-MET-010.
- TST-POL-007 (item 2.4): broad release request → disposition restrict; record
  cites rule(s) fired; permitted subset appears in the rules-fired citation and
  the FCE-REQ-OPS-001 explanation; reason_codes empty; policy-decision
  event_detail remains the closed D2 sub-schema. Writer-rejection hook
  (RT-M6S11-01): a policy-decision record carrying an unknown
  `permitted_channels` detail field is refused fail-closed. Trace:
  FCE-REQ-POL-011, FCE-REQ-OPS-001, FCE-REQ-AUD-001.
- TST-POL-008 (item 2.5): routed object produces a routing-class record with
  destination domain in event_detail, disposition route-to-higher-domain,
  reason_codes empty; object not released on the original channel.
  Envelope-invariance hook (RT-M6S11-02): routed object's envelope hash is
  identical pre/post routing; only audit linkage differs. Trace:
  FCE-REQ-POL-011, FCE-REQ-AUD-001, FCE-REQ-PRV-001.
- DR-SCH-005 re-entry hook (RT-M6S11-03): a fused all-public object whose
  parent manifest entry has been removed fails closed at G2 re-entry. Trace:
  FCE-REQ-PRV-002, FCE-REQ-MET-010.

## Closed-registry coverage roll-up

RC-001 (malformed incl. duplicate-ID; forged-parentage path) S1/S3 · RC-002
(1.2, 2.2 — block, override-immune) · RC-003 (1.1, 2.1, 4.3) · RC-004 (2.3,
3.x — M7 claim boundary stated) · RC-005 (1.3 ambiguous; 1.4 mixed-version) ·
RC-006 (4.5) · RC-007 (4.1) · RC-008 (S1 PIP spoof) · RC-009/-010 (3.4) ·
RC-011 (S2, mechanism-simulated) · RC-012 (3.4 / pre-marking). Detection
flags: unrecorded_parentage (S1), mixed_bundle_versions (1.4),
source_supplied_policy_binding_state (3.4), duplicate_object_id (S3 explicit
case). 12/12 RC codes + all four flags represented (representation at M6;
demonstration claims are per-item and M7-bounded where stated).

## Policy-action coverage roll-up

permit (1.5, 2.4 granted subset) · restrict (2.4) · block (1.1, 1.2, 2.1, 2.2,
4.3) · segregate (1.1, 2.1) · quarantine (1.3, 1.4, forged parentage,
duplicate-ID) · reject (3.4, malformed) · route-to-higher-domain (2.5) ·
require-human-review (1.3, 1.4) · downgrade (4.5) · override (4.1–4.4) ·
transform — ACCEPTED GAP at M6 (lead concurrence 2026-07-07): representability
demonstrated in docs/07; fixture-level exercise deferred to Sprint 13 / M7 V&V
planning; recorded in the decision register. 10/11 exercised + 1 explicit gap.

## Modality coverage roll-up

eo_ir (S1 public, S2–S4 synthetic) · acoustic_like (S1 public, S3 synthetic) ·
radar_like (S1, S2) · sigint_like (S1) · ais_like (S2) · uas_telemetry (S3,
S4). All six registered modalities exercised; FCE-REQ-ING-010's two-modality
minimum exceeded on public fixtures alone (eo_ir + acoustic_like).

## Trim-report obligations (Sprint 12)

Per RT-M6S11-05 disposition: the trim report states whether the mechanical
window-widening rule (<10 association candidate pairs after trim) fired or did
not fire, with before/after candidate-pair counts in either case. Widening is
additive-only; split determinism is unaffected (seed over stable source record
IDs, FCE-DR-POC-003).

## Facts / Assumptions / Judgment / Uncertainty

- Facts: closed D6 and RC registries (docs/07); docs/18 merge/quarantine
  semantics and flags; docs/08 event classes, closed event_detail sub-schemas,
  and requiredness; schema v0.2.0 provenance classes; FCE-DR-SCH-005 (ratified
  2026-07-07); M6-open rulings (eafb980); decision #6 source families; RTM
  v0.5 row set; RT-M3S6-05 M7 due date; RT-M6S11 dispositions.
- Assumptions: AOI/time-window co-registration yields ≥10 association candidate
  pairs (mechanical widening otherwise, disclosed per trim-report obligations);
  Sentinel-2 STAC access remains keyless (verify at Sprint 12 network-approval
  scoping).
- Judgment: public fixtures concentrated in S1; S3 wearable→acoustic_like
  replacement; conflict-to-scenario assignments; variant-to-scenario matrix;
  lineage-carrier rule placement.
- Uncertainty: association-candidate yield until download;
  combination-enumeration scale at scenario richness (docs/18 flags a DR if it
  breaks); TRANSFORM ACTION FIXTURE GAP — accepted at M6, deferred to Sprint 13
  / M7 V&V planning (lead concurrence 2026-07-07); whether M7 requires a
  fixture-level transform case is that plan's call.
