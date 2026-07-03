# 07 — Policy Decision Model v0 (draft)

Owner: `policy-engineer`. Skill: `fce-policy-as-code`.
XACML PDP/PEP/PAP/PIP and OPA/Rego are reference patterns only (cite OASIS
XACML; openpolicyagent.org). No compliance claims.

## Project taxonomy disclaimer [OPEN-02]

All classification, domain, and caveat values are a PROJECT TAXONOMY for
exercising the pipeline. They are not real Government of Canada markings or
procedures. A documented mapping links the project taxonomy to named handling
targets (e.g., the Protected B target in FCE-ESS-02) without reproducing real
marking procedures.

## Model

- PDP (ARCH-03): decision. PEP (ARCH-04): enforcement at each gate.
- PAP (ARCH-05): signed, versioned bundle administration and hot-reload.
- PIP (ARCH-06): attributes — mission, user, sensor, classification, domain,
  caveat, timestamp, network state, operational context.
- Base disposition is deny. Every rule adds a narrow, attributable permit or a
  stronger restriction.

## Policy actions (all 11 representable)

permit, restrict, block, segregate, quarantine, reject, transform,
route-to-higher-domain, require-human-review, downgrade (only with valid
authority and transformation proof), override (only with authenticated
authority, reason code, time limit, and audit signature placeholder).

## Reason-code registry (excerpt)

| Code | Meaning |
|---|---|
| RC-001 | Missing or malformed mandatory metadata |
| RC-002 | Classification/domain/caveat mismatch with channel |
| RC-003 | No explicit permit for cross-domain merge |
| RC-004 | Stale or unverifiable timestamp |
| RC-005 | Ambiguous condition; enqueue human review |
| RC-006 | Authorized downgrade with valid transformation proof |
| RC-007 | Authenticated override within time limit |

## Label propagation and high-water mark

Merged or derived object label = most-restrictive combination of parent labels
across classification, domain, and caveat, unless RC-006 (authorized downgrade
with proof) applies. Propagation is deterministic and recorded in provenance.

## No-unauthorized-merge invariant (formal)

For any fusion output O derived from inputs I1..In:
O is permitted only if there exists an explicit permit P in the active bundle
such that P covers the combined (classification, domain, caveat) tuple of
I1..In. Absent P, the merge is blocked and inputs are segregated. Violation is
either structurally unrepresentable or fails closed. Verified by property-based
test (TST-PRP-040) and red-team test.

## Conflict resolution

Deterministic priority: deny-overrides by default. Unresolved ties fail closed
and enqueue human review (RC-005). No nondeterministic outcome is permitted; any
such case escalates to the architect and holds at fail-closed in the interim.

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

## Hot-reload (FCE-DES-02)

PAP loads signed bundles with version pinning; in-flight objects complete under
the bundle version pinned at G4 entry; invalid or unsigned bundles are rejected
fail-closed with rollback to the last good version.

## Requirement trace

FCE-REQ-POL-001, FCE-REQ-POL-011, FCE-REQ-POL-012, FCE-REQ-POL-020,
FCE-REQ-KRN-010, FCE-REQ-OPS-002.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: default-deny; 11 actions; deny-overrides; invariant is fail-closed.
- Assumptions: project taxonomy is adequate to exercise all rules.
- Judgment: reason-code set and rule examples.
- Uncertainty: coalition caveat modelling depth (OPEN-01/OPEN-02).
