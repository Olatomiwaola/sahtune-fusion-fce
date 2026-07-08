# 17 — Verification & Validation Plan (V&V Matrix and Enforcement Demonstration)

Owner: `test-evaluation-engineer` with `requirements-traceability-engineer`
(bidirectional audit), `policy-engineer` (Scenario 4 coverage / re-pin),
`red-team-reviewer` (findings-only), `audit-forensics-engineer`,
`sensor-fusion-engineer`. Skills: `fce-test-and-evaluation`,
`fce-requirements-traceability`, `fce-documentation-style`.

v0.1 (M7 Sprint 13, design): this is the bidirectional V&V plan for the Sahtune
Fusion Compliance Engine (FCE). It maps every requirement in RTM v0.5 (25 rows)
to at least one test or stated verification method, gives every guard
GDR-001..016 a rejection test, maps every `docs/09` v1 conflict item (all 20,
including the three runtime items) to a test or an explicit harness condition,
carries the M3-Sprint-6 red-team obligations into concrete tests, specifies the
explainability tests, ratifies the FCE-DR-POC-005 pass/fail criteria, and
defines the two-layer harness that Sprint 14 implements and runs. Design only —
no implementation code, no fixture touch, no held-out read at Sprint 13.

## Claim boundary (binding on this document and on EVD-M7)

This plan is a **specification of tests and a harness**. It demonstrates nothing
by itself. Enforcement-demonstration claims become legal only in EVD-M7, and
only for what the sealed held-out run in Sprint 14 actually shows. The RC-004
stale case exists as a fixture from M6; its **emission demonstration** is the M7
obligation discharged here as a test spec and executed in Sprint 14
(RT-M3S6-05). Substantive anti-replay / trusted-time remains **H4** (open, TRL
4-5), and this plan claims neither. Standards (ITSG-33, NIST SP 800-207, NIST AI
RMF, XACML, OPA/Rego, W3C PROV, RFC 8785, SLSA) are reference alignment only. AI
is advisory only; every pass/fail authority in this plan is deterministic.
Honest negative results from the Sprint 14 run are a **required output**, not a
block failure.

---

## §0 — Seal + anchor verification status (open of M7)

Sprint 13 runs in the chat/design environment, which has **no repo, git, or
fixture access** and, by held-out discipline (GDR-014 no-blind-report, GDR-015
diagnostic-read-only), **must not** open `data/fixtures/heldout/*` before the
Sprint 14 evaluation. Therefore the seal/anchor recomputations are Claude Code
operations at the Sprint 14 boundary. What was verifiable in chat has been
verified; the rest is specified for raw execution.

### Verified in chat (no fixture touch)

- **Aggregate-digest formula reproduces.** Recomputing sha-256 over the two
  seal-recorded `hash␠␠path` lines, `LC_ALL=C sort`, trailing newline, yields
  `059829241e527eb1aa09e3ff8ce8abafed1eeee445e04474f32ac267954ed63e` —
  identical to the sealed aggregate and to the precondition value. The seal
  record is internally self-consistent, and the exact method is now pinned
  (`LC_ALL=C sort`, trailing newline, shasum -a 256) so the on-disk recompute
  has no ambiguity. **This does not verify held-out file contents** — only that
  the seal's recorded per-file hashes combine to the recorded aggregate.
