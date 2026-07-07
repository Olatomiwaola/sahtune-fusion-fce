# 07 — Policy Decision Model v1

Owner: `policy-engineer`. Skill: `fce-policy-as-code`.
XACML PDP/PEP/PAP/PIP and OPA/Rego are reference patterns only (cite OASIS
XACML; openpolicyagent.org). No compliance claims.

v1 (M3 Sprint 5): reason-code registry closed with G1 codes and
override_immutable flags; disposition severity lattice added (FCE-DR-POL-001,
RATIFIED 2026-07-04); decision-record output contract added; RULE-POL-004..006 added;
taxonomy registry authoring in progress (leadership decision #2 approved
2026-07-04, OPEN-02 resolved; FU-M2S4-1).

M5 Sprint 9 amendment (2026-07-06): MERGE-PERMIT schema added
(permitted_combinations exact-multiset semantics per RT-M5S9-01/-03
dispositions); segregation disposition-not-transformation sentence added.
Registry and RULE-POL-002 unchanged.

## Project taxonomy disclaimer [OPEN-02]

All classification, domain, and caveat values are a PROJECT TAXONOMY for
exercising the pipeline. They are not real Government of Canada markings or
procedures. A documented mapping links the project taxonomy to named handling
targets (e.g., the Protected B target in FCE-ESS-02) without reproducing real
marking procedures.

### Enumerated taxonomy registry [D6 — authored 2026-07-05; FU-M2S4-1 closed]

Leadership decision #2 approved 2026-07-04 (OPEN-02 resolved). The enumerated
project-taxonomy value families below are authored verbatim from the verified,
hash-pinned calibration fixture (`data/fixtures/calibration/taxonomy.json`,
sha-256 `59979c4d72b79cba6dec02892cc2940d609a705a2a724b5416ec275749bec240`,
recorded in EVD-M2). This registry is now the authoritative source; the fixture's
`_provenance` note (which predates this section) is retained to preserve the
pinned hash. No real Government of Canada markings.

**Modality**

| Value |
|---|
| eo_ir |
| radar_like |
| sigint_like |
| acoustic_like |
| ais_like |
| uas_telemetry |

**Classification label**

| Value |
|---|
| PROJ-LEVEL-1 |
| PROJ-LEVEL-2 |
| PROJ-LEVEL-3 |

**Domain label**

| Value |
|---|
| DOMAIN-A |
| DOMAIN-B |

**Release caveat**

| Value |
|---|
| PROJ-CAVEAT-X |

**Reference-only mapping to named handling targets**

Documentation-level, reference-only mapping (FCE-REQ-POL-011): never a real
Government of Canada marking procedure and never an enforcement input.
PROJ-LEVEL-2 mapping selected by engineering judgment; project lead concurrence
2026-07-05.

| Project-taxonomy value | Named external target (reference only) |
|---|---|
| PROJ-LEVEL-2 | Protected B (equivalent handling target, FCE-ESS-02) |

PROJ-LEVEL-1 and PROJ-LEVEL-3 have no named external target at TRL 1-3.

**Guard spec (Sprint 6).** A taxonomy-equality guard shall assert that the
enumerated families above equal the calibration fixture's families
(`data/fixtures/calibration/taxonomy.json`). Until that guard lands the fixture
stays hash-pinned (sha-256 above); at Sprint 6 the guard switches its authority
from the pinned fixture hash to docs/07 equality (this section). Tracked:
FU-M2S4-1 (closed on authoring), guard implementation in Sprint 6.

## Model

- PDP (ARCH-03): decision. PEP (ARCH-04): enforcement at each gate.
- PAP (ARCH-05): signed, versioned bundle administration and hot-reload.
- PIP (ARCH-06): attributes — mission, user, sensor, classification, domain,
  caveat, timestamp, network state, operational context. Every PIP-sourced
  attribute must be authenticated and integrity-bound to a trusted source before
  the PDP consumes it; any unverifiable or unauthenticated attribute fails closed
  at G4 with reason code RC-008. Attributes are never accepted on trust from an
  unauthenticated caller. [B1]
- Base disposition is deny. Every rule adds a narrow, attributable permit or a
  stronger restriction.

## Policy actions (all 11 representable)

permit, restrict, block, segregate, quarantine, reject, transform,
route-to-higher-domain, require-human-review, downgrade (only with valid
authority and transformation proof), override (only with authenticated
authority, reason code, time limit, and audit signature placeholder).

Override is envelope-bounded: it acts only within an already-permitted envelope.
Override can never create a permit, relax the no-unauthorized-merge invariant, or
override a cross-domain / domain-mismatch block. A merge or cross-domain release
that lacks an explicit permit stays blocked regardless of operator authority or
reason code. [B2]

## Reason-code registry (CLOSED — v1) [D2]

Column `override_immutable` (RT-M3S5-01): true = no operator override may act
against a decision carrying this code.

