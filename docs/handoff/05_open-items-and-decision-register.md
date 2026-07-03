# 05 — Open Items and Decision Register

Consolidated open inputs, maturity items, and decisions needed. Sources: `00`
(OPEN-*), `98` (H/L conditions), `97` (B1–B3 closure).

## Open inputs
| ID | Item | Impact | Needed for |
|---|---|---|---|
| OPEN-01 | Verbatim DND IDEaS solicitation text absent | RTM outcome cells are paraphrased anchors | GATE-A / M1 |
| OPEN-02 | Project-taxonomy → named-handling-level mapping (e.g., Protected B target) | Policy labels use project taxonomy only | M2 / M3 |
| OPEN-03 | Edge hardware SKU unconfirmed (Jetson-class assumed) | Benchmarks stay TARGET | TRL 4-5 / M8 |

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
| L1 | Gate or remove `data_origin: LIVE` at this TRL; banner keys off `data_origin` |
| L2 | Align G1 "object signature (if present)" text with the schema |
| L3 | State audit replay is read-only; mission-replay re-traverses G1–G7 |
| L4 | Keep "Protected B" as reference-only external target; re-check vs solicitation |
| L5 | Capture freshness/clock evaluation reference in the audit record |

## Decisions needed from Kanatir leadership
1. Provide the verbatim solicitation text (unblocks OPEN-01 / GATE-A).
2. Approve the project-taxonomy → handling-level mapping approach (OPEN-02).
3. Confirm the target edge hardware class/SKU for later benchmarking (OPEN-03).
4. Prioritize/schedule H1–H14 across TRL bands (esp. H6 crypto/key management).
5. Approve moving from TRL 1-3 (design) to TRL 4-5 (implementation/test) — this is
   the point at which code generation would first be requested; it is out of scope
   until explicitly approved.
6. Approve any external evaluation activity (e.g., NVIDIA rig) — paper-only until then.
7. Confirm no external-facing use of any artifact until the red-team claim audit is
   re-run on the final text.