- **Bundle SHA cross-reference.** The precondition names the bundle SHA to
  confirm; the seal record records `BUNDLE_SHA =
  6a830b2474a362f799fab045f0f2c23ca0b9d117c8f1e1d0acc5b51a69c53502` for
  `data/fixtures/policy/bundle_proj-baseline_0.2.0.json`. The on-disk recompute
  must equal this (also closes the M6 chat's truncated-hash item).

### To run raw in Claude Code before any fixture touch (fail closed on mismatch)

```
# 1. Anchor
git log --oneline -5
#   expect HEAD = 284c3fa (Sprint 12 pointer); chain visible:
#   707048a (M6 close) <- 507d3c5 (Sprint 12 build) <- 91d4960 (Sprint 12 open)
git status -sb            # state push sync; report if changed

# 2. Bundle SHA (no held-out touch)
shasum -a 256 data/fixtures/policy/bundle_proj-baseline_0.2.0.json
#   expect 6a830b2474a362f799fab045f0f2c23ca0b9d117c8f1e1d0acc5b51a69c53502

# 3. Held-out aggregate — SPRINT 14 EVALUATION BOUNDARY ONLY.
#    Hashing file bytes for the seal check is not a diagnostic content read,
#    but it is still deferred to the Sprint 14 run open to honor GDR-015 and
#    keep a single documented held-out-read point.
LC_ALL=C sh -c 'shasum -a 256 data/fixtures/heldout/* | LC_ALL=C sort | shasum -a 256'
#   expect 059829241e527eb1aa09e3ff8ce8abafed1eeee445e04474f32ac267954ed63e
```

Any mismatch anywhere = **STOP, report raw, no work** (precondition).

### Fail-closed source-document gaps at Sprint 13 open

Two source docs named in the block inputs were **not available to the design
environment**: `docs/07_policy-decision-model.md` and the **contents** of
`data/fixtures/policy/bundle_proj-baseline_0.2.0.json` (the actual
`permitted_combinations` / registry / lattice). Consequences, fail closed:

- §4 (Scenario 4 tuple-coverage `covers()` verification) is specified in full
  but its **final match check is BLOCKED** pending the bundle's actual
  `permitted_combinations` enumeration. It does not silently pass. Resolution is
  a Claude Code read-back of the bundle (or the permits pasted into chat),
  performed **before** the held-out run, under the seal re-pin protocol.
- Registry/lattice references below are taken from the derived docs that quote
  them (`docs/08`, `docs/18`, `docs/09`, coverage matrix), labelled as such;
  they are not a substitute for `docs/07` at ratification and are flagged where
  they matter.

---

## §1 — FCE-DR-POC-005 ratification (pass/fail criteria)

`[ROLE: test-evaluation-engineer]` lead. Candidate = `docs/16` Pass/Fail
criteria 1–10. Reviewed against the block state; recommendation to lead (John)
to ratify **before Sprint 14** (register target "ratify before M7 Sprint 2").

| # | Criterion (docs/16, verbatim intent) | Sprint-14 objective evidence | Ratify? |
|---|---|---|---|
| 1 | All pre-code decisions exist and are approved | FCE-DR-POC-001..007 resolved/ratified per the registers; POC-005 ratified here | YES |
| 2 | ≥2 approved open-source data families manifested and trimmed | OSD-01 USGS + OSD-04 Sentinel-2, sealed; EVD-M6 source manifest | YES |
| 3 | Calibration and held-out fixtures split and sealed before evaluation | Sprint 12 seal (aggregate `059829…63e`, blind seed) | YES |
| 4 | Every guard GDR-001..016 has a rejection test | §3c below (16/16 mapped) | YES |
| 5 | Code-correctness tests pass | Layer 1: 106 baseline + matrix-new tests green from `.venv` | YES |
| 6 | Held-out validation runs without changing bundle or thresholds | Layer 2: single pass under sealed `proj-baseline@0.2.0`; re-pin only by protocol | YES |
| 7 | Unauthorized merge blocked on held-out fixtures | §3d items 1.1/2.1 + GDR-011; fusion-decision RC-003/segregate record | YES |
| 8 | Audit/provenance/export evidence emitted for held-out decisions | R1+R2 verified; export-class record + manifest sha-256 | YES |
| 9 | Test report maps results to FCE-REQ-* rows | §3b reverse trace; coverage report in EVD-M7 | YES |
| 10 | Negative results, gaps, failed tests reported verbatim | GDR-014 binds; EVD-M7 verbatim-negative rule | YES |

**Ratification recommendation (T&E):** ADOPT `docs/16` criteria 1–10 verbatim as
FCE-DR-POC-005, with one binding reading recorded at ratification: criterion 6's
"without changing the policy bundle or thresholds" is satisfied **only** under
the seal re-pin protocol (explicit, pre-evaluation, recorded; no silent
evaluation; no post-seal mutation). The "engineering progress; PoC validation
gate not passed" status (docs/16) is the mandatory outcome label if any of 1–10
fails on the held-out run. **Lead ratification required before Sprint 14.**

---

## §2 — Two-layer harness definition (Sprint 14 build target)

Per `docs/16` §"Direct Answer" and §5, the proof claim is split. The harness has
two layers with a hard ordering; Layer 2 never runs if Layer 1 is red.

**Layer 1 — code correctness (calibration fixtures only, no held-out read).**
Full existing suite (106 green baseline: Python 3.12.13, pytest 9.1.0) plus the
matrix-new tests specified in §3. Proves the machinery is wired and guards fire
on bad inputs. Uses calibration fixtures only — the only development data.
Cannot, and does not, make a concept-validation claim.

**Layer 2 — sealed held-out run (the enforcement demonstration).** Single pass.
Bundle `proj-baseline@0.2.0` exactly as sealed. Held-out fixtures read for the
**first time**. Every held-out object traverses G1→G7. For every object the run
records disposition, reason codes, and detection flags and compares them to the
`docs/09` v1 expected dispositions (§5). Audit chain R1 (chain integrity) + R2
(decision-sequence reconstruction) verified. Guard rejection evidence collected.
Coverage report produced. Results — **including every negative** — reported
verbatim in EVD-M7 (chat-authored per rule 9). GATE-D closes when Sprints 10 + 14
are both DONE.

**Harness-level guards (bind at this block).**
- **GDR-014 no-blind-report:** the harness structurally cannot emit a test/eval
  report unless a guard-summary object exists for the run.
- **GDR-015 diagnostic-read-only:** diagnostic/inspection mode cannot write any
  model/evidence artifact; the held-out read happens once, in evaluation mode,
  at the documented Layer-2 open.
- **GDR-016 normalization identity:** fixture-builder path and runtime ingestion
  path share the same CANON-1 envelope-normalization function (LAP-RED-006).

---

## §3 — Bidirectional V&V matrix

### §3a — Requirement → verification (RTM v0.5, 25/25)

Every row has ≥1 test or a stated verification method. "Layer" = harness layer;
"M8" = benchmark verification deferred to the M8 design sprints (method stated,
not executed at TRL 1-3). Fail-closed cases are marked FC.

| REQ ID | Requirement (short) | Class(es) | Test / method IDs | Layer | Notes |
|---|---|---|---|---|---|
| FCE-REQ-KRN-001 | Recorded decision before downstream release | integration, property, FC | TST-INT-001, TST-PRP-010 (no-decision→blocked) | L1+L2 | ties GDR-010 no-bypass; item 3.3 |
| FCE-REQ-POL-001 | Deterministic decisions under pinned bundle | property | TST-PRP-001 (+RT-M3S6-02 breadth ext) | L1+L2 | full decision tuple, all classes |
| FCE-REQ-KRN-002 | AI advisory only; every decision cites a rule ID | inspection, red-team | TST-RED-001 | L1 | disable-AI cannot flip deny→permit |
| FCE-REQ-KRN-011 | No merge without explicit covering permit; block→segregate+audit | property, red-team, FC | TST-PRP-051, TST-RED-051 | L1+L2 | GDR-011; items 1.1/2.1; RC-003 override-immune |
| FCE-REQ-KRN-012 | Kernel-recorded parentage; bidirectional cross-check | property, red-team, FC | TST-PRP-052, TST-RED-052 (V3/V4/V7) | L1+L2 | forged-parentage variant; `unrecorded_parentage` |
| FCE-REQ-ING-010 | ≥2 sensor modalities traverse G1-G7 | integration | TST-INT-010 | L1+L2 | eo_ir + acoustic_like on public fixtures |
| FCE-REQ-POL-011 | ≥1 network domain + Protected-B-equiv, project taxonomy only | analysis, unit | TST-UNT-011 | L1 | no real GoC markings |
| FCE-REQ-MET-010 | Bind classⁿ/domain/caveat; reject missing mandatory fields | unit, FC | TST-UNT-010 (+ LAP-UNIT-002/007/008/009/010) | L1+L2 | G2 RC-001; malformed variant |
| FCE-REQ-KRN-010 | Checks at ingestion + fusion; auto-disposition, audited | integration | TST-INT-011 | L1+L2 | no human approval for predefined conditions |
| FCE-REQ-POL-012 | Default-deny / fail-closed on ambiguous; enqueue review | property, red-team, FC | TST-PRP-012 (V5) | L1+L2 | items 1.3/1.4; RC-005; mixed_bundle_versions |
| FCE-REQ-ING-011 | Freshness vs staleness policy; RC-004 fail-closed + audit | unit, red-team, FC | **TST-UNT-030 (RC-004 emission, RT-M3S6-05)** | L2 | stale variant; injected clock; trusted time = H4 |
| FCE-REQ-PRV-001 | Provenance for every ingested + produced object | unit, integration | TST-INT-040 | L1+L2 | source sensor ID, label, timestamps, domain |
| FCE-REQ-PRV-002 | Provenance preserved across transform/fusion (parent links) | property | TST-PRP-040 (V1) | L1+L2 | replay reaches origins, no orphans |
| FCE-REQ-AUD-001 | Audit record per policy decision (rules, action, disposition) | integration, inspection | TST-INT-050 | L1+L2 | 9 event classes; requiredness matrix |
| FCE-REQ-AUD-002 | Append-only, tamper-evident hash chain | property, red-team, FC | TST-RED-050 (edit/delete/reorder + torn tail) | L1 | whole-file substitution = H6 (disclosed) |
| FCE-REQ-EXP-001 | Export audit+lineage with integrity manifest | integration | TST-INT-060 | L2 | JSONL + manifest sha-256; no accreditation claim |
| FCE-REQ-AUD-003 | Decision sequence replayable from audit alone | integration, analysis | TST-INT-061 (R2) | L2 | read-only replay; no G1-G7 re-traverse |
| FCE-REQ-EDG-001 | End-to-end latency TARGET, named hardware | benchmark, analysis | TST-PRF-001 / EVD-BENCH-001 | **M8** | TARGET only; not executed at TRL 1-3 |
| FCE-REQ-POL-020 | Signed bundle updates without restart; reject unsigned FC | integration, red-team, FC | TST-RED-020 | L1 (partial) | signing = H6 placeholder; version-pin/rollback demoed |
| FCE-REQ-EDG-010 | SWaP/compute limits, named edge device | benchmark, analysis | TST-EDG-010 | **M8** | TARGET only |
| FCE-REQ-EDG-011 | Fail-closed across 6 degraded-mode classes | bench, red-team, FC | TST-EDG-011 (simulated) | L2 (sim) | item 3.1 resource-exhaustion harness condition |
| FCE-REQ-OPS-001 | Human-readable explanation per decision | inspection, integration | TST-EXP-001..004 (§3f) | L1+L2 | rules, attributes consumed, reason code |
| FCE-REQ-OPS-002 | Override needs authority+reason+time-limit+sig; else FC | red-team, integration, FC | TST-RED-002 (V6) | L1+L2 | items 4.1-4.4; cannot relax B2 |
| FCE-REQ-SEC-001 | Zero-trust authN/authZ on every interface; deny FC | red-team, inspection, FC | TST-RED-SEC-001 | L1 | mechanism-simulated (H3/H13 disclosed) |
| FCE-REQ-SEC-002 | Authenticate/integrity-bind PIP attrs; RC-008 at G4 FC | property, red-team, FC | TST-PRP-013, TST-RED-003 | L1+L2 | PIP-spoof variant; GDR-008 |

**Coverage: 25/25 requirements have ≥1 verification method.** 21 exercised on
the laptop PoC (Layers 1/2); 2 (FCE-REQ-EDG-001, FCE-REQ-EDG-010) carry a
benchmark method deferred to M8 by scope (TARGET, no TRL 1-3 execution — not a
gap, a stated method); FCE-REQ-POL-020 is partially exercised at L1 with signing
disclosed as H6 placeholder.

### §3b — Test → requirement (reverse trace, no orphan tests)

| Test / method ID | Class | Requirement(s) | docs/09 item(s) |
|---|---|---|---|
| TST-INT-001 | integration | FCE-REQ-KRN-001 | 3.3 (bypass) |
| TST-PRP-010 | property (FC) | FCE-REQ-KRN-001 | 3.3 |
| TST-PRP-001 (+RT-M3S6-02) | property | FCE-REQ-POL-001 | all (determinism) |
| TST-RED-001 | red-team | FCE-REQ-KRN-002 | — |
| TST-PRP-051 / TST-RED-051 | property/red-team | FCE-REQ-KRN-011 | 1.1, 2.1 |
| TST-PRP-052 / TST-RED-052 | property/red-team | FCE-REQ-KRN-012 | S1 forged parentage (V3/V4/V7) |
| TST-INT-010 | integration | FCE-REQ-ING-010 | S1 heterogeneous |
| TST-UNT-011 | unit | FCE-REQ-POL-011 | — |
| TST-UNT-010 (+LAP-UNIT-002/007/008/009/010) | unit (FC) | FCE-REQ-MET-010 | 3.4, S3 malformed |
| TST-INT-011 | integration | FCE-REQ-KRN-010 | 4.x auto-disposition |
| TST-PRP-012 | property (FC) | FCE-REQ-POL-012 | 1.3, 1.4 |
| TST-UNT-030 | unit/red-team (FC) | FCE-REQ-ING-011 | 2.3, 3.x stale (RC-004) |
| TST-INT-040 | unit/integration | FCE-REQ-PRV-001 | all (provenance) |
| TST-PRP-040 | property | FCE-REQ-PRV-002 | 1.5 |
| TST-INT-050 | integration | FCE-REQ-AUD-001 | all (audit) |
| TST-RED-050 | property/red-team (FC) | FCE-REQ-AUD-002 | — |
| TST-INT-060 | integration | FCE-REQ-EXP-001 | 4.x export |
| TST-INT-061 (R2) | integration | FCE-REQ-AUD-003 | 4.x replay |
| TST-PRF-001 / EVD-BENCH-001 | benchmark (M8) | FCE-REQ-EDG-001 | — |
| TST-RED-020 | integration/red-team | FCE-REQ-POL-020 | — |
| TST-EDG-010 | benchmark (M8) | FCE-REQ-EDG-010 | — |
| TST-EDG-011 | bench/red-team (sim, FC) | FCE-REQ-EDG-011 | 3.1 |
| TST-EXP-001..004 | inspection/integration | FCE-REQ-OPS-001 | 2.4 explanation |
| TST-RED-002 | red-team/integration (FC) | FCE-REQ-OPS-002 | 4.1-4.4 |
| TST-RED-SEC-001 | red-team | FCE-REQ-SEC-001 | S2 spoof (RC-011) |
| TST-PRP-013 / TST-RED-003 | property/red-team (FC) | FCE-REQ-SEC-002 | S1 PIP spoof |
| TST-POL-007 | unit | FCE-REQ-POL-011, FCE-REQ-OPS-001 | 2.4 |
| TST-POL-008 | unit | FCE-REQ-POL-011, FCE-REQ-AUD-001, FCE-REQ-PRV-001 | 2.5 |

No orphan tests: every listed test binds ≥1 RTM requirement. LAP-* fixture/guard
tests bind through the GDR map (§3c) and the requirement rows above.

### §3c — Guard → rejection test (GDR-001..016, 16/16)

Every guard has a positive AND a negative (rejection) test that proves it fires
(docs/16 §4). GDR-001..006 + GDR-016 were demonstrated firing at M6 (7/7,
EVD-M6); this plan carries them forward and adds GDR-007..015.

| Guard | Guard function | Rejection test (fires on) | Test ID | Where |
|---|---|---|---|---|
| GDR-001 | Source-provenance | Missing source URL/hash aborts fixture build | LAP-RED-002a | M6 ✓, re-run L1 |
| GDR-002 | Licence/terms | Missing licence note marks source unapproved | LAP-RED-002b | M6 ✓ |
| GDR-003 | Trim-manifest | Build aborts without row counts/filter params | LAP-RED-002c | M6 ✓ |
| GDR-004 | Split integrity | Held-out ID in calibration aborts evaluation | LAP-RED-001 | M6 ✓, binds L2 |
| GDR-005 | Data-presence | Empty/all-null modality aborts before report | LAP-RED-005 | M6 ✓ |
| GDR-006 | Envelope-version | Unsupported envelope version rejected | LAP-UNIT-004 / GDR-006 hook | M6 ✓ |
| GDR-007 | Binding-state authority | Source `policy_binding_state=validated` forced `unvalidated` | LAP-UNIT-003 + pre_marking variant | L1+L2 |
| GDR-008 | PIP-auth | Unauthenticated PIP attr fails closed RC-008 | LAP-RED-003 / TST-RED-003 | L1+L2 |
| GDR-009 | Policy-version | Missing bundle version aborts held-out run | GDR-009 hook / TST-RED-020 | L2 open |
| GDR-010 | No-bypass | Object without complete G1-G7 trace blocked | TST-PRP-010 / TST-INT-001 | L1+L2 |
| GDR-011 | No-merge | Unauthorized merge blocked and audited | LAP-INT-003 / TST-RED-051 | L1+L2 |
| GDR-012 | Override-envelope | Override cannot relax no-merge/cross-domain block | LAP-RED-004 / TST-RED-002 (V6) | L1+L2 |
| GDR-013 | Audit-write | Missing audit write blocks release/test pass | LAP-INT-004 | L1+L2 |
| GDR-014 | No-blind-report | Report refused unless guard summary exists | harness self-test | L1+L2 |
| GDR-015 | Diagnostic-read-only | Diagnostic mode cannot write model/evidence | harness self-test | L1+L2 |
| GDR-016 | Normalization identity | Builder vs runtime envelope divergence fails build | LAP-RED-006 | M6 ✓, L1 |

### §3d — docs/09 v1 conflict item → test / harness condition (20/20)

Coverage matrix at M6 = 17/20 static-representable; items 3.1–3.3 are **runtime
conditions**, mapped here to explicit harness conditions (not static fixtures).

| Item | Conflict | Expected disposition (registry) | Test / harness condition |
|---|---|---|---|
| 1.1 | Cross-domain merge, no covering combination | block+segregate, RC-003 (override-immune) | TST-RED-051 / unauthorized_merge variant |
| 1.2 | Caveat/domain mismatch w/ channel | block, RC-002, override-immune | TST-POL (RC-002 block) calibration |
| 1.3 | Ambiguous classification | quarantine+review, RC-005 | TST-PRP-012 / calibration |
| 1.4 | Mixed pinned bundle versions | quarantine+review, RC-005 + mixed_bundle_versions | TST-PRP-012 (V5) |
| 1.5 | Permitted same-domain merge (positive) | permit; kernel parentage + HWM | TST-PRP-051 / TST-PRP-040 (**covers() must enumerate — §4**) |
| 2.1 | Cross-domain merge, no permit (maritime) | block+segregate, RC-003 | TST-RED-051 |
| 2.2 | Caveat violation vs channel | block, RC-002, override-immune | TST-POL (RC-002 block) |
| 2.3 | Stale acquisition timestamp | fail-closed, **RC-004 (emission = M7)** | **TST-UNT-030 (RT-M3S6-05)** |
| 2.4 | Broad release, mixed caveat channels | restrict — partial permit; reason_codes empty | TST-POL-007 |
| 2.5 | Higher-class object on lower channel | route-to-higher-domain (delivery only) | TST-POL-008 |
| 3.1 | Resource exhaustion during decision | fail-closed; no permit-by-default | **harness: simulated resource-limit class (TST-EDG-011)** |
| 3.2 | Audit-write starvation at G7 | pipeline halts; object does not proceed | **harness: audit-write starvation condition (GDR-013/TST-INT-004 ext)** |
| 3.3 | Network loss mid-flow | complete under pinned bundle or fail closed; no bypass | **harness: network-loss condition (GDR-010/TST-PRP-010)** |
| 3.4 | G1-reject family (schema_version/LIVE/pre-marking) | reject RC-009 / reject RC-010 / forced-unvalidated RC-012 | LAP-UNIT-004/006 + pre_marking variant |
| 4.1 | Override, all four preconditions | accepted; audited, RC-007 | TST-RED-002 branch A |
| 4.2 | Override missing a precondition | rejected fail-closed; audited | TST-RED-002 branch B |
| 4.3 | Override vs RC-003 blocked merge (immunity) | rejected; block stands (B2) | TST-RED-002 (V6) |
| 4.4 | Override vs RC-005 / unrecorded_parentage quarantine | both rejected (envelope excludes quarantine) | TST-RED-002 / RT-M5S9-05 pair |
| 4.5 | Downgrade w/ valid authority + proof | authorized downgrade, RC-006 | TST-INT (downgrade class) |
| 4.6 | Downgrade w/ invalid/missing proof | rejected fail-closed | TST-INT (downgrade FC) |

**20/20 mapped.** Items 3.1/3.2/3.3 are explicit runtime harness conditions in
Layer 2 (degraded-mode simulation at TRL 1-3), discharging the M6 "3.1–3.3 →
M7 harness" deferral.

### §3e — Carried red-team obligations (register, due M7)

`[ROLE: test-evaluation-engineer]` formalizes the three carried items into
concrete tests. Substantive fixes that are H-items remain H-items — only the
demonstrations/tests land here.

| RT ID | Obligation | Formalized as | Residual |
|---|---|---|---|
| RT-M3S6-02 | Determinism hash-compare breadth beyond permit+reject | TST-PRP-001 **breadth extension**: repeated evaluation compares the **full decision tuple** (decision, reason_codes[], enforcement_action, disposition, detection_flags) byte-identical across ALL disposition classes exercised on held-out + calibration — block, restrict, quarantine, route, downgrade, override, not only permit/reject | none (test-level closure) |
| RT-M3S6-03 | Lattice test beyond pairwise | TST-PRP-011 (new): D3 severity-lattice total-order property over **≥3-way** combinations — transitivity and idempotence of the high-water-mark/most-restrictive combination; ties fail closed | none (test-level closure) |
| RT-M3S6-05 | RC-004 emission (stale fixtures exist; demo lands M7) | **TST-UNT-030**: stale variant → fail-closed disposition RC-004 **with an emitted ingestion/policy audit event**; verified on held-out at Layer 2 | **substantive anti-replay = H4** (trusted/attested time, TRL 4-5) — explicitly not claimed |

### §3f — Explainability tests (FCE-REQ-OPS-001)

| Test | Checks | Trace |
|---|---|---|
| TST-EXP-001 | Explanation lists rule ID(s), attributes consumed, decision, disposition, reason code, human-readable | FCE-REQ-OPS-001 |
| TST-EXP-002 | Partial-permit (item 2.4) explanation carries the permitted subset in the FCE-REQ-OPS-001 explanation and the rules-fired citation — **never** in policy-decision `event_detail` (closed D2 sub-schema unchanged; RT-M6S11-01) | FCE-REQ-OPS-001, FCE-REQ-POL-011 |
| TST-EXP-003 | Block/quarantine explanation names the override-immunity where it applies (RC-002/RC-003) without implying an override path exists | FCE-REQ-OPS-001, FCE-REQ-KRN-011 |
| TST-EXP-004 | Explanation cites the deterministic rule ID even when advisory AI is disabled (no explanation depends on AI output alone) | FCE-REQ-OPS-001, FCE-REQ-KRN-002 |

---

## §4 — Scenario 4 tuple-coverage verification (`covers()` vs sealed bundle)

`[ROLE: policy-engineer]` (no web tools). **STATUS: BLOCKED — fail closed.**
The final match check needs the sealed bundle's actual `permitted_combinations`
(`bundle_proj-baseline_0.2.0.json`), which was not available to the design
environment. The verification is fully specified here; it is resolved by a
Claude Code read-back of the bundle (or the permits pasted into chat) **before**
the held-out run.

**What must be checked.** Scenario 4 (UAV) constructs target-track estimates as
**derived lifecycle objects in-run by ARCH-08** from eo_ir + uas_telemetry
observation fixtures (docs/09 §Scenario 4; amendment A2). For the deliberate-
positive path — a valid fused/derived track must exist so the override (4.1–4.4)
and downgrade (4.5–4.6) cases have a real object to act on — the merge that
constructs that track must be covered by an **exact-multiset** entry in
`permitted_combinations` (docs/18 §4: no wildcards, no cardinality shortcuts;
[T1,T2] does not cover [T1,T1]).

**Procedure (deterministic).**
1. From the S4 calibration fixtures, extract the (classification, domain,
   release_caveat) label tuple of every observation object that enters a
   deliberate-positive S4 merge, and the multiset presented to `covers()`.
2. For each such multiset M, check `∃ e ∈ permitted_combinations : multiset(e) == M`
   (exact equality, per docs/18 §4 / RT-M5S9-01 semantics).
3. Any S4 **deliberate-positive** merge whose M is **not** enumerated ⇒ the
   held-out (and calibration positive) run would false-negative the positive
   case — exactly the failure mode caught pre-seal for item 1.5 in bundle
   v0.1.0. Resolution is **not** silent: a `policy-engineer` block proposes an
   explicit, pre-evaluation, recorded **re-pin** (new bundle version, e.g. an
   `MP-S4-*` entry mirroring the `MP-S1-15-PUBLIC-PAIR` precedent), ratified by
   the lead before the held-out run; the sealed `0.2.0` is never mutated in
   place (seal re-pin protocol, verbatim).
4. S4 **negative** cases (4.3 override-vs-RC-003 block) intentionally present an
   **uncovered** cross-domain multiset — those must remain uncovered (RC-003).
   Do not "fix" a negative case by adding a permit.

**Deliverable when the bundle is available (Claude Code, pre-run):**
`shasum -a 256 data/fixtures/policy/bundle_proj-baseline_0.2.0.json` (confirm
`6a830b…c53502`), then dump `permitted_combinations` raw and run steps 1–3.
Record the result and any re-pin decision in the seal record + decision register
before Layer 2.

**Fallback (declared now):** if step 3 finds an uncovered deliberate-positive S4
tuple, the pre-evaluation re-pin is the sanctioned path; the held-out run does
not proceed under a bundle that would false-negative a positive case, and it
never proceeds silently under a different bundle than the one recorded.

---

## §5 — Expected dispositions (closed registry; Layer-2 oracle)

The held-out run compares each object's (disposition, reason_codes, detection
flags) to this table, sourced from `docs/09` v1 and the closed RC registry as
quoted in `docs/08`/`docs/18`. Reason codes ⊆ RC-001..012; dispositions ∈ D3
lattice.