| Code | Meaning | override_immutable |
|---|---|---|
| RC-001 | Missing or malformed mandatory metadata | false |
| RC-002 | Classification/domain/caveat mismatch with channel (B2) | true |
| RC-003 | No explicit permit for cross-domain merge (B2) | true |
| RC-004 | Stale or unverifiable timestamp | false |
| RC-005 | Ambiguous condition; enqueue human review | false |
| RC-006 | Authorized downgrade with valid transformation proof | false |
| RC-007 | Authenticated override within time limit (envelope-bounded; see B2) | false |
| RC-008 | Unverifiable or unauthenticated PIP attribute; fail closed at G4 | false |
| RC-009 | G1 reject: unsupported schema_version (envelope-version gate, GDR-006); fail closed before policy evaluation | false |
| RC-010 | G1 reject: unsupported data_origin (LIVE at TRL 1-3 per FCE-DR-SCH-002); fail closed before policy evaluation | false |
| RC-011 | G1 reject: source authentication failure — source_sensor_id cannot be authenticated (H14 audit hook) | false |
| RC-012 | G1 detection (non-reject): source-supplied policy_binding_state detected and forced to `unvalidated` (B3, THR-MET-003); recorded in disposition output | false |

Registry is CLOSED: any code used in any fixture, test, or gate spec must exist
here (guard test `test_registry_guard.py`). ENGINEERING JUDGMENT: RC-009/RC-010
split the freeze record's single G1 trigger class for replay/forensic clarity;
the G1 disposition (REJECT fail-closed, never reaches G2) is unchanged.
Consistency check (resolves RT-M2S4-03): RC-001, RC-003, RC-005, RC-008 as used
in the freeze record, RTM acceptance criteria, and `docs/97` are all present —
CONSISTENT; no orphaned codes.

## Label propagation and high-water mark

Merged or derived object label = most-restrictive combination of parent labels
across classification, domain, and caveat, unless RC-006 (authorized downgrade
with proof) applies. Propagation is deterministic and recorded in provenance.
Segregation is a disposition, not a transformation: no derived object exists
and no label propagates; the segregated set is recorded in provenance and
audit only (M5 Sprint 9 amendment 2026-07-06).

## No-unauthorized-merge invariant (formal)

For any fusion output O derived from inputs I1..In:
O is permitted only if there exists an explicit permit P in the active bundle
such that P covers the combined (classification, domain, caveat) tuple of
I1..In. Absent P, the merge is blocked and inputs are segregated. Violation is
either structurally unrepresentable or fails closed. No operator override,
authority, reason code, or PIP attribute can create P or bypass this check; an
override may act only inside an already-permitted envelope (B2). Verified by
property-based test (TST-PRP-040) and red-team test.

## MERGE-PERMIT schema [M5 Sprint 9 amendment 2026-07-06]

Bundle section `merge_permits[]`. Explicit enumeration only — no wildcards,
no patterns, no cardinality shortcuts at TRL 1-3.

| Field | Constraint |
|---|---|
| permit_id | unique within the bundle |
| permitted_combinations | list of parent-tuple multisets; each entry is an explicit multiset of (classification, domain, caveat) tuples |
| output_authority | fixed value HWM: the output label is always computed by ARCH-07 invoked by ARCH-08 post-permit; a permit can never assign an output label |

`covers(request)` is true iff the request's parent-tuple multiset EXACTLY
matches one enumerated entry in `permitted_combinations` (RT-M5S9-01: a
combination [T1, T2] does not cover [T1, T1] or [T2, T2]; duplicate-tuple
merges [T, T] are legal only when explicitly enumerated). There is no
max_parents field: each combination fixes its own cardinality (architect
disposition + lead concurrence 2026-07-06). RULE-POL-002 text and semantics
are unchanged; this schema defines the data it evaluates. Trace:
FCE-REQ-KRN-011, FCE-REQ-KRN-012.

## Conflict resolution

Deterministic priority: deny-overrides by default. Unresolved ties fail closed
and enqueue human review (RC-005). No nondeterministic outcome is permitted; any
such case escalates to the architect and holds at fail-closed in the interim.

## Disposition severity lattice [D3, FCE-DR-POL-001 — RATIFIED 2026-07-04]

Total order over dispositions, most → least restrictive:

reject > quarantine > block > segregate > require-human-review > restrict >
transform > route-to-higher-domain > permit.

Combination: when multiple rules fire, the final disposition = the most
restrictive among fired outcomes. `downgrade` and `override` are
authority-gated actions — never products of lattice combination (only explicit
authorized paths, RC-006 / RC-007). The order is total, so disposition-level
ties are structurally impossible; residual ambiguity (an unresolvable
condition/attribute) is not a tie — it quarantines with RC-005
(FCE-REQ-POL-012). Middle-entry ordering is ENGINEERING JUDGMENT per
FCE-DR-POL-001 (status: RATIFIED 2026-07-04).

Trace: FCE-REQ-POL-001, FCE-REQ-POL-012.

## Decision-record output contract [D4] (M4 audit-coordination hook; spec only)

Every PDP evaluation emits atomically: input object ID(s); PIP attribute set
consumed (IDs + auth status); policy-bundle version pinned at G4 entry; rule
ID(s) fired; final disposition (D3 lattice); reason code(s) from the closed
registry; enforcement action; evaluation timestamp; deterministic-evaluation
flag. This is the field set the 18-field audit schema (M4, `docs/08`) consumes.

