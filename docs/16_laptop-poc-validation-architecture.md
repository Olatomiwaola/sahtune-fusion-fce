# 16 — Laptop PoC Validation Architecture

Owner: `test-evaluation-engineer` with `data-model-engineer`,
`policy-engineer`, `audit-forensics-engineer`, `sensor-fusion-engineer`, and
`red-team-reviewer`.

Purpose: define the defensible pre-lab proof-of-concept method for the FCE. This
is not just a test list. It is the process that prevents the project from
claiming proof from weak evidence.

## Direct Answer

The laptop PoC is not proven by writing a schema validator or getting green unit
tests. The laptop PoC is proven only when a sealed, repeatable evaluation bundle
uses at least two open-source sensor-derived data sources, trims them under a
recorded protocol, converts them through the same FCE envelope path used by the
PoC runtime, runs the seven-gate/policy/audit/no-merge flow locally, and
produces replayable evidence against held-out fixtures.

The proof claim is separated into two layers:

1. **Code correctness:** unit/integration/red-team tests show the PoC machinery is
   wired correctly and the guards fire on bad inputs.
2. **Concept validation:** a held-out laptop evaluation shows the FCE concept can
   enforce metadata validation, deterministic policy, provenance, audit, and
   no-unauthorized-merge behavior on open-source-derived heterogeneous data.

Green code tests alone are not a proof-of-concept claim.

## Method To Transfer Into FCE

### 1. Reconstruct ground truth before code

Before any PoC source file is created, M1/M2 must produce a ground-truth package:

| Artifact | Purpose |
|---|---|
| `docs/03_rtm.md` | Requirement source of truth and acceptance criteria |
| `docs/06_metadata-schema.md` | FCE object-envelope contract |
| `docs/07_policy-decision-model.md` | Deterministic policy/action/reason-code contract |
| `docs/08_audit-record-schema.md` | Audit and replay contract |
| `docs/09_synthetic-dataset-plan.md` | Synthetic scenario discipline |
| `docs/16_laptop-poc-validation-architecture.md` | Laptop proof method and guard discipline |
| `evidence/laptop-poc/source_manifest.json` | Source URLs, query params, hashes, licence notes |
| `evidence/laptop-poc/decision_register.md` | Pre-code decisions and rationale |

No implementation starts from memory, summaries, or chat-only assumptions.

### 2. Lock decisions before code

The following decisions must be written before M2 Sprint 2 or any later PoC code:

| Decision ID | Decision | Why it matters |
|---|---|---|
| FCE-DR-POC-001 | Approved open-source data sources and query windows | Prevents cherry-picking sources after results are known |
| FCE-DR-POC-002 | Schema/envelope version used by the PoC | Prevents silent contract drift |
| FCE-DR-POC-003 | Calibration vs held-out fixture split and random seed | Prevents evaluation contamination |
| FCE-DR-POC-004 | Fixed policy bundle version for held-out evaluation | Prevents post-hoc rule tuning |
| FCE-DR-POC-005 | Pass/fail validation criteria | Prevents moving the goalpost |
| FCE-DR-POC-006 | Evidence write rules and sealed-artifact locations | Prevents accidental overwrite of prior evidence |
| FCE-DR-POC-007 | Dependency boundary: standard library first, external installs only by approval | Keeps laptop proof repeatable |

### 3. Make changes additive and versioned

The PoC may add new artifacts, schema versions, fixture formats, and evidence
records. It must not rewrite prior sealed evidence. If a contract changes, it is
versioned and old evidence remains readable or explicitly rejected by a version
gate.

Required version gates:

| Gate | Rule |
|---|---|
| Envelope version gate | Runtime rejects unsupported fixture/envelope versions |
| Policy bundle version gate | Evaluation records the exact bundle version and rejects missing/ambiguous versions |
| Evidence schema version gate | Test report records the evidence schema version |
| Prior artifact seal | Sealed evidence cannot be overwritten by a later diagnostic or rerun |

### 4. Build guards that make invalid proof impossible

Every guard must have a positive test and a negative test that proves it fires.

