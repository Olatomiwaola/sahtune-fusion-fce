# EVD-M1 — M1 Sprint 2 Coverage Audit Report

Proposed repo home: `evidence/trl_1_3/EVD-M1_coverage-report.md` (per `fce-evidence-pack`).
Produced by: `requirements-traceability-engineer` role block, M1 Sprint 2 chat, 2026-07-03.
Audit subjects: `docs/03_rtm.md` (RTM v0.1, post-fix), `docs/02_capability-decomposition.md`,
`docs/handoff/08_sprint-tracker.md`, `docs/handoff/05_open-items-and-decision-register.md`
as supplied to the Sprint 2 chat. This report proposes; nothing herein is applied to the repo.
GATE-A is declared by Kanatir leadership only — never by this report.

---

## 1. Row-count reconciliation (FACT — discrepancy)

- FACT: `docs/handoff/08_sprint-tracker.md` (Sprint 1 row) and the Sprint 2 brief state "17 RTM rows (16 original + FCE-REQ-KRN-011)".
- FACT: the supplied `docs/03_rtm.md` contains **21** unique requirement rows: FCE-REQ-KRN-001, FCE-REQ-POL-001, FCE-REQ-KRN-002, FCE-REQ-KRN-011, FCE-REQ-ING-010, FCE-REQ-POL-011, FCE-REQ-MET-010, FCE-REQ-KRN-010, FCE-REQ-POL-012, FCE-REQ-PRV-001, FCE-REQ-PRV-002, FCE-REQ-AUD-001, FCE-REQ-AUD-002, FCE-REQ-EXP-001, FCE-REQ-AUD-003, FCE-REQ-EDG-001, FCE-REQ-POL-020, FCE-REQ-EDG-010, FCE-REQ-OPS-001, FCE-REQ-OPS-002, FCE-REQ-SEC-001. No duplicate IDs.
- UNCERTAINTY: whether the supplied `03_rtm.md` matches repo HEAD at commit 4637107, or whether the tracker count is stale. This chat cannot read the repo; reconciliation must be done in Claude Code (see REPO-UPDATE RU-05).
- Impact on audit: none on coverage direction (21 ≥ 17; no outcome loses coverage), but the tracker is the single sprint-state reference and its evidence-count claim must match the artifact.

## 2. Outcome coverage audit (Sprint 2 objective 1)

| Outcome | Verbatim anchor present in `02`/`03` | Requirement rows (Source column) | Coverage |
|---|---|---|---|
| FCE-ESS-01 | Yes (Canada.ca citation) | FCE-REQ-KRN-001, FCE-REQ-POL-001, FCE-REQ-KRN-002, FCE-REQ-KRN-011, FCE-REQ-SEC-001 | COVERED (≥1 shall) |
| FCE-ESS-02 | Yes | FCE-REQ-KRN-011, FCE-REQ-ING-010, FCE-REQ-POL-011, FCE-REQ-MET-010, FCE-REQ-SEC-001 | COVERED (≥1 shall) |
| FCE-ESS-03 | Yes | FCE-REQ-KRN-010, FCE-REQ-POL-012 | COVERED (≥1 shall) |
| FCE-ESS-04 | Yes | FCE-REQ-PRV-001, FCE-REQ-PRV-002 | COVERED (≥1 shall) |
| FCE-ESS-05 | Yes | FCE-REQ-AUD-001, FCE-REQ-AUD-002 | COVERED (≥1 shall) |
| FCE-ESS-06 | Yes | FCE-REQ-EXP-001, FCE-REQ-AUD-003 | COVERED (≥1 shall) |
| FCE-DES-01 | Yes — **explicitly confirmed present** | FCE-REQ-EDG-001 | COVERED (should) |
| FCE-DES-02 | Yes | FCE-REQ-POL-020 | COVERED (should) |
| FCE-DES-03 | Yes — **explicitly confirmed present** | FCE-REQ-EDG-010 | COVERED (should; see FLAG-02) |
| FCE-DES-04 | Yes | FCE-REQ-OPS-001, FCE-REQ-OPS-002 | COVERED |

**Result: Essential 6/6. Desired 4/4. FCE-DES-01 and FCE-DES-03 explicitly confirmed.**