| Case | Expected disposition | Reason code / flag |
|---|---|---|
| tampered (label/hash post-hash mutation) | G2/G3 integrity fail-closed | RC-001 path |
| malformed (unknown field) | G2 reject | RC-001 (FCE-DR-SCH-003) |
| malformed (duplicate object_id) | quarantine | RC-001 path + `duplicate_object_id` |
| stale (beyond staleness policy) | fail-closed | **RC-004 (emission demonstrated at M7)** |
| PIP spoof (unauthenticated attr) | G4 fail-closed | RC-008 |
| pre-marking (source-supplied binding) | accept-with-detection; forced unvalidated | RC-012 + `source_supplied_policy_binding_state` |
| unauthorized merge (no covering combo) | block + segregate; null output | RC-003 (override-immune) |
| forged parentage (claimed parents) | quarantine | `unrecorded_parentage` (docs/18 §1) |
| permitted same-domain merge (1.5) | permit; kernel parentage + HWM | reason_codes empty (clean permit) |
| ambiguous classification (1.3) | quarantine + review | RC-005 |
| mixed bundle versions (1.4) | quarantine + review | RC-005 + `mixed_bundle_versions` |
| partial-permit broad release (2.4) | restrict | reason_codes empty; rules-fired cited |
| route higher-class on low channel (2.5) | route-to-higher-domain (delivery only) | reason_codes empty unless registry requires |
| spoofed AIS-like source (S2) | G1 reject | RC-011 (MECHANISM-SIMULATED) |
| override, all 4 preconditions (4.1) | accepted; audited | RC-007 |
| override missing precondition (4.2) | rejected fail-closed; audited | override-class |
| override vs RC-003 block (4.3) | rejected; block stands | B2 / override_immutable |
| override vs quarantine (4.4) | rejected | RULE-POL-005 envelope check |
| downgrade valid proof (4.5) | authorized downgrade | RC-006 (authority + proof) |
| downgrade invalid proof (4.6) | rejected fail-closed | downgrade preconditions |