## Example rules (Rego-style, reference pattern only — no implementation)

### RULE-POL-001 — narrow permit
```
# Rule: RULE-POL-001 — same-domain permit
# Trace: FCE-REQ-POL-011  Bundle: proj-baseline@0.1.0  Default: deny
package fce.policy.release
default allow := false
allow if {
    input.object.classification in data.permits[input.mission].classifications
    input.object.domain == input.channel.domain
    valid_caveats(input.object.release_caveat, input.channel)
    not stale(input.object.timestamp)
}
# TST-POL-001: given same-domain object with permitted classification and fresh
# timestamp, expect permit; audit event policy-decision with RULE-POL-001,
# reason code none (permit).
```

### RULE-POL-002 — default block on cross-domain merge
```
# Rule: RULE-POL-002 — block unpermitted cross-domain merge
# Trace: FCE-REQ-KRN-010  Bundle: proj-baseline@0.1.0  Default: deny
package fce.policy.merge
default allow := false
allow if {
    some p
    p := data.merge_permits[_]
    covers(p, input.inputs)   # explicit permit covering all inputs
}
# TST-POL-002: given two inputs of differing domain with no covering permit,
# expect block + segregate; audit fusion-decision with RULE-POL-002, RC-003.
```

### RULE-POL-003 — quarantine ambiguous label
```
# Rule: RULE-POL-003 — quarantine ambiguous classification
# Trace: FCE-REQ-POL-012  Bundle: proj-baseline@0.1.0  Default: deny
package fce.policy.ingest
default allow := false
quarantine if { not resolvable(input.object.classification) }
# TST-POL-003: given object with unresolvable classification, expect quarantine
# + require-human-review; audit transformation with RULE-POL-003, RC-005.
```

### RULE-POL-004 — PIP attribute authentication (B1)
```
# Rule: RULE-POL-004 — PIP attribute authentication (B1)
# Trace: FCE-REQ-SEC-002  Bundle: proj-baseline@0.1.0  Default: deny
package fce.policy.pip
default attributes_valid := false
attributes_valid if {
    every attr in input.pip_attributes { attr.authenticated; attr.integrity_bound }
}
# TST-POL-004: one spoofed/unauthenticated PIP attribute among otherwise valid
# inputs → fail-closed at G4 with RC-008; audit records the failing attribute
# ID; no decision consumes the attribute.
```

### RULE-POL-005 — envelope-bounded override (B2; RT-M3S5-01 fix applied)
```
# Rule: RULE-POL-005 — envelope-bounded override (B2)
# Trace: FCE-REQ-OPS-002, FCE-REQ-KRN-011  Bundle: proj-baseline@0.1.0  Default: deny
package fce.policy.override
default override_valid := false
override_valid if {
    input.override.authority_authenticated
    input.override.reason_code
    input.override.time_limit_valid
    input.override.audit_signature_placeholder
    input.underlying_decision.disposition in data.permitted_envelope
    not data.reason_codes[input.underlying_decision.reason_code].override_immutable
}
# TST-POL-005a: all preconditions + in-envelope decision → accepted, RC-007,
# audited. TST-POL-005b: override vs RC-003 cross-domain block → rejected,
# block stands. TST-POL-005c: any missing precondition → rejected fail-closed.
# TST-POL-005d: override vs RC-002 domain-mismatch block → rejected
# (override_immutable). TST-POL-005e: override expired per injected clock →
# rejected (H4 dependency stated in EVD-M3).
```

### RULE-POL-006 — deny-overrides conflict combination
```
# Rule: RULE-POL-006 — deny-overrides conflict combination (D3 lattice)
# Trace: FCE-REQ-POL-001, FCE-REQ-POL-012  Bundle: proj-baseline@0.1.0  Default: deny
package fce.policy.combine
final_disposition := most_restrictive([d | d := fired_rules[_].disposition])
# TST-POL-006a: {permit, restrict} → restrict. TST-POL-006b: {permit, block} →
# block. TST-POL-006c: unresolvable condition → quarantine, RC-005, review
# queue; never permit-by-default.
```

## Hot-reload (FCE-DES-02)

PAP loads signed bundles with version pinning; in-flight objects complete under
the bundle version pinned at G4 entry; invalid or unsigned bundles are rejected
fail-closed with rollback to the last good version.

## Requirement trace

FCE-REQ-POL-001, FCE-REQ-POL-011, FCE-REQ-POL-012, FCE-REQ-POL-020,
FCE-REQ-KRN-010, FCE-REQ-KRN-011, FCE-REQ-OPS-002, FCE-REQ-SEC-001,
FCE-REQ-SEC-002.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: default-deny; 11 actions; deny-overrides; invariant is fail-closed.
- Assumptions: project taxonomy is adequate to exercise all rules.
- Judgment: reason-code set and rule examples.
- Uncertainty: coalition caveat modelling depth (OPEN-01/OPEN-02).