FCE-REQ-KRN-011: present; Source = FCE-ESS-01, FCE-ESS-02; **Capability = CAP-06 confirmed**; design elements ARCH-08, G5; verification = property-based test + red-team test; acceptance criterion covers no-unauthorized-merge, segregate disposition with RC-003, audit event, B2 override non-relaxation, and high-water-mark label propagation with full parent linkage. Trace confirmed against `02` (CAP-06 → ARCH-08) and the register (B2, RC-003).

Capability-to-outcome mapping in `02` is consistent with the RTM Source column; no orphan capabilities affect M1 scope (CAP-12 is the optional NVIDIA evaluation track, correctly outside the compliance path).

## 3. Row-by-row audit (Sprint 2 objective 2)

Criteria per row: singular; testable; correct shall/should; exactly one ID; ≥1 verification method from the approved legend; acceptance criterion complete and non-clipped.

| Req ID | Singular | Testable | shall/should correct | One ID | Legend-valid method(s) | Acceptance criterion complete | Verdict |
|---|---|---|---|---|---|---|---|
| FCE-REQ-KRN-001 | Yes | Yes | shall — correct (ESS) | Yes | integration test, property-based test — valid | Yes | PASS |
| FCE-REQ-POL-001 | Yes | Yes | shall — correct | Yes | property-based test — valid | Yes | PASS |
| FCE-REQ-KRN-002 | Compound (3 clauses: advisory-only, no sole-AI dependence, cite rule ID) | Yes | shall — correct | Yes | inspection, red-team test — valid | Yes | PASS with note N-01 |
| FCE-REQ-KRN-011 | Compound (no-merge + segregate-and-audit) | Yes | shall — correct | Yes | property-based test, red-team test — valid | Yes; note criterion overlaps OPS-002 (B2) and CAP-03 (label propagation) — see N-02 | PASS with note N-02 |
| FCE-REQ-ING-010 | Yes | Yes | shall — correct | Yes | integration test — valid | Yes | PASS |
| FCE-REQ-POL-011 | Compound but coherent (taxonomy value + no-GoC-marking guard) | Yes | shall — correct | Yes | analysis, unit test — valid | Yes | PASS with note N-01 |
| FCE-REQ-MET-010 | Yes | Yes | shall — correct | Yes | unit test — valid | Yes | PASS |
| FCE-REQ-KRN-010 | Compound (checks at two points + auto-disposition) | Yes | shall — correct | Yes | integration test — valid | Yes | PASS with note N-01 |
| FCE-REQ-POL-012 | Yes | Yes | shall — correct | Yes | property-based test, red-team test — valid | Yes | PASS |
| FCE-REQ-PRV-001 | Yes | Yes | shall — correct | Yes | unit test, integration test — valid | Yes | PASS |
| FCE-REQ-PRV-002 | Yes | Yes | shall — correct | Yes | property-based test — valid | Yes | PASS |
| FCE-REQ-AUD-001 | Yes | Yes | shall — correct | Yes | integration test, inspection — valid | Yes | PASS |
| FCE-REQ-AUD-002 | Yes | Yes | shall — correct | Yes | property-based test, red-team test — valid | Yes | PASS |
| FCE-REQ-EXP-001 | Yes | Yes | shall — correct | Yes | integration test — valid | Yes; correctly limits language to accreditation-support | PASS |
| FCE-REQ-AUD-003 | Yes | Yes | shall — correct | Yes | integration test, analysis — valid | Yes | PASS |
| FCE-REQ-EDG-001 | Yes | Yes (as plan-level at TRL 1-3) | should — correct (DES) | Yes | benchmark — valid but see FLAG-03 (not TRL 1-3 producible alone) | Yes; TARGET discipline correct | FLAG-03 |
| FCE-REQ-POL-020 | Compound; fail-closed rejection clause hosted inside a should | Yes | should — correct for capability; fail-closed clause conditional-binding, see N-03 | Yes | integration test, red-team test — valid | Yes | PASS with note N-03 |
| FCE-REQ-EDG-010 | Compound | Yes | **INCORRECT — mixed modal: "should operate … and shall fail closed" in one row** | Yes | benchmark — valid; **"edge/degraded test" — NOT on approved legend** | Yes; TARGET discipline correct | **FLAG-02, FLAG-04** |
| FCE-REQ-OPS-001 | Yes | Yes | should — correct | Yes | **"explainability test" — NOT on approved legend** | Yes | **FLAG-01** |
| FCE-REQ-OPS-002 | Compound (four preconditions + fail-closed) | Yes | shall under a DES outcome — acceptable as conditional-binding safeguard (binding whenever override capability exists), see N-03 | Yes | red-team test, integration test — valid | Yes | PASS with note N-03 |
| FCE-REQ-SEC-001 | Yes | Yes | shall — correct | Yes | red-team test, inspection — valid | Yes | PASS |