---

## §6 — Sprint 14 execution protocol (REPO-UPDATE, Claude Code)

1. Open: run §0 anchor + bundle-SHA checks raw; then §4 bundle-permits read +
   S4 `covers()` check; record re-pin decision if any (before any held-out read).
2. Layer 1: full suite + matrix-new tests (TST-PRP-011, TST-PRP-001 breadth ext,
   TST-UNT-030, TST-EXP-001..004, GDR-007..015 rejection tests) from `.venv`
   (Python 3.12.13, pytest 9.1.0). Must be green before Layer 2.
3. Layer 2: single sealed held-out pass under `proj-baseline@0.2.0`; §0 held-out
   aggregate recompute at run open; every object G1→G7; compare to §5; R1+R2;
   guard rejection evidence; coverage report.
4. EVD-M7 chat-authored per rule 9 at `evidence/laptop-poc/heldout_eval_report.md`
   (+ code-correctness report), verbatim negatives included; guard summary
   present (GDR-014).
5. Tracker rows 13→14 status updated; GATE-D closes when Sprints 10 + 14 DONE.
6. New chat for M8, anchored to the M7 pointer hash.

---

## §7 — Facts / Assumptions / Judgment / Uncertainty

- **Facts:** RTM v0.5 25-row set and verification-method assignments; GDR-001..016
  and the M6 7/7 demonstrated set (EVD-M6); docs/09 v1 20 conflict items and
  expected dispositions; docs/08 event classes / requiredness / replay R1-R2;
  docs/18 exact-multiset `covers()` and cross-check semantics; seal record
  values and the reproduced aggregate-digest formula; carried RT-M3S6-02/-03/-05
  obligations and their register due-date (M7).
