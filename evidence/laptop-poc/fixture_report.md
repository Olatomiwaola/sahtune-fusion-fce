# EVD-M6 — Sprint 12 Fixture Package Report

Chat-authored per working-conventions rule 9 (RATIFIED 2026-07-07); evidence
figures quoted verbatim from the M6-07A read-only collection at HEAD 507d3c5
and the Stage read-backs of the M6-06 build. Date: 2026-07-08.

## Claim boundary

This report claims fixture existence, guard function, and coverage
REPRESENTATION only. No enforcement demonstration is claimed — that is M7
(two-layer harness, sealed held-out replay, deterministic-outcome
verification, honest negative results). The RC-004 stale case exists as
fixture only; its emission demonstration is an M7 obligation (RT-M3S6-05).
USGS and Sentinel-2 STAC data are reproducible public-source anchors for a
TRL 1-3 compliance-engine proof of concept — never operational or
CAF-equivalent data.

## Source acquisition (network per the one-time Sprint 12 approval, bounds 1–6)

Two approved public source families (leadership decision #6; OPEN-04):
- OSD-01 USGS FDSN event service (fixture modality acoustic_like —
  disclosed assignment): 200 event records, AOI lat 35.0–37.5 / lon
  −122.0–−118.0, window 2025-06-01→2025-08-31, minmagnitude=1.5,
  orderby=time-asc, limit=200.
- OSD-04 Sentinel-2 STAC via earth-search.aws.element84.com /v1 (eo_ir):
  corrective slice of 100 items constrained to the USGS effective span
  (slice-alignment supersession recorded in the source manifest; original
  Stage-B slice retained on disk, never used for fixtures).
Network re-opens beyond the initial download go: two, each lead-authorized
and closed immediately (GDR-002 licence remediation; corrective re-query).

OSD-01 licence governance value (GDR-002): the USGS public-domain and credit
statements captured verbatim from the copyrights-and-credits page, first
line: "USGS-authored or produced data and information are considered to be
in the U.S." — full provenance chain:
R1 8c610ec9839398f0a52fa695c5c9c23f0aa216489933a9d1e6a6de098e4b95e1 https://earthquake.usgs.gov/fdsnws/event/1/
R2 358f498d734ad4f1887a2eaf9381b133144c463ea7c803bd2a554d845040cc33 https://www.usgs.gov/policies-and-notices
R3 e8cee4b1d24072d785815704ce718649284cd0ad49d59a058176c59043191592 https://www.usgs.gov/information-policies-and-instructions
R4 e4b6684666812ccebd165218cb183a942120503a583a921a8623f2f5b239bbab https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits
OSD-04 licence: Copernicus/Sentinel terms captured verbatim from the Stage-A
registry page with terms URL (source manifest).

## Trim and association

Metadata-level trim per docs/16 steps 4–7. Association candidate pairs
(pre-committed definition: epicenter within item bbox AND |Δt| ≤ 7 days):
208 ≥ 10 — mechanical widening NOT fired (before = after; trim report).

## Split and seal (FCE-DR-POC-003 / -004 / -006)

Deterministic 70/30 stratified split, rank = sha-256 over
"<record_id>:12918724377571503927" (seed minted blind at Sprint 11 close,
before any download). Calibration: USGS 140, S2 70 (first-3 ranked IDs —
USGS: nc75211292, nc75211237, nc75197406; S2: S2C_11SKU_20250724_0_L2A,
S2B_11SKV_20250719_0_L2A, S2B_11SMU_20250716_0_L2A). Held-out: USGS 60,
S2 30, in two sealed files:
0f6897ee626fb085d115f3139ebf16189e918d0ec0530247463b4ed1997ab6b6  data/fixtures/heldout/osd01_usgs_heldout.json
359e396b934e5a0c91610dfa8303dd8cd0e5093cf4affbac2056ef9e0e97d10f  data/fixtures/heldout/osd04_s2stac_heldout.json
Aggregate seal digest (sha-256 over sorted "hash  path" lines):
059829241e527eb1aa09e3ff8ce8abafed1eeee445e04474f32ac267954ed63e
Pinned policy bundle for held-out evaluation: proj-baseline@0.2.0
(FCE-DR-POC-004 resolved at this seal; see the Sprint 12 seal record for the
bundle hash and the re-pin protocol). Held-out set untouched after seal
until the M7 replay.

## Variants

Seven synthetic red-team variants per docs/09 v1 (tampered, malformed incl.
explicit duplicate-ID, stale, PIP spoof, pre-marking, unauthorized merge,
forged parentage), lineage in the fixture-generation manifest per amendment
A1 (envelope parentage only for forged-parentage), data_origin per
FCE-DR-SCH-005; GDR-004 assertion clean — no variant derives from a held-out
parent.

## Guard and test evidence

Fresh full suite at close: 106 passed (98 baseline + 8 fixture-sprint tests:
LAP-RED-001, LAP-RED-002a/b/c, LAP-RED-005, LAP-RED-006, GDR-006
envelope-version reuse check, permitted_channels writer-rejection hook).
Fixture-build guards demonstrated firing: 7/7 (GDR-001, -002, -003, -004,
-005, -006, -016).

## Coverage representation

300 public-fixture envelopes (all PUBLIC-OPEN-SOURCE, manifest-resolvable
per GDR-001). Closed-registry representation: RC 12/12; detection flags 4/4
(unrecorded_parentage, mixed_bundle_versions,
source_supplied_policy_binding_state, duplicate_object_id). docs/09 v1
conflict items represented in fixtures: 17/20 — items 3.1, 3.2, 3.3 are
runtime conditions (resource exhaustion, audit-write starvation, network
loss), not static fixtures; they are exercised by the M7 harness.

## Findings and honest notes

- Pre-seal defect caught: bundle v0.1.0's merge permits all carry
  PROJ-CAVEAT-X; the docs/09 item-1.5 caveat-empty public pair was NOT
  covered — held-out evaluation would have false-negatived the deliberate
  positive case. Resolved pre-evaluation by proj-baseline@0.2.0
  (MP-S1-15-PUBLIC-PAIR), lead concurrence 2026-07-08 — POC-004 ordering
  (pin before evaluation) honored.
- Scenario 4 tuple coverage under 0.2.0 is verified at Sprint 13; any change
  requires explicit pre-evaluation re-pin (recorded), never silent
  evaluation under a different bundle, never post-seal mutation.
- Process notes (register): M6-05r licence-capture gap (remediated R1→R4);
  R3 extractor bytes/str bug (recovered from the saved local file, no extra
  network); slicing artifact (corrected by the supersession-recorded
  re-query); eafb980 read-back deviation (M6-01; codified as rule 10).
- No test failures; no guard fired on the real build; raw source files (8)
  retained local-only under ignored data/raw/.

## Trace

FCE-REQ-ING-010/-011, FCE-REQ-MET-010, FCE-REQ-PRV-001/-002,
FCE-REQ-POL-011, FCE-REQ-KRN-011/-012, GDR-001..006/-016,
FCE-DR-POC-003/-004/-006, FCE-DR-SCH-005.
