---
name: fce-test-and-evaluation
description: Produces FCE simulation, bench, edge, integration, adversarial, acceptance, and regression test templates with every test linked to a requirement. Use for V&V planning, test matrices, test case specification, coverage analysis, or acceptance criteria work.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Test & Evaluation

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`.

## Purpose
Build and maintain the V&V system: templated, requirement-linked tests across all classes, with bidirectional traceability.

## Trigger conditions
Test plan/matrix creation or update; new requirement needing verification; red-team finding formalization; regression suite design; coverage audits.

## Procedure
1. Every test uses `templates/test-case.md`: ID (TST-<class>-<nnn>), linked REQ IDs, class, preconditions, procedure, expected result (objective pass/fail), environment, data (synthetic-labelled).
2. Cover all mandatory classes: unit (per policy rule, metadata validation, label propagation), integration (ingestion→tagging→policy→fusion→audit), property-based (prohibited cross-domain merges), red-team (metadata tampering, replay, malformed packets, stale timestamps, policy bypass, privilege escalation, audit suppression, source spoofing, invalid downgrade, invalid override), performance (tactical latency), edge/degraded (compute, storage, network loss, power, CPU load, thermal), regression (policy updates), explainability (operator trust).
3. Maintain the bidirectional matrix; report coverage as n/total with named gaps.
4. Fail-closed cases mandatory for every gate: missing, malformed, expired, ambiguous, unverifiable inputs.
5. Test descriptions only until implementation approval.

## Required reference files
RTM, policy rule set + unit-test descriptions, benchmark protocols, scenario specs.

## Optional supporting scripts
None at Phase A. (Future: coverage checker — requires approval.)

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash (until implementation approved), WebSearch, WebFetch, MCP connectors.

## Example usage
"Cover FCE-REQ-POL-012" → class selection (unit + property) → TST-POL-031, TST-PRP-004 specs → matrix update → coverage delta.

## Validation checklist
- [ ] Bidirectional trace complete; gaps named.
- [ ] All 8 test classes represented in the plan.
- [ ] All 10 red-team categories present.
- [ ] Fail-closed cases per gate present.
- [ ] Objective pass/fail only; no clipped cells; synthetic data labelled.

## Output template
```
## Test spec(s): <IDs>
[per test: template fields]
Matrix delta: <REQ↔TST additions>
Coverage: <n/m>, gaps: <list>
Facts / Assumptions / Judgment / Uncertainty: <split>
```

## Failure conditions (stop and escalate)
- Requirement untestable as written → return to requirements-traceability-engineer.
- Test requires live/real data → stop; synthetic-first principle; escalate.
- Expected result would depend on black-box AI output alone → redesign; AI outputs may be observed but never the sole pass/fail authority.