No clipped or truncated cell text was found anywhere in the supplied RTM; all acceptance criteria are complete sentences.

### Flags (require correction before GATE-A)

- **FLAG-01 (FCE-REQ-OPS-001):** verification method "explainability test" is not in the approved legend (`03` legend; shared constraint 8). Correction: assign "inspection, integration test" in the RTM; retain explainability testing as a V&V test class in the planned `docs/17_vv-plan.md`, or amend the legend by decision record — leadership/architect choice.
- **FLAG-02 (FCE-REQ-EDG-010):** mixed modal verbs — "should operate within defined SWaP and compute limits … and shall fail closed under resource exhaustion." A binding fail-closed invariant (shared constraint 3) hosted inside a should-row risks being read as optional. No existing shall row covers fail-closed-under-resource-exhaustion (FCE-REQ-POL-012 covers ambiguous policy conditions only). Correction: split — EDG-010 retains the should (SWaP/compute TARGET operation); the resource-exhaustion fail-closed behavior moves to a new binding row. **Gap flagged, not filled: the new requirement ID must be minted by this role in Claude Code against repo HEAD; no ID is invented here.**
- **FLAG-03 (FCE-REQ-EDG-001):** sole verification method "benchmark" cannot produce TRL 1-3 evidence — execution is blocked on OPEN-03 (hardware SKU unconfirmed) and deferred to TRL 4-5 per the tracker (Sprints 15–16). Correction: add "analysis" (of the TARGET-labelled benchmark plan) as the TRL 1-3 method; benchmark retained for later execution. Acceptance criterion already plan-scoped, so this is a method-column fix only.
- **FLAG-04 (FCE-REQ-EDG-010):** second verification method "edge/degraded test" is not on the approved legend. Correction: map to "bench test" (degraded-mode bench test at TRL 1-3 is laptop-simulated; true edge deferred with OPEN-03), or amend the legend by decision record.
- **FLAG-05 (tracker/RTM count):** see §1. "17 RTM rows" vs 21 REQ IDs must be reconciled in the repo before the tracker is relied on as evidence pointer for GATE-A.

### Notes (no correction mandated at TRL 1-3 — ENGINEERING JUDGMENT)