- **Assumptions:** the calibration fixtures suffice to green Layer 1 without a
  held-out read; the sealed bundle is loadable unchanged at Sprint 14; STAC/USGS
  fixtures already sealed need no re-fetch (no network in M7).
- **Engineering judgment:** the test-ID scheme and class assignments; mapping
  items 3.1–3.3 to simulated degraded-mode harness conditions rather than static
  fixtures; treating FCE-REQ-EDG-001/-010 as method-stated/M8-deferred rather
  than M7 gaps; the RT-M3S6-02 "full decision tuple across all classes" breadth
  definition.
- **Uncertainty:** Scenario 4 `covers()` result is **unresolved pending the
  bundle contents** (§4, fail closed); whether a S4 re-pin is required is that
  read-back's call; the exact count of matrix-new tests that green on first
  Layer-1 run; held-out outcomes are unknown until the single Layer-2 pass and
  are reported verbatim regardless.

---

## Requirement trace

FCE-REQ-KRN-001/-002/-010/-011/-012, FCE-REQ-POL-001/-011/-012/-020,
FCE-REQ-ING-010/-011, FCE-REQ-MET-010, FCE-REQ-PRV-001/-002,
FCE-REQ-AUD-001/-002/-003, FCE-REQ-EXP-001, FCE-REQ-EDG-001/-010/-011,
FCE-REQ-OPS-001/-002, FCE-REQ-SEC-001/-002. Guards GDR-001..016.
FCE-DR-POC-003/-004/-005/-006. RT-M3S6-02/-03/-05, RT-M5S9-05, RT-M6S11-01/-02.
