# 97 — B1–B3 Closure Review (documentation pass)

Records the focused documentation pass that closes the three blocking-in-text
conditions from `98_live-gate-review.md`. Docs-only. No source code, no installs,
`.claude/` untouched, core architecture unchanged except as needed to close
B1–B3.

## Closure status

| ID | Condition | Status | Verified by (later) |
|---|---|---|---|
| B1 | Authenticate and integrity-bind every PIP-sourced attribute; unverifiable attributes fail closed at G4; add THR-PIP-001 | CLOSED IN TEXT | H9 (property-based + red-team test) |
| B2 | Operator override cannot relax the no-unauthorized-merge invariant or a cross-domain/domain-mismatch block; override acts only within an already-permitted envelope | CLOSED IN TEXT | H9 |
| B3 | `policy_binding_state` is FCE-authority-set only; forced to `unvalidated` at G1; never trusted from source; schema updated | CLOSED IN TEXT | H9 |

## B1 — PIP attribute authentication and integrity (fail closed at G4)

Edits:
- `07` Model/PIP: every PIP attribute (mission, user, sensor, classification,
  domain, caveat, timestamp, network state, operational context) must be
  authenticated and integrity-bound before the PDP consumes it; unverifiable
  attribute fails closed at G4 with RC-008; never accepted on trust.
- `07` Reason-code registry: added RC-008 (unverifiable/unauthenticated PIP
  attribute; fail closed at G4).
- `05` G4 row: pass condition now requires authenticated, integrity-verified PIP
  attributes; fail-closed on any unverifiable PIP attribute (RC-008). Added to
  the B1–B3 clarifications block.
- `04` Trust boundaries: added PIP-attributes-to-PDP (ARCH-06 to ARCH-03) as a
  first-class boundary with fail-closed at G4.
- `10` Threat register: added THR-PIP-001 (PIP attribute spoofing) with mitigation
  and detection.
- `11` Failure modes: added FM-17 (unverifiable/unauthenticated PIP attribute →
  fail closed, RC-008).

Requirement note: this pass references FCE-REQ-SEC-001 and FCE-REQ-POL-011. A
dedicated RTM requirement for PIP attribute authentication (e.g., a new
FCE-REQ-SEC or FCE-REQ-POL row) should be added in the next RTM update; `03` was
out of scope for this docs pass and was not edited. Tracked as a follow-up.

## B2 — Override cannot relax the merge / cross-domain block

Edits:
- `07` Policy actions: override is envelope-bounded; it can never create a permit,
  relax the no-unauthorized-merge invariant, or override a cross-domain /
  domain-mismatch block.
- `07` No-unauthorized-merge invariant: added that no override, authority, reason
  code, or PIP attribute can create the required permit P or bypass the check.
- `05` G6 row: pass condition states override acts only within an already-permitted
  envelope and cannot relax a G5 no-unauthorized-merge or cross-domain block.
- `10` Threat register: added THR-OPS-002 (override used to relax merge / cross-domain
  block) with mitigation.
- `11` Failure modes: added FM-19 (override attempts to relax merge/cross-domain →
  reject; envelope-bounded).

## B3 — `policy_binding_state` is FCE-authority-set only

Edits:
- `06` Design rules: added a rule that `policy_binding_state` (field 15) is
  FCE-authority-set only, forced to `unvalidated` at G1, and never trusted from
  source input.
- `06` Schema field 15: constraint changed to "FCE-authority-set only; forced to
  unvalidated at G1; ingested value ignored (never trusted from source)."
- `05` G1 row: pass condition forces `policy_binding_state` to `unvalidated`
  regardless of ingested value.
- `04` Trust boundaries: added object-binding-state-to-FCE boundary (ARCH-01 sets
  it; never trusted from source).
- `10` Threat register: added THR-MET-003 (source-supplied policy_binding_state
  pre-marking) with mitigation.
- `11` Failure modes: added FM-18 (pre-marking → force `unvalidated` at G1).

## Changed files (this pass)

`04_software-architecture-and-trust-boundaries.md`,
`05_seven-gate-data-flow.md`, `06_metadata-schema.md`,
`07_policy-decision-model.md`, `10_security-threat-model.md`,
`11_failure-modes-and-mitigations.md`, `98_live-gate-review.md` (status note),
and this file `97_b1-b3-closure-review.md`.

## Residual / follow-up

- H9: demonstrate B1–B3 by property-based and red-team test at TRL 4-5.
- RTM (`03`): add a dedicated PIP-attribute-authentication requirement and, if
  desired, requirement rows referencing THR-OPS-002 and THR-MET-003 in a later
  RTM update (out of scope for this docs pass).
- High-priority conditions H1–H14 in `98` remain open.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: the edits above are present in the named files.
- Assumptions: text closure is sufficient at design stage; test closure (H9)
  follows at TRL 4-5.
- Judgment: reason code RC-008 and threat/failure-mode IDs assigned here.
- Uncertainty: final RTM requirement IDs for the new controls (pending `03` update).
