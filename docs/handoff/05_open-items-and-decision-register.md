# 05 — Open Items and Decision Register

Consolidated open inputs, maturity items, and decisions needed. Sources: `00`
(OPEN-*), `98` (H/L conditions), `97` (B1–B3 closure).

## Open inputs
| ID | Item | Impact | Needed for |
|---|---|---|---|
| OPEN-01 | Verbatim DND IDEaS solicitation text supplied and verified against the live Canada.ca page on 2026-07-03 (word-for-word match, all 10 outcomes; RT-M1S1-01 closed); anchors registered in `docs/02` and `docs/03` | M1 Sprint 1 unblocked; GATE-A still requires Sprint 2 coverage audit | M1 Sprint 2 / GATE-A |
| OPEN-02 | Project-taxonomy → named-handling-level mapping (e.g., Protected B target) | **RESOLVED 2026-07-04**: approach confirmed M2 Sprint 3 (documentation-level reference-only mapping, no real GoC markings); leadership decision #2 approved 2026-07-04. Enumerated registry authoring follows under FU-M2S4-1 | M2 / M3 |
| OPEN-03 | Edge hardware SKU unconfirmed (Jetson-class assumed) | Benchmarks stay TARGET | TRL 4-5 / M8 |
| OPEN-04 | Laptop PoC data-source approval: choose at least two public source families from `docs/16_laptop-poc-validation-architecture.md` | Required for source manifest, trim report, calibration/held-out fixture seal, and pre-lab validation evidence | M6 / M7 |

## B1–B3 (closed in text; test closure deferred)
| ID | Condition | Status |
|---|---|---|
| B1 | Authenticate/integrity-bind PIP attributes; fail closed at G4 (RC-008) | Closed in text (`97`); test = H9 |
| B2 | Override cannot relax no-unauthorized-merge / cross-domain block | Closed in text (`97`); test = H9 |
| B3 | `policy_binding_state` FCE-authority-set only; forced `unvalidated` at G1 | Closed in text (`97`); test = H9 |

## H1–H14 (open high-priority; before TRL 4-5 exit)
| ID | Item | Suggested owner |
|---|---|---|
| H1 | Enforce ARCH-08 as sole fusion authority; detect self-declared empty parentage | sensor-fusion / architect |
| H2 | Define and verify downgrade transformation-proof structure and authority | policy-engineer |
| H3 | Enumerate all admin/debug/maintenance/telemetry interfaces with authN/authZ | security-assurance |
| H4 | Trusted/attested time source; clock-independent anti-replay | security-assurance / edge |
| H5 | Security-critical bundle-change class forcing in-flight re-evaluation/hold | policy-engineer |
| H6 | Crypto root-of-trust and key management; audit append-only + external anchoring | security-assurance / devsecops |
| H7 | Audit-chain-writer serialization/total-order model; concurrency test | audit-forensics / test |
| H8 | Deterministic cross-object bundle-version resolution at G5 fusion | policy / architect |
| H9 | Demonstrate no-bypass and no-unauthorized-merge (and B1–B3) by test | test-evaluation |
| H10 | Anti-rollback / monotonic version-floor on updates and bundles | devsecops |
| H11 | Edge at-rest protection, secure boot, physical-tamper posture | security-assurance / edge |
| H12 | Two-person / content-review control on policy-bundle publication | policy / devsecops |
| H13 | Release-destination authN and audit-export authZ | security-assurance |
| H14 | Audit schema to log unauthenticated-source-rejection events at G1 | audit-forensics |

## L1–L5 (documentation-level; track)
| ID | Item |
|---|---|
| L1 | RESOLVED 2026-07-03 by schema v0.2.0 (`06`) and FCE-DR-SCH-002: LIVE removed at TRL 1-3, rejected fail-closed at G1; banner keys off `data_origin` in {SYNTHETIC, SYNTHETIC-DERIVED} |
| L2 | Align G1 "object signature (if present)" text with the schema |
| L3 | State audit replay is read-only; mission-replay re-traverses G1–G7 |
| L4 | Keep "Protected B" as reference-only external target; re-check vs solicitation |
| L5 | Capture freshness/clock evaluation reference in the audit record |

