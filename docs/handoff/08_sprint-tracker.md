# 08 — Sprint Tracker (global numbering)

Owner: `fce-lead-systems-architect`. Repo home: `docs/handoff/08_sprint-tracker.md`.
This is the single reference for: which sprint we are in, what it produces,
where it runs, and how long it should take. Update the Status column at the end
of every sprint chat — this file is the pointer, the block docs (`14`, `15`)
remain the detailed source of truth.

## Numbering rule

Sprints are numbered globally and consecutively: each mission block owns two.
M1 = Sprints 1–2, M2 = Sprints 3–4, M3 = Sprints 5–6, M4 = Sprints 7–8,
M5 = Sprints 9–10, M6 = Sprints 11–12, M7 = Sprints 13–14 (TRL 1-3 scope),
M8 = Sprints 15–16, M9 = Sprints 17–18 (design-only at TRL 1-3).
Older documents that say "M2 Sprint 2" mean global Sprint 4 — the mapping is
always: global = (block number − 1) × 2 + block-local sprint.

## Effort estimates

All durations are ENGINEERING JUDGMENT planning estimates for one developer
working with Claude (chat for design/review, Claude Code for repo/code work),
in focused working days. They are internal planning figures — never schedule
commitments, never proposal claims. Rule of thumb: design/spec sprints run
0.5–1 day; PoC/code sprints run 1–2 days; the fixture sprint runs 1–2 days
including data download and trimming.

## Tracker

