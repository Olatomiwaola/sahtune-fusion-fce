---
name: fce-policy-as-code
description: Produces FCE policy schemas, Rego-style declarative rule examples, label propagation rules, conflict handling, and no-unauthorized-merge invariants. Use for any policy schema, label/domain/caveat/authority schema, default-deny design, policy action modelling, Rego-style examples, or policy unit-test descriptions.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Policy-as-Code

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`. XACML PDP/PEP/PAP/PIP model and OPA/Rego syntax are reference patterns only (cite OASIS XACML spec and openpolicyagent.org docs as primary references); no compliance claims.

## Purpose
Design the declarative policy layer: schemas, rules, propagation, conflicts, invariants — deterministic, default-deny, fail-closed.

## Trigger conditions
Any work on: policy/label/domain/release-caveat/authority schemas; policy actions; conflict resolution; merge invariants; example rules; policy test descriptions.

## Procedure
1. Model within PDP (decision) / PEP (enforcement) / PAP (administration) / PIP (attributes: mission, user, sensor, classification, domain, caveat, timestamp, network state, operational context).
2. Base disposition is **deny**. Every rule adds a narrow, attributable permit or a stronger restriction.
3. Support all required actions: permit, restrict, block, segregate, quarantine, reject, transform, route-to-higher-domain, require-human-review, downgrade (only with valid authority + transformation proof), override (only with authenticated authority + reason code + time limit + audit signature).
4. Define label propagation: merged/derived objects take the most restrictive combination (high-water mark) unless an authorized downgrade transformation with proof applies.
5. State the **no-unauthorized-merge invariant** formally: no fusion output may combine inputs whose domain/classification/caveat combination lacks an explicit permit; violations are structurally unrepresentable or fail closed.
6. Conflict resolution: deterministic priority ordering (deny-overrides default); unresolved ties fail closed and enqueue human review.
7. Write example rules in Rego-style syntax (`templates/policy-rule.md`), each with a unit-test **description** (no implementation until approved) linked to a requirement ID.
8. Use a **project taxonomy** for labels — never invent real Government of Canada classified procedures or markings.

## Required reference files
Metadata schema (docs/05_data_model/), RTM, audit schema fields.

## Optional supporting scripts
None at Phase A. (Future: policy schema validator — requires approval.)

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash, WebSearch, WebFetch, MCP connectors (no network by default).

## Example usage
"Write the cross-domain merge rules" → invariant statement → domain compatibility matrix → 3 Rego-style examples (permit narrow, block default, quarantine ambiguous) → unit-test descriptions → REQ links.

## Validation checklist
- [ ] Default-deny everywhere; ties fail closed.
- [ ] All 11 policy actions representable.
- [ ] Downgrade/override preconditions complete.
- [ ] Propagation defined for merge/transform/downgrade/quarantine.
- [ ] Invariant formal + property-test description present.
- [ ] Every example rule → unit-test description → REQ ID.
- [ ] Project taxonomy disclaimer present.

## Output template
```
## Schema/Rule set: <name> v<version>
Attributes consumed (PIP): <list>
Rules: <Rego-style blocks>
Propagation notes: <...>
Conflict handling: <...>
Unit-test descriptions: TST-POL-XXX ...
Requirement trace: <REQ IDs>
Facts / Assumptions / Judgment / Uncertainty: <split>
```

## Failure conditions (stop and escalate)
- A requested rule would require inventing real classified procedure → refuse, use project taxonomy, flag.
- Nondeterministic conflict outcome unavoidable → escalate to architect; interim disposition = fail closed.
- Rule cannot emit required audit fields → coordinate with audit-forensics-engineer before proceeding.