## M2 Sprint 3 follow-ups (schema freeze v0.2.0)

Raised by the Sprint 3 schema freeze and red-team review (RT-M2S3, non-blocking for the
v0.2.0 freeze). Sources: `docs/05_data_model/m2-schema-freeze-record.md`,
`docs/06_security/red_team_findings/RT-M2S3.md`.

| ID | Item | Owner | Due |
|---|---|---|---|
| FU-M2S3-1 | Define `integrity_hash` input domain and canonicalization (which bytes/fields are hashed); G2 integrity-check clause is untestable until then (RT-M2S3-02, freeze record field 14) | data-model-engineer | M4 |
| FU-M2S3-2 | ~~Decide unknown/extra envelope-field disposition~~ **CLOSED 2026-07-04** by FCE-DR-SCH-003 (reject fail-closed at G2 with RC-001; LAP-UNIT-010). Resolves RT-M2S3-03. | architect | done |
| FU-M2S3-3 | Define `object_id` uniqueness scope (global vs per-run/per-mission) and duplicate-ID disposition before Sprint 4 test assertions are final (RT-M2S3-01, freeze record field 1) | data-model-engineer | before Sprint 4 assertions |
| FU-M2S4-1 | Author the enumerated project-taxonomy registry in `docs/07` (classification, domain, caveat, modality value families) and add a guard that the calibration `taxonomy.json` equals the docs/07 families. **CLOSED 2026-07-05**: registry authored in `docs/07` (D6) verbatim from the verified fixture, SHA-256 `59979c4d…bec240` match; reference-only PROJ-LEVEL-2 ↔ Protected B mapping (lead concurrence 2026-07-05); taxonomy-equality guard switch specced for Sprint 6 (fixture stays hash-pinned until then). Consumed OPEN-02 / decision #2. | policy-engineer | closed 2026-07-05 |
| FU-M3S5-1 | State the H4 trusted-time (injected-clock) dependency for override expiry, and label RC-011 cases "mechanism-simulated", in EVD-M3 — EVD-M3 must not claim trusted time or source authentication demonstrated (RT-M3S5-02, RT-M3S5-03). | test-evaluation-engineer | M3 Sprint 6 |

RT-M2S3-03 and RT-M2S3-04 are resolved (see `docs/06_security/red_team_findings/RT-M2S3.md`);
FCE-DR-SCH-003 recorded in `docs/12_decision_records/`. **RT-M2S4-03 (reason-code
registry consistency) → RESOLVED** by the closed RC-001..012 registry + consistency check
in `docs/07` v1 (no orphaned codes). M3 Sprint 5 red-team findings: RT-M3S5-01 fixed
in-text, RT-M3S5-02/-03 open non-blocking (`docs/06_security/red_team_findings/RT-M3S5.md`);
FCE-DR-POL-001 (severity lattice, proposed) recorded in `docs/12_decision_records/`.

## Decisions needed from Kanatir leadership

Governance note 2026-07-03: gate ceremony collapsed per docs/handoff/09_governance-note-gates.md. Items #1 and #5 closed therein; GATE-A satisfied. Remaining items decided per-block as they become blocking.
1. Confirm whether later solicitation amendments exist before GATE-A is declared
   (OPEN-01 is resolved for M1 Sprint 1 using verified Canada.ca outcome text).
2. Approve the project-taxonomy → handling-level mapping approach (OPEN-02).
   **CLOSED 2026-07-04** — leadership decision #2 approved; approach confirmed
   M2 Sprint 3. OPEN-02 resolved; registry authoring follows (FU-M2S4-1).
3. Confirm the target edge hardware class/SKU for later benchmarking (OPEN-03).
4. Prioritize/schedule H1–H14 across TRL bands (esp. H6 crypto/key management).
5. Approve the TRL 1-3 local PoC boundary and implementation language/tooling
   before M2 Sprint 2 begins; production/operational implementation remains out
   of scope until later approval.
6. Approve the laptop PoC public data sources, trim limits, calibration/held-out
   split, and guard list in `docs/16` before M6 Sprint 2.
7. Approve any external evaluation activity (e.g., NVIDIA rig) — paper-only until then.
8. Confirm no external-facing use of any artifact until the red-team claim audit is
   re-run on the final text.