| Sprint | Block | Objective | Key outputs | Runs in | Est. effort | Gate | Status |
|---|---|---|---|---|---|---|---|
| 1 | M1 | Replace paraphrased outcome anchors with verbatim solicitation text; draft finalized RTM rows with acceptance criteria | Verbatim outcome registry in `02`/`03` with Canada.ca citation; 21 RTM rows (20 original + FCE-REQ-KRN-011 added by accountability review; count corrected by EVD-M1 audit, RU-05); live-source verification evidence | Chat (this Project) + Claude Code apply | 0.5–1 day | — | DONE 2026-07-03 (incl. accountability-review fixes, commit 4637107) |
| 2 | M1 | Coverage audit: ESS 6/6, DES 4/4 (FCE-DES-01/03 confirmed), all 21 rows singular/testable/correct shall-should, verification methods reviewed | Coverage report (EVD-M1), gap list, GATE-A recommendation | Chat, then Claude Code commit | 0.5–1 day | GATE-A | DONE 2026-07-03 — EVD-M1 at evidence/trl_1_3/EVD-M1_coverage-report.md; RU-02..RU-04 committed (RTM v0.2, 22 rows, FCE-REQ-EDG-011 added); GATE-A audit basis: RECOMMEND; leadership declaration pending |
| 3 | M2 | Ratify FCE-DR-SCH-001/002 and freeze the 15-field schema at v0.2.0; confirm taxonomy mapping approach (OPEN-02); fail-closed at G2 | Schema v1 freeze record, provenance model spec, validation-rule list, PoC file plan | Chat | 0.5–1 day | — | DONE 2026-07-03 — schema frozen v0.2.0; FCE-DR-SCH-001/002 authored+ratified; RULE-VAL-001..018 issued; LAP-UNIT-006..009 minted; PoC file plan issued (Python 3.12, stdlib + pinned pytest per decision #5); RT-M2S3-01..05 open, non-blocking |
| 4 | M2 | Implement minimal schema-validation PoC and tests (valid object, missing field, malformed, source-supplied policy_binding_state) | Schema validator PoC, fixtures, test output (EVD-M2) | Claude Code | 1–2 days | GATE-B (partial) | DONE 2026-07-04 — validator PoC + fixtures; 44+ tests from .venv (Python 3.12.13, pytest 9.1.0); EVD-M2 at evidence/laptop-poc/unit_test_report.md; FCE-DR-SCH-003 recorded; integrity-hash verification deferred to M4 (FU-M2S3-1); GATE-B partial |
| 5 | M3 | Finalize deterministic default-deny PDP/PEP/PAP/PIP model: 11 actions, reason codes incl. RC-008, deny-overrides, B1 PIP auth, B2 override envelope | Policy model v1, rule examples, evaluator file plan | Chat | 0.5–1 day | — | DONE 2026-07-05 — all Sprint 5 artifacts committed (49c4c4f + close addendum 509cbf6, hash recorded in trailing pointer commit); FU-M2S4-1 closed (PROJ-LEVEL-2 mapping, lead concurrence 2026-07-05); RT-M3S5-02/-03 open non-blocking (EVD-M3 obligations per FU-M3S5-1). Sprint 6: OPEN. |
| 6 | M3 | Implement machine-readable policy fixture + local deterministic evaluator returning permit/restrict/block/quarantine/review | Policy evaluator PoC, determinism tests, PIP-spoof and override red-team tests (EVD-M3) | Claude Code | 1–2 days | GATE-B (partial) | DONE 2026-07-05 (artifacts f48229e, hash recorded in trailing pointer commit) — policy evaluator PoC (src/fce_poc/policy, 7 modules) + JSON bundle/PIP fixtures; 24 policy tests / 68 full-suite pass from .venv (Python 3.12.13, pytest 9.1.0); RULE-POL-001..006 / TST-POL-001..006, G1 RC-009..012, determinism (FCE-REQ-POL-001), registry+taxonomy guard (sha-256 pin + D6 set-equality); EVD-M3 at evidence/laptop-poc/policy_eval_report.md; RT-M3S5-02/-03 open non-blocking (injected clock H4 / RC-011 mechanism-simulated H3-H4 per FU-M3S5-1); no OPA, no network. GATE-B partial (awaits Sprint 8). |
| 7 | M4 | Finalize 18-field audit schema, 9 event classes, hash-chain semantics, replay spec, export/manifest shape | Audit schema v1, replay spec, PoC file plan | Chat | 0.5–1 day | — | DONE 2026-07-06 (close commit 6d87c94) — audit record schema v1 (18 common fields + closed per-class event_detail, 9 classes, requiredness matrix, CANON-1 hash chain, replay R1/R2/R3, JSONL export + manifest); FCE-DR-AUD-001 + FCE-DR-SCH-004 RATIFIED; RTM v0.4 (FCE-REQ-ING-011, 24 rows); RT-M4S7 findings 01–05 (none blocking); register: FU-M2S3-1/-3 closed, FU-M4S7-1..3 opened. No implementation code (per lead constraint; canonical.py lands Sprint 8). Sprint 8: OPEN — blocked until this close commit + pointer commit land. |
| 8 | M4 | Implement JSONL audit emission + provenance parent-link capture for accepted/rejected/transformed/fused objects | Audit writer PoC, sample JSONL, replay check (EVD-M4) | Claude Code | 1–2 days | GATE-B closes when Sprints 4, 6, 8 all done | DONE 2026-07-06 (close commit bdc311b) — audit writer PoC (src/fce_poc/audit: canonical/envelope_integrity/records/writer/chain/replay/export/demo + provenance/links) + schema file; CANON-1 hash chain, tail-verify, R1+R2 replay, JSONL export + manifest; deterministic sample chain evidence/laptop-poc/audit_sample.jsonl (8 records, R1+R2 verified); 15 audit tests (T1–T15) / 83 full-suite pass from .venv (Python 3.12.13, pytest 9.1.0); EVD-M4 at evidence/laptop-poc/audit_report.md; register FU-M4S7-1..3 closed; RT-M4S7-03/-04 hooks landed (T11, T7). GATE-B CLOSED 2026-07-06 (Sprints 4, 6, 8 all DONE; declaration in docs/handoff/09 governance note). |
| 9 | M5 | Finalize fusion-kernel interface, high-water-mark propagation, explicit-permit merge check, segregation-on-block — tested against FCE-REQ-KRN-011 | Fusion-kernel spec, merge decision model | Chat | 0.5–1 day | — | DONE 2026-07-06 (close commit bc97289) — fusion-kernel merge semantics spec (docs/18): ARCH-08 sole fusion authority, kernel-written parentage, C1–C3 (bidirectional G5-entry cross-check), MERGE-PERMIT permitted_combinations (docs/07), docs/04 ARCH-07 pure-function amendment, docs/05 G5 wording+trace, RTM v0.5 (FCE-REQ-KRN-012, 25 rows, V1–V7 mapped), RT-M5S9 findings 01–06 dispositioned (none blocking), register updated (RT-M3S6-06 design-level closure). Sprint 10: OPEN — blocked until this close commit + pointer commit land. |
| 10 | M5 | Implement merge evaluation over 2+ parents: permitted same-domain merge + blocked cross-domain merge with RC-003 and audit | No-merge PoC, blocked-merge evidence (EVD-M5) | Claude Code | 1–2 days | GATE-D (partial) | DONE 2026-07-06 (close commit 42b70c9) — fusion merge evaluator PoC (src/fce_poc/fusion: permits/labels/crosscheck/kernel) + merge_permits fixture; V1–V7 + RT-M5S9-01/-02/-03/-05 hooks implemented; 11 fusion tests / 98 full-suite pass from .venv (Python 3.12.13, pytest 9.1.0); EVD-M5 at evidence/laptop-poc/fusion_merge_report.md; RT-M3S6-06/H1 test closure recorded (V3/V4/V7); kernel-written parentage, C3 bidirectional cross-check, exact-multiset covers(). GATE-D PARTIAL opened (Sprint 14 completes it). |
| 11 | M6 | Finalize four scenario specs (Joint ISR, Maritime, Tactical Edge, UAV) with embedded conflicts; confirm source choices under OPEN-04 | Scenario library, trim protocol, split plan, expected dispositions | Chat | 0.5–1 day | — | DONE 2026-07-07 (close commit c8cfefd) — scenario library finalized as docs/09 v1 (four scenarios, embedded M2–M5 conflict coverage, seven-variant matrix incl. forged parentage; RC-002→block ruling; items 2.4/2.5 added); FCE-DR-SCH-005 RATIFIED; RT-M6S11 01–05 dispositioned (none blocking, claim audit clean); FCE-DR-POC-003 RESOLVED (blind seed) + FCE-DR-POC-006 RATIFIED; rule 10 ratified. Sprint 12: OPEN — network-approval scope to be set at Sprint 12 open. |
| 12 | M6 | Download, trim, manifest, split, and seal fixtures: 2 approved open-source families + synthetic red-team variants (tampered, malformed, stale, PIP spoof, pre-marking, unauthorized merge) | Source manifest, trim report, calibration + sealed held-out fixture sets, coverage matrix (EVD-M6) | Claude Code | 1–2 days | GATE-C | DONE 2026-07-08 (close commit 707048a) — public-source fixture package sealed: manifest w/ licence provenance R1→R4 + supersession record; 208 candidate pairs (widening not fired); 70/30 split under blind seed (POC-003); held-out sealed (aggregate 059829241e…954ed63e) w/ pinned bundle proj-baseline@0.2.0 (POC-004 resolved); seven variants; 106 tests green; RC 12/12 · flags 4/4 · guards 7/7 · items 17/20 (3.1–3.3 → M7 harness); EVD-M6 at evidence/laptop-poc/fixture_report.md; GATE-C DECLARED (docs/handoff/09). M6 block complete; M7 opens in a new chat anchored to the pointer commit. |
| 13 | M7 | Finalize bidirectional V&V matrix across unit/integration/property-based/explainability/red-team classes; every requirement ≥1 test; every GDR guard has a rejection test | V&V matrix, test-harness file plan (target file `docs/17_vv-plan.md`) | Chat | 0.5–1 day | — | DONE 2026-07-08 (design) — docs/17_vv-plan.md v0.1: bidirectional V&V matrix (RTM v0.5 25/25 requirements each ≥1 verification method; guards GDR-001..016 16/16 rejection tests; docs/09 v1 conflict items 20/20, runtime items 3.1–3.3 mapped to simulated degraded-mode harness conditions); two-layer harness defined (L1 code-correctness / L2 sealed held-out); FCE-DR-POC-005 RECOMMENDED (docs/16 criteria 1–10; crit-6 bound to the seal re-pin protocol) — lead ratification pending before Sprint 14; RT-M3S6-02/-03/-05 formalized (TST-PRP-011 3-way lattice, TST-PRP-001 full-tuple breadth ext, TST-UNT-030 RC-004 emission; anti-replay residual = H4); Scenario 4 covers() BLOCKED fail-closed pending bundle_proj-baseline_0.2.0.json read-back (explicit pre-evaluation re-pin fallback per seal protocol); red-team RT-17-01..04 dispositioned, none blocking; GATE-B CLOSED / GATE-C DECLARED preconditions satisfied. Close hash recorded in trailing pointer commit. (design commit 6c794c4) |
| 14 | M7 | Implement and run the two-layer harness: code-correctness tests, then the sealed held-out validation run; report negative results verbatim | Runnable harness, guard rejection tests, code-correctness report, held-out validation report, coverage report (EVD-M7) | Claude Code | 1–2 days | GATE-D closes when Sprints 10 + 14 done | DONE 2026-07-08 — two-layer harness on sealed proj-baseline@0.2.0: Layer 1 code-correctness 126 passed / 1 skip (GDR-010 deferred); Layer 2 single sealed held-out pass = 9/10 oracle MATCH, 1 disclosed NEGATIVE (stale -> no RC-004; RFC3339/H4, carried); FCE-DR-SCH-004 D5 duplicate-ID detection added (gap closed); no-unauthorized-merge enforced on held-out (segregate/RC-003; covered permit/HWM/parentage); R1+R2 verified (94 records, manifest recompute match); determinism byte-identical (LAP-EVAL-001); GDR-014/015 PASS; coverage mapped (LAP-EVAL-002). EVD-M7 at evidence/laptop-poc/heldout_eval_report.md. FCE-DR-POC-005: 9/10 MET, crit-4 PARTIAL -> verdict "engineering progress; PoC validation gate not passed". RT-M7S14-01 (dual freshness model) carried. GATE-D CLOSED (Sprints 10 + 14 DONE). close commit 1102e2b. |
| 15 | M8 | Define benchmark metric set (per-gate + end-to-end latency, throughput, memory, CPU/GPU, thermal, power) — all TARGET; six degraded-mode classes with fail-closed responses | Benchmark plan (TARGET-labelled) | Chat | 0.5–1 day | — | Design-only at TRL 1-3; pending GATE-D |
| 16 | M8 | Baseline-vs-candidate protocol on named hardware; NVIDIA decision records DR-001…007 outside the compliance path | Degraded-mode protocol, NVIDIA decision records | Chat (execution deferred to TRL 4-5 approval) | 0.5–1 day | GATE-E | Pending Sprint 15; hardware blocked on OPEN-03 |
| 17 | M9 | Evidence index (EVD-*) per TRL band; TRL exit-criteria gap audit | Evidence pack index, gap report | Chat | 0.5–1 day | — | Pending GATE-D |
| 18 | M9 | Compliance matrix (clause → evidence), claim screen, red-team claim audit, website-safe and proposal-safe language | Compliance matrix, proposal-ready sections | Chat | 1 day | GATE-F | Pending Sprint 17 |

## Roll-up

TRL 1-3 execution scope is Sprints 1–14 (M1–M7): roughly 11–18 focused days at
the estimates above — call it 3–4 calendar weeks for one developer at sustained
part-time pace, before M8/M9 design sprints. ENGINEERING JUDGMENT; re-estimate
after Sprint 4, the first code sprint, which calibrates the PoC velocity.

## Standing rules per sprint chat

One chat per mission block: both sprints of that block run sequentially in the
same chat, design sprint committed via Claude Code before the build sprint
begins; a new block always starts a new chat. Every sprint chat opens by reading this tracker plus
the block entry in `15`, runs its role blocks per the one-chat rule, ends with
the role handoff plus a one-line tracker status update to commit via Claude
Code. Chat drafts REPO-UPDATE notes; Claude Code writes and runs. A sprint is
DONE only when its evidence artifact (EVD-*) exists at the referenced path and
this tracker's Status column is updated in the repo.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: block objectives, outputs, gates, and dependencies are drawn from
  `docs/14` and `docs/15` at commit 4637107; Sprint 1 completion state is
  verified against the repo.
- Assumptions: OPEN-04 (data sources) and OPEN-02 (taxonomy mapping) resolve
  without schema rework; one developer plus Claude at part-time pace.
- Judgment: the global numbering convention, all effort estimates, and the
  suggested USGS + Sentinel-2 source pairing.
- Uncertainty: PoC sprint velocity unknown until Sprint 4; OPEN-03 hardware
  timing affects only Sprints 15–16.
