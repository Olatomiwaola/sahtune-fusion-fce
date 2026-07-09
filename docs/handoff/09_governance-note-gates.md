# 09 — Governance Note: Gate Simplification (2026-07-03)

Decision by Kanatir leadership (sole developer = leadership; recorded once so
no future chat re-blocks on it):

1. GATE ceremony collapsed. A gate is satisfied when its audit basis is
   RECOMMEND and John confirms continuation in the block chat. No separate
   declaration step. Applies to GATE-A..GATE-F.
2. GATE-A: satisfied 2026-07-03. Basis: EVD-M1 + addendum (RECOMMEND).
   Amendment check (register #1): performed 2026-07-03 against the Canada.ca
   challenge page and CanadaBuys for W7714-248676/014 — no amendments found.
   [IF YOU HAVE NOT ACTUALLY CHECKED: do it before committing this file.]
3. Register decision #5: approved 2026-07-03 — TRL 1-3 laptop PoC per
   docs/16; implementation language/tooling: Python 3.12, standard library
   plus pinned pytest only; no other dependencies without a new decision.
4. Block chats still fail closed on missing SOURCE DOCS — unchanged.
5. Chat-side audits still produce RECOMMEND / DO-NOT-RECOMMEND; a
   DO-NOT-RECOMMEND still blocks until corrections are committed — unchanged.

## GATE-B declaration — CLOSED 2026-07-06

Project-lead declaration, recorded from the M4 block chat: GATE-B is CLOSED for
schema/policy/audit coherence and TRL 1-3 code-correctness evidence, on review of
the committed basis — M2 Sprint 4 (EVD-M2, 44 tests), M3 Sprint 6 (EVD-M3, 24
tests), M4 Sprint 8 (EVD-M4, 15 audit / 83 full-suite). Sprint-close commits:
6d87c94/7dd5b15 (Sprint 7), bdc311b/340ee1f (Sprint 8).

This declaration does NOT claim: production readiness, operational deployment,
classified-processing authority, accreditation, ATO, certification, lab/edge
validation, measured performance, GATE-C, or GATE-D.

Boundaries open and carried forward: H4 trusted/attested time; H6 external
chain-head anchoring / root of trust; H7 concurrent-writer total ordering;
envelope-only hash binding; FU-M4S8-1; RT-M3S6-06; OPEN-04; M7-due register items.

GATE-D PARTIAL declared 2026-07-07 (lead declaration, in chat, M5 block).
Basis: EVD-M5 (evidence/laptop-poc/fusion_merge_report.md, as corrected by
dated annotations at 3819be0 and 119bac1) at close commit 42b70c9 —
fusion-kernel merge semantics at TRL 1-3 code-correctness only:
exact-multiset covers(), kernel-written parentage, C3 bidirectional
G5-entry cross-check, segregation and quarantine paths with correct
detection-flag routing. No production, deployment, performance, or
accreditation claim. Sprint 14 (M7 held-out validation) completes GATE-D.

GATE-C DECLARED 2026-07-08 (lead): the sealed, guarded, licence-provenanced
public-source + synthetic fixture package required by docs/16 exists — basis
EVD-M6 (evidence/laptop-poc/fixture_report.md) at the Sprint 12 close
commit; seed per FCE-DR-POC-003, bundle pin per FCE-DR-POC-004
(proj-baseline@0.2.0), locations per FCE-DR-POC-006. TRL 1-3 scope: fixture
existence and guard function only; enforcement demonstration is M7 (GATE-D).

GATE-D CLOSED 2026-07-08 (lead declaration). Sprints 10 (M5 merge evaluator) and 14 (M7 two-layer harness + sealed held-out run) both DONE. No-unauthorized-merge / fusion enforcement demonstrated by test at TRL 1-3 on calibration and sealed held-out fixtures (EVD-M5, EVD-M7). This attests Sprint 10+14 completion and the enforcement demonstration only; it is NOT accreditation, ATO, or operational authority, and the FCE-DR-POC-005 PoC-validation status remains "engineering progress; PoC validation gate not passed" (criterion 4 GDR-010 deferred; FCE-REQ-ING-011 held-out RC-004 not enforced, H4).