- **N-01:** FCE-REQ-KRN-002, FCE-REQ-KRN-010, FCE-REQ-POL-011 are compound but each expresses a single coherent invariant; splitting at TRL 1-3 would add trace overhead without verification benefit. Revisit at V&V planning (M7).
- **N-02:** FCE-REQ-KRN-011's acceptance criterion embeds override non-relaxation (B2, also in FCE-REQ-OPS-002) and high-water-mark propagation (CAP-03 territory). Keep, but the M7 V&V matrix should cross-reference one property test from both rows to prevent divergent duplicate criteria.
- **N-03:** Convention to record (one line in `03`'s legend section): fail-closed and safeguard clauses attached to Desired-outcome capabilities are conditional-binding — binding whenever the capability is present (applies to FCE-REQ-POL-020's rejection clause and FCE-REQ-OPS-002's shall).

## 4. Verification-method TRL 1-3 review (Sprint 2 objective 3)

| Method (as used in RTM) | Rows | TRL 1-3 evidence producible? |
|---|---|---|
| inspection | KRN-002, AUD-001, SEC-001 | Yes — document/PoC inspection |
| analysis | POL-011, AUD-003 | Yes |
| unit test | POL-011, MET-010, PRV-001 | Yes — laptop PoC (Sprints 4/6/8) |
| integration test | KRN-001, ING-010, KRN-010, PRV-001, AUD-001, EXP-001, AUD-003, POL-020, OPS-002 | Yes — laptop PoC pipeline |
| property-based test | KRN-001, POL-001, KRN-011, POL-012, PRV-002, AUD-002 | Yes — laptop PoC |
| red-team test | KRN-002, KRN-011, POL-012, AUD-002, POL-020, OPS-002, SEC-001 | Yes — fixture-based (M6 red-team variants) |
| benchmark | EDG-001, EDG-010 | **No at TRL 1-3** — TARGET plan only; execution blocked on OPEN-03; rows stay TARGET-labelled (correctly labelled today; FLAG-03 adds the plan-level method) |
| "explainability test" | OPS-001 | Off-legend — FLAG-01 |
| "edge/degraded test" | EDG-010 | Off-legend — FLAG-04 |

## 5. Untraceable items

None. Every REQ ID traces to at least one outcome anchor, one CAP-* from `02`, and at least one ARCH-*/G* design element that exists in `02`'s capability table. All reason codes referenced in acceptance criteria (RC-001, RC-003, RC-005, RC-008) and conditions (B1–B3) appear in the supplied docs; no new IDs are introduced by this report.

## 6. GATE-A recommendation

**DO-NOT-RECOMMEND in the artifact's current state**, expected to convert to a clean RECOMMEND basis once the correction set is committed. Reasons:

1. FLAG-02: a fail-closed invariant is currently hosted in a should-row — a modal-discipline defect touching shared constraint 3; GATE-A should not be declared over it.
2. FLAG-01 / FLAG-04: two verification methods are off the approved legend, breaking shared constraint 8 traceability as written.
3. FLAG-05: the tracker's evidence-count claim (17) does not match the audited artifact (21); the tracker is the single sprint-state reference and must be accurate before it anchors a gate.
4. FLAG-03: FCE-DES-01's row needs a TRL 1-3-producible method added so the outcome is not unverifiable at this band.

Coverage itself is clean (ESS 6/6, DES 4/4, DES-01/03 confirmed, KRN-011 → CAP-06 confirmed) and no defect requires re-architecture — all corrections are RTM/tracker edits plus one new requirement ID minted in Claude Code. Leadership should also note decision-register item #1 (confirm no later solicitation amendments) is a stated pre-GATE-A leadership check independent of this audit. GATE-A is declared by Kanatir leadership only.

## 7. Facts / Assumptions / Judgment / Uncertainty

- **FACT:** coverage results (§2), row-audit results (§3), method review (§4), row count of 21, absence of clipped cells, presence of verbatim Canada.ca-cited anchors in the supplied docs.
- **ASSUMPTION:** the supplied copies of `02`, `03`, `05`, `08` faithfully reflect repo state at or after commit 4637107 (this chat cannot read the repo); Sprint 1's live-source verification of 2026-07-03 stands and is not re-performed here.
- **ENGINEERING JUDGMENT:** N-01–N-03 dispositions; the split-vs-reword remedy for FLAG-02; the DO-NOT-RECOMMEND framing with an identified path to RECOMMEND.
- **UNCERTAINTY:** which side of the 17-vs-21 discrepancy is stale; possible later solicitation amendments (leadership decision #1); OPEN-02/OPEN-03 may later refine POL-011 and EDG-* rows without affecting this audit's coverage result.


---

## Addendum — 2026-07-03 (post-correction)

RU-02, RU-03, RU-04, and the N-03 legend convention were committed (RTM v0.2).
FCE-REQ-EDG-011 minted at HEAD to host the resource-exhaustion fail-closed
invariant; RTM row count is now 22 (FACT, verified by grep at commit time).
Off-legend methods resolved by reassignment (ASSUMPTION recorded: legend
amendment was declined in favour of the lighter reassignment; reversible by
decision record). The Section 6 GATE-A position accordingly converts from
DO-NOT-RECOMMEND to RECOMMEND as the audit basis. Declaration remains with
Kanatir leadership, including decision-register item #1 (amendment check).
