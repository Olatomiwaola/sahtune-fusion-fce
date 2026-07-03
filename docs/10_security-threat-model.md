# 10 — Security and Threat Model v0 (draft)

Owner: `security-assurance-engineer` with `red-team-reviewer`.
Skill: `fce-threat-model`. ITSG-33 (CCCS) and NIST SP 800-207 cited from
primary sources — reference alignment only.

## Coverage areas (all 8)

sensor, metadata, policy engine, audit chain, operator, network, edge hardware,
update workflows.

## Threat register (baseline 16+; STRIDE and mission-specific)

| THR ID | Area | Threat | Actor | Vector | Impact | Affected REQs | Mitigations | Detection | Residual | Sev | Lik | Det | Mit maturity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| THR-MET-001 | metadata | Metadata spoofing (Tampering) | insider/external | forged labels at ingest | wrong disposition | FCE-REQ-MET-010, FCE-REQ-ING-010 | source authN at G1, integrity hash, fail-closed | hash mismatch, anomaly advisory | tracked | high | med | med | design |
| THR-MET-002 | metadata | Missing metadata (DoS/bypass) | any | strip mandatory fields | object stalls or bypass attempt | FCE-REQ-MET-010 | G2 completeness check, fail-closed | validator reject count | accepted | med | med | high | design |
| THR-POL-001 | policy engine | Policy conflict yields nondeterminism | misconfig | conflicting rules | inconsistent enforcement | FCE-REQ-POL-001, FCE-REQ-POL-012 | deny-overrides, ties fail-closed | property-based tests | tracked | high | low | med | design |
| THR-POL-002 | policy engine | Mid-mission policy manipulation | insider | unsigned bundle load | unauthorized permits | FCE-REQ-POL-020 | signed bundles, version pin, rollback | signature check fail | tracked | high | low | med | design |
| THR-KRN-001 | policy engine | Domain misrouting / unauthorized merge | external | craft inputs to force merge | cross-domain leak | FCE-REQ-KRN-010 | no-unauthorized-merge invariant, G5 block | merge-permit check | blocking-until-verified | high | low | med | design |
| THR-EDG-001 | edge hardware | Latency-induced overblocking | environment | resource pressure | mission delay | FCE-REQ-EDG-001 | degraded-mode budgets, TARGET tuning | latency monitor | tracked | med | med | med | design |
| THR-POL-003 | policy engine | Underblocking (missed restriction) | misconfig | permissive rule | data over-release | FCE-REQ-POL-011 | default-deny, red-team suite | red-team tests | tracked | high | low | med | design |
| THR-AUD-001 | audit chain | Audit tampering | insider | edit/delete records | lost accountability | FCE-REQ-AUD-002 | append-only, hash chain, signature placeholder | chain verification | tracked | high | low | high | design |
| THR-OPS-001 | operator | Operator misuse of override | insider | override abuse | improper release | FCE-REQ-OPS-002 | authority + reason + time limit + audit | override audit review | tracked | high | med | high | design |
| THR-SIM-001 | metadata | Dataset weakness (unrepresentative synthetic) | internal | thin scenarios | false confidence | FCE-REQ-* (V&V) | scenario coverage matrix (`09`) | coverage audit | accepted | med | med | med | design |
| THR-KRN-002 | policy engine | AI hallucination influences decision | model | bad advisory score | wrong advisory | FCE-REQ-KRN-002 | AI advisory-only, deterministic rule cite | decision cites rule ID | accepted | med | med | high | design |
| THR-EDG-002 | edge hardware | Edge failure / power loss | environment | node crash | processing halt | FCE-REQ-EDG-010 | fail-closed, safe restart, audit backpressure | health monitor | tracked | med | med | med | design |
| THR-NET-001 | network | Clock drift / manipulation | external | NTP spoof | stale-timestamp errors | FCE-REQ-POL-011 | clock_source field, freshness check, fail-closed | drift detector | tracked | med | low | med | design |
| THR-POL-004 | policy engine | Policy hot-reload failure | ops | bad bundle mid-flow | inconsistent state | FCE-REQ-POL-020 | version pin, rollback, in-flight consistency | reload health check | tracked | med | low | med | design |
| THR-NET-002 | network | Domain misrouting on release | misconfig | wrong channel | cross-domain leak | FCE-REQ-KRN-010 | channel domain match at G5/G6 | routing audit | tracked | high | low | med | design |
| THR-AUD-002 | audit chain | Log overflow / audit starvation | load | flood events | audit loss | FCE-REQ-AUD-001 | backpressure, rotation, fail-closed halt | queue-depth alarm | tracked | med | med | high | design |
| THR-UPD-001 | update workflows | Dependency / supply-chain compromise | external | tainted update | integrity loss | FCE-REQ-SEC-001 | signed updates, SBOM (reference alignment), rollback | signature/SBOM check | tracked | high | low | med | design |
| THR-SEN-001 | sensor | Source spoofing | external | impersonate sensor | poisoned inputs | FCE-REQ-ING-010, FCE-REQ-SEC-001 | mutual authN at G1, fail-closed | authN failure log | tracked | high | med | med | design |
| THR-PIP-001 | policy engine | PIP attribute spoofing (attributes drive authZ) | insider/external | forge network_state / mission / user context supplied to PDP | correctly-signed-but-wrong permit; default-deny flipped to permit | FCE-REQ-SEC-001, FCE-REQ-POL-011 | authenticate and integrity-bind all PIP attributes; unverifiable attribute fails closed at G4 (RC-008) [B1] | PIP attribute source authN check; mismatch alarm | tracked | high | med | med | design |
| THR-OPS-002 | operator | Override used to relax no-unauthorized-merge or cross-domain block | insider | authenticated override applied over a G5 block | authenticated cross-domain leak | FCE-REQ-OPS-002, FCE-REQ-KRN-010 | override confined to already-permitted envelope; cannot create a permit or relax the invariant (B2) | override audit reconciled against merge invariant | tracked | high | low | high | design |
| THR-MET-003 | metadata | Source-supplied policy_binding_state pre-marking | external/insider | ingest object pre-marked validated | validation/handling skipped | FCE-REQ-MET-010 | policy_binding_state is FCE-authority-set only; forced unvalidated at G1; ingested value ignored (B3) | ingest reset check; state-transition audit | tracked | high | low | high | design |

## Reference alignment (not a compliance claim)

Mitigations map, for reference only, to ITSG-33 control families (e.g., access
control, audit and accountability, system and information integrity) and to
NIST SP 800-207 zero-trust tenets (per-request authZ, assume-breach,
least-privilege). Citations are to primary sources; no certification is claimed.

## Residual-risk summary

One item (THR-KRN-001, unauthorized merge on a trust boundary) is marked
blocking-until-verified: it stays blocking until the no-unauthorized-merge
invariant is demonstrated by property-based and red-team tests. All others are
tracked or accepted at v0 pending V&V. THR-PIP-001, THR-OPS-002, and THR-MET-003
were added to close blocking-in-text conditions B1, B2, and B3 (see
`97_b1-b3-closure-review.md`); their mitigations are specified in text and remain
tracked until demonstrated by red-team test.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: 8 areas covered; 16+ baseline risks present; fail-closed per mode.
- Assumptions: likelihood/severity ratings are pre-test estimates.
- Judgment: ranking and mitigation maturity ("design" = not yet tested).
- Uncertainty: real attacker capability; ratings firm up after red-team tests.
