# 11 — Failure Modes and Mitigations v0 (draft)

Owner: `test-evaluation-engineer` with `security-assurance-engineer`.
Every failure mode resolves to a fail-closed disposition.

## Principle

Missing, malformed, expired, ambiguous, or unverifiable input at any gate fails
closed. No failure mode degrades to permit-by-default.

## Failure-mode table (FMEA-style)

| FM ID | Failure mode | Cause | Effect if unmitigated | Detection | Mitigation (fail-closed) | Trace |
|---|---|---|---|---|---|---|
| FM-01 | Missing mandatory metadata | dropped field at ingest | undefined disposition | G2 completeness check | quarantine, RC-001 | FCE-REQ-MET-010 |
| FM-02 | Malformed metadata | schema violation | parser error | G2 schema validation | reject, RC-001 | FCE-REQ-MET-010 |
| FM-03 | Expired/stale timestamp | clock drift, replay | old data treated as fresh | G3 freshness check | quarantine, RC-004 | FCE-REQ-POL-011 |
| FM-04 | Ambiguous classification | unresolved label | inconsistent decision | G3/G4 resolvability check | quarantine + human review, RC-005 | FCE-REQ-POL-012 |
| FM-05 | Unauthorized cross-domain merge | crafted inputs | cross-domain leak | G5 merge-permit check | block + segregate, RC-003 | FCE-REQ-KRN-010 |
| FM-06 | Policy conflict / tie | conflicting rules | nondeterminism | property-based tests | deny-overrides; tie fails closed | FCE-REQ-POL-001 |
| FM-07 | Unsigned/invalid policy bundle | bad update | unauthorized permits | signature verification | reject bundle, rollback | FCE-REQ-POL-020 |
| FM-08 | Audit write failure | store full/slow | lost accountability | queue-depth/health monitor | halt release at G7 | FCE-REQ-AUD-001 |
| FM-09 | Audit chain break | tamper/corruption | non-replayable | chain verification | flag, fail-closed, forensic export | FCE-REQ-AUD-002 |
| FM-10 | Resource exhaustion at edge | CPU/mem/thermal | dropped processing | Degraded-Mode Manager | fail-closed, safe queue | FCE-REQ-EDG-010 |
| FM-11 | Network loss mid-flow | link down | partial routing | health monitor | hold at gate, no partial release | FCE-REQ-EDG-010 |
| FM-12 | AI advisory unavailable/wrong | model error | missing advisory | decision cites rule ID | proceed deterministically without AI | FCE-REQ-KRN-002 |
| FM-13 | Override without preconditions | operator error/abuse | improper release | G6 precondition check | reject override, RC-007 required | FCE-REQ-OPS-002 |
| FM-14 | Invalid downgrade proof | bad transformation | improper downgrade | G6 proof check | reject downgrade, RC-006 required | FCE-REQ-POL-012 |
| FM-15 | Source authentication failure | spoof/misconfig | poisoned inputs | G1 authN | reject/quarantine source | FCE-REQ-SEC-001 |
| FM-16 | Accelerator path anomaly | ARCH-14 fault | corrupted preprocess | integrity check at G1 | discard, re-ingest via CPU path | FCE-REQ-ING-010 |
| FM-17 | Unverifiable/unauthenticated PIP attribute | spoofed or unauthenticated context source | wrong permit at G4 | G4 attribute authN/integrity check | fail closed, deny, RC-008 (B1) | FCE-REQ-SEC-001, FCE-REQ-POL-011 |
| FM-18 | Source-supplied policy_binding_state pre-marking | ingested `validated` flag | validation/handling skipped | G1 authority reset | force `unvalidated` at G1; ignore ingested value (B3) | FCE-REQ-MET-010 |
| FM-19 | Override attempts to relax merge / cross-domain block | operator override abuse | authenticated cross-domain leak | G6 envelope check vs merge invariant | reject; override confined to already-permitted envelope (B2) | FCE-REQ-KRN-010, FCE-REQ-OPS-002 |

## Degraded-mode constraint classes (all 6)

compute limits, storage limits, network loss, degraded power, high CPU load,
thermal constraints. Fail-closed behaviour is verified per class in `12`
(TRL 4-5 exit) and traced to FCE-REQ-EDG-010.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: every failure mode maps to a fail-closed disposition and a reason code.
- Assumptions: detection mechanisms are feasible on the target hardware.
- Judgment: the FMEA decomposition and mitigation choices.
- Uncertainty: detection latency under real load (TARGET until measured).