| Guard ID | Guard | Invalid proof it prevents | Required rejection test |
|---|---|---|---|
| GDR-001 | Source-provenance guard | Unknown or unverifiable raw data enters the proof | Missing source URL/hash aborts fixture build |
| GDR-002 | Licence/terms guard | Data with unclear reuse terms becomes evidence | Missing licence note marks source unapproved |
| GDR-003 | Trim-manifest guard | Records are cherry-picked without trace | Fixture build aborts without row counts/filter params |
| GDR-004 | Calibration/held-out split guard | Policy tuned on evaluation data | Held-out IDs in calibration set abort evaluation |
| GDR-005 | Data-presence guard | Empty/all-null source produces fake passing output | Empty modality aborts before test report |
| GDR-006 | Envelope-version guard | Old-shaped fixtures silently pass | Unsupported envelope version rejected |
| GDR-007 | Binding-state authority guard | Source pre-validates itself | Source-supplied `policy_binding_state=validated` forced to `unvalidated` |
| GDR-008 | PIP-auth guard | Unauthenticated attributes drive permit | Unauthenticated PIP attribute fails closed with RC-008 |
| GDR-009 | Policy-version guard | Evaluation cannot be replayed | Missing policy bundle version aborts held-out run |
| GDR-010 | No-bypass guard | Object skips gates | Object without complete G1-G7 trace is blocked |
| GDR-011 | No-merge guard | Cross-domain/caveat leak | Unauthorized merge attempt blocked and audited |
| GDR-012 | Override-envelope guard | Human override creates permit | Override cannot relax no-merge or cross-domain block |
| GDR-013 | Audit-write guard | Decisions occur without evidence | Missing audit write blocks release/test pass |
| GDR-014 | No-blind-report guard | Report claims success without guard provenance | Test report cannot be emitted unless guard summary exists |
| GDR-015 | Diagnostic-read-only guard | Inspection mode accidentally writes evidence | Diagnostic mode structurally cannot write model/evidence artifacts |
| GDR-016 | Normalization identity guard | Test fixtures are built differently from runtime input | Fixture builder and runtime use the same envelope-normalization function |

### 5. Separate code correctness from concept validation

Code correctness evidence may be produced in M2-M5. It proves functions behave as
specified. It does **not** prove the concept works.

Concept validation evidence is produced in M7 from a held-out bundle. It proves
whether the concept works at laptop scale. If it fails, the result is still valid
evidence and must be reported verbatim.

| Layer | What it proves | What it cannot claim |
|---|---|---|
| Code correctness | Schema validator, policy evaluator, audit writer, merge guard, and guards behave as specified | Real-world mission suitability |
| Held-out laptop validation | The integrated FCE flow works on sealed open-source-derived heterogeneous fixtures | Lab, edge, field, classified, or operational performance |
| Lab/edge testing | Later TRL 4-5 feasibility on named hardware | Certification, ATO, or operational authority |

## Open-Source Data Sources

Use public, non-sensitive, non-DND data only. The initial laptop proof should use
USGS events plus one Earth-observation/radar source. Maritime/AIS and air-track
sources are candidates only after access terms are verified.

| Source ID | Source | Data type | Laptop role | Verification |
|---|---|---|---|---|
| OSD-01 | USGS Earthquake Catalog API: https://earthquake.usgs.gov/fdsnws/event/1/ | GeoJSON/CSV event records | Lightweight geospatial/time event stream | API docs and query response hash |
| OSD-02 | NOAA NEXRAD/NCEI: https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar | Radar archive/product metadata; optional small product | Radar-like modality metadata | NCEI page and source manifest |
| OSD-03 | NEXRAD on AWS: https://registry.opendata.aws/noaa-nexrad/ | Public NEXRAD bucket metadata/products | Alternate radar access path | Registry entry and object hash |
| OSD-04 | Sentinel-2 COG/STAC: https://registry.opendata.aws/sentinel-2-l2a-cogs/ | Satellite scene metadata; optional small COG chip | EO modality | STAC metadata and hash |
| OSD-05 | USGS Landsat access: https://www.usgs.gov/landsat-missions/landsat-data-access | Satellite scene metadata/products | EO fallback | USGS access record |
| OSD-06 | NOAA/MarineCadastre AIS: https://marinecadastre.gov/ais/ | Maritime AIS CSV if available | Maritime track candidate | Availability/licence check required |
| OSD-07 | OpenSky Network: https://opensky-network.org/ | ADS-B state vectors if access terms allow | Air-track candidate | Access-terms check required |

Minimum pre-lab evaluation: two source families, one of which should be geospatial
event/object records and one radar/EO scene metadata source. Binary radar/image
decoding is optional in TRL 1-3; metadata-level fusion is sufficient if the FCE
contract is exercised.

## Trim Protocol

Raw data is not evidence until it is trimmed and manifested.

1. Select source IDs before data download.
2. Record query URL, parameters, access timestamp, and source page.
3. Store raw responses under `data/raw/` locally; do not commit bulk raw data.
4. Trim to a fixed time window and area of interest where supported.
5. Start with 50-500 records per source.
6. Keep source record ID, timestamp, location/scene bounds, source confidence or
   quality field if present, and minimal payload.
7. Compute source hash and trimmed-file hash.
8. Split deterministically into calibration and held-out fixtures using the
   pre-committed seed.
9. Never tune policy rules after seeing held-out results unless a new policy
   version is declared and the previous held-out result remains sealed.

## Fixture And Evidence Layout

Recommended local/repo layout:

```text
data/raw/                         # local only by default
data/trimmed/                     # small public excerpts only if approved
data/fixtures/calibration/        # FCE envelopes for development tests
data/fixtures/heldout/            # sealed held-out laptop validation bundle
evidence/laptop-poc/source_manifest.json
evidence/laptop-poc/trim_report.md
evidence/laptop-poc/decision_register.md
evidence/laptop-poc/guard_report.json
evidence/laptop-poc/unit_test_report.md
evidence/laptop-poc/heldout_eval_report.md
evidence/laptop-poc/audit.jsonl
evidence/laptop-poc/decisions.jsonl
evidence/laptop-poc/provenance.json
evidence/laptop-poc/export_manifest.json
```

## Required Laptop Tests

| Test ID | Layer | Test | Expected result |
|---|---|---|---|
| LAP-UNIT-001 | Code correctness | Valid envelope passes schema validation | Accepted at G2 |
| LAP-UNIT-002 | Code correctness | Missing mandatory metadata | Fail closed at G2 |
| LAP-UNIT-003 | Code correctness | Source-supplied binding state | Forced to `unvalidated`; source value not trusted |
| LAP-UNIT-004 | Code correctness | Unsupported envelope version | Rejected before policy |
| LAP-UNIT-005 | Code correctness | Identical input/policy repeated | Same decision, reason code, and action |
| LAP-RED-001 | Guard | Held-out object appears in calibration | Evaluation aborts |
| LAP-RED-002 | Guard | Missing source hash/licence/query params | Fixture build aborts or marks source unapproved |
| LAP-RED-003 | Guard | Unauthenticated PIP attribute | Fail closed with RC-008 |
| LAP-RED-004 | Guard | Operator override attempts blocked merge permit | Override rejected |
| LAP-INT-001 | Integration | USGS + EO/radar fixtures traverse G1-G7 | Decisions, audit, provenance emitted |
| LAP-INT-002 | Integration | Permitted same-domain merge | Fused object has parent links and high-water mark |
| LAP-INT-003 | Integration | Unauthorized cross-domain/caveat merge | Merge blocked, inputs segregated, audit emitted |
| LAP-INT-004 | Integration | Audit writer simulated failure | Release/test pass blocked |
| LAP-EVAL-001 | Held-out validation | Held-out bundle replayed twice | Identical decisions and reason codes |
| LAP-EVAL-002 | Held-out validation | Held-out coverage report | Every tested FCE-REQ row mapped to evidence |

## Pass/Fail Criteria

The laptop PoC is ready for lab planning only if:

1. All pre-code decisions exist and are approved.
2. At least two approved open-source data families are manifested and trimmed.
3. Calibration and held-out fixtures are split and sealed before evaluation.
4. Every guard GDR-001 through GDR-016 has a rejection test.
5. Code-correctness tests pass.
6. Held-out validation runs without changing the policy bundle or thresholds.
7. Unauthorized merge is blocked on held-out fixtures.
8. Audit/provenance/export evidence is emitted for held-out decisions.
9. The test report maps results to `FCE-REQ-*` rows.
10. Negative results, gaps, and failed tests are reported verbatim.

If the held-out run improves the architecture evidence but fails one of these
criteria, the correct status is **engineering progress; PoC validation gate not
passed**.

## Train/Serve Identity Rule

FCE does not require model training for the core compliance decision. However,
the same principle applies: the path that creates evaluation fixtures and the
path that runtime ingestion uses must share the same envelope-normalization and
validation functions. If a future advisory AI model is added, its training and
serving features must be generated through the same code path, and this identity
must be tested.

## M1-M7 Rework Map

| Block | Reworked responsibility |
|---|---|
| M1 | Requirements plus proof decisions: acceptance criteria, pass/fail criteria, no-overclaim rules |
| M2 | Envelope contract, version gate, source-provenance/trim manifest guard |
| M3 | Policy bundle versioning, deterministic evaluator, no tuning after held-out exposure |
| M4 | Audit/provenance evidence writer, no-blind-report guard |
| M5 | No-merge guard, override-envelope guard, sealed blocked-merge evidence |
| M6 | Open-source data sourcing, trimming, calibration/held-out split, fixture seal |
| M7 | Code-correctness tests plus separate held-out validation report |

## Facts / Assumptions / Judgment / Uncertainty

- **Facts:** the listed public sources provide official access paths or source
  documentation for open data suitable for lightweight laptop-source selection.
- **Assumptions:** a developer laptop can process 50-500 records per source using
  standard-library Python and small JSON/CSV fixtures.
- **Engineering judgment:** the proof discipline is more important than the size
  of the PoC; the PoC is valuable only if it would catch invalid evidence.
- **Uncertainty:** final source selection depends on access terms, download size,
  and approval for any optional dependency.
