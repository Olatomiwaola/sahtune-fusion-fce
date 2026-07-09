# EVD-M7 — Sprint 14 Two-Layer Harness & Sealed Held-Out Evaluation Report

Chat-authored per working-conventions rule 9 (evidence-append). Figures quoted
verbatim from the Sprint 14 Layer-1 suite and the single sealed Layer-2 held-out
run at HEAD 24a38c6 (+ the duplicate-ID fix commit). Date: 2026-07-08.
Owner role: `test-evaluation-engineer`. Skill: `fce-test-and-evaluation`.

## Verdict

**Engineering progress; PoC validation gate not passed** (docs/16 status).

The integrated FCE flow enforced metadata validation, deterministic policy,
provenance, audit, and no-unauthorized-merge behaviour on sealed open-source-
derived held-out fixtures, with deterministic (twice-identical) results and a
verifiable audit chain. It is **not** a full pass because (a) the held-out stale
case does not emit RC-004 — RFC3339/wall-clock freshness is bounded by H4
(trusted/attested time), carried as a disclosed negative; and (b) the GDR-010
no-bypass rejection test is deferred. This is an expected, honest M7 outcome, not
a block failure — honest negatives are a required output.

## Claim boundary

This report claims what the sealed held-out run demonstrated at TRL 1-3 on a
laptop. It claims no certification, accreditation, ATO, operational or
CAF-equivalent capability, and no trusted-time, cryptographic, or concurrency
guarantees (H4/H6/H7 open, disclosed). USGS and Sentinel-2 STAC data are
reproducible public-source anchors. AI is advisory only; every disposition here
is deterministic. Standards are reference alignment only.

## Run-boundary integrity (single documented held-out read)

- Sealed bundle: `bundle_proj-baseline_0.2.0.json` sha-256 match = **true**
  (`6a830b24…c53502`); `pinned_version="0.2.0"`.
- Held-out aggregate digest match = **true** (`059829241e…954ed63e`).
- Held-out corpus and bundle byte-identical to the Sprint 12 seal — nothing
  mutated in place; no re-pin (Scenario 4 covered by MP-V1-SAME-DOMAIN,
  resolved pre-run).
- Read was aggregate-hash + evaluation only; GDR-015 diagnostic-read-only held.

## Layer 1 — code correctness (calibration only)

Full suite **126 passed, 1 skipped** from `.venv` (Python 3.12.13, pytest
9.1.0), on the sealed 0.2.0 bundle. The 1 skip = GDR-010 no-bypass (deferred).
Matrix-new coverage landed: TST-FUS-S4 (S4 fused-track permit via
MP-V1-SAME-DOMAIN → HWM (PROJ-LEVEL-2, DOMAIN-A, [PROJ-CAVEAT-X]) + kernel-written
parentage), TST-PRP-011 (≥3-way lattice: order-independent, idempotent,
transitive; ties fail closed — RT-M3S6-03), TST-PRP-001 breadth (full
decision-tuple determinism across permit/reject/block/quarantine — RT-M3S6-02),
TST-UNT-030 (RULE-ING-011 → RC-004 fail-closed reject + audit on the injected
tick — RT-M3S6-05), GDR-009 (version-mismatch reject), OPS-001 explanation
surface (TST-EXP-001..004), the sealed-bundle integrity gate, and the
FCE-DR-SCH-004 D5 duplicate-ID detection (below).

## Layer 2 — sealed held-out evaluation (single pass)

Every held-out object traversed G1→G7 under sealed 0.2.0. Ten oracle cases
(§ docs/17 §5), reported verbatim:

| Case | Oracle (expected) | Actual | Verdict |
|---|---|---|---|
| clean_corpus | accept/permit; ≥2 modalities | 90 accepted / 90 permit; acoustic_like=60, eo_ir=30 (ING-010) | MATCH |
| tampered | integrity fail-closed (RC-001 path) | verify_integrity=False, fail-closed | MATCH |
| malformed_unknown_field | G2 reject/quarantine RC-001 | quarantined, RC-001 (unknown-field) | MATCH |
| malformed_duplicate | quarantine RC-001 + `duplicate_object_id` (D5) | quarantined, RC-001, `duplicate_object_id:<colliding-id>` | **MATCH (fixed this sprint)** |
| stale | fail-closed + RC-004 | validator accepted, policy permit, **no RC-004** | **★ NEGATIVE (carried) ★** |
| pip_spoof | G4 fail-closed RC-008 | block, RC-008 (RULE-POL-004) | MATCH |
| pre_marking | forced-unvalidated + RC-012 detection | accepted + `policy_binding_state_source_supplied` (RC-012) | MATCH |
| forged_parentage | quarantine + `unrecorded_parentage` | check_parent ok=False, `unrecorded_parentage` (tracklet, claimed parent) | MATCH |
| unauthorized_merge | block + segregate + RC-003, null output | segregate, RC-003, null output | MATCH |
| covered_merge | permit + HWM + kernel parentage | permit, HWM (L2,A,[X]), kernel-written parentage | MATCH |

**Net: 9 MATCH, 1 NEGATIVE (stale, disclosed).**

### Enforcement on held-out (docs/16 pass/fail crit 7)
Unauthorized cross-domain merge → segregate + RC-003 + null output; covered
same-domain merge → permit + high-water-mark label + kernel-written parentage.
No-unauthorized-merge demonstrated on held-out data.

### Guards, audit, determinism
- **GDR-014** (no-blind-report): PASS — report emits only with a guard-summary object present.
- **GDR-015** (diagnostic-read-only): PASS — no evidence/model/report written to the repo; outputs confined to scratch.
- **GDR-010** (no-bypass): rejection test DEFERRED (not implemented) — see gaps.
- **R1** chain-integrity: `verify_chain ok=true, count=94`.
- **R2** decision-sequence reconstruction / export: `record_count=94`, manifest sha-256 recompute match = **true** (FCE-REQ-AUD-003, FCE-REQ-EXP-001).
- **Determinism (LAP-EVAL-001):** two passes byte-identical = **true** (FCE-REQ-POL-001).
- **Coverage (LAP-EVAL-002):** clean_corpus→ING-010/PRV-001/MET-010; stale→ING-011; pip_spoof→SEC-002; forged→KRN-012/PRV-002; merges→KRN-011/PRV-002; determinism→POL-001; R1/R2→AUD-002/-003/EXP-001; duplicate→MET-010 (FCE-DR-SCH-004 D5).

## Verbatim negatives and disclosures

1. **stale → no RC-004 (NEGATIVE, carried; lead decision — do not fix in Sprint 14).**
   The held-out stale variant is `acquisition_timestamp=2000-01-01` (RFC3339)
   with no `object_timestamp_tick`. `RULE-ING-011` keys on the injected integer
   tick, so the freshness gate does not fire → the object is permitted, no
   RC-004. This is the direct, predicted consequence of the accepted tick-based
   freshness design. **FCE-REQ-ING-011 is PARTIALLY demonstrated:** RC-004
   fail-closed emission works on tick-based staleness (Layer 1, TST-UNT-030) but
   is **not** enforced on the RFC3339-timestamp held-out fixture. RFC3339/
   wall-clock freshness and trusted/attested time remain **H4** (deferred,
   unclaimed).

2. **malformed_duplicate → quarantine (GAP CLOSED this sprint).** The validator
   previously deferred duplicate-ID handling ("pending"); the held-out run
   surfaced it (both duplicates accepted). Fixed per lead decision under
   **FCE-DR-SCH-004 D5**: an additive, per-run, batch-level dedup wrapper around
   the untouched single-object evaluator — a repeated `object_id` in a run is
   quarantined fail-closed on the existing RC-001 path with a
   `duplicate_object_id:<id>` detection flag naming the colliding id. No new
   reason code; no change to unrelated validation. Re-run verdict = MATCH.

3. **RT-M7S14-01 (finding, carried tech-debt):** a latent dual freshness model
   exists — the pre-existing `_stale` check and the new `RULE-ING-011` — left in
   place to honour the additive constraint (retiring `_stale` would touch
   RULE-POL-001). `RULE-ING-011` fires first and behaviour is deterministic; no
   test exercises the divergence. Consolidation deferred.

4. **Boundary notes.** Freshness is computed on the injected integer tick, not
   parsed RFC3339 (flag-2). `clock_source` and `staleness_threshold` are recorded
   uniformly on decision records; determinism preserved and the audit writer's
   unknown-field refusal passed, so the fields are schema-legal (flag-3).

## FCE-DR-POC-005 criteria (1–10) result

| # | Criterion | Result |
|---|---|---|
| 1 | Pre-code decisions exist and approved | MET |
| 2 | ≥2 approved open-source families manifested/trimmed | MET (USGS + Sentinel-2) |
| 3 | Calibration/held-out split + sealed before evaluation | MET (blind seed, seal) |
| 4 | Every guard GDR-001..016 has a rejection test | **PARTIAL** — GDR-010 deferred |
| 5 | Code-correctness tests pass | MET (126 passed / 1 skip) |
| 6 | Held-out runs without changing bundle/thresholds | MET (sealed 0.2.0, no re-pin) |
| 7 | Unauthorized merge blocked on held-out | MET (segregate/RC-003) |
| 8 | Audit/provenance/export evidence for held-out decisions | MET (R1/R2, 94 records, manifest) |
| 9 | Test report maps to FCE-REQ rows | MET (coverage map) |
| 10 | Negatives, gaps, failed tests reported verbatim | MET (this report) |

Criterion 4 is partial and FCE-REQ-ING-011 held-out enforcement did not fire →
overall status **engineering progress; PoC validation gate not passed**.

## Carried to follow-on TRL work
- H4: trusted/attested time + RFC3339/wall-clock freshness (stale RC-004 on real timestamps).
- GDR-010 no-bypass rejection test.
- RT-M7S14-01: consolidate the dual freshness model (retire `_stale`).

## Trace
FCE-REQ-ING-010/-011, FCE-REQ-MET-010, FCE-REQ-PRV-001/-002, FCE-REQ-POL-001,
FCE-REQ-KRN-011/-012, FCE-REQ-SEC-002, FCE-REQ-AUD-001/-002/-003,
FCE-REQ-EXP-001, FCE-REQ-OPS-001. Guards GDR-001..016 (GDR-010 deferred).
FCE-DR-POC-004/-005, FCE-DR-SCH-004 (D5). RT-M3S6-02/-03/-05, RT-M7S14-01.
docs/16 Pass/Fail 1–10; docs/17 §5/§6.
