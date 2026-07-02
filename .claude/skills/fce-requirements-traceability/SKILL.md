---
name: fce-requirements-traceability
description: Converts DND IDEaS solicitation wording into shall/should requirements with IDs, verification methods, RTM rows, and acceptance criteria. Use whenever DND outcomes, solicitation text, requirements, traceability, RTM, acceptance criteria, or verification methods are mentioned — even implicitly (e.g., "does the design cover the challenge outcomes?").
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Requirements Traceability

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`.

## Purpose
Turn exact DND solicitation language into measurable, verifiable requirements and maintain end-to-end traceability: outcome → capability → requirement → design element → test → evidence.

## Trigger conditions
- DND wording must become requirements.
- RTM creation, update, coverage audit, or gap analysis.
- Any artifact needs requirement-trace review.
- Acceptance criteria or verification-method assignment.

## Procedure
1. Quote the solicitation outcome verbatim with source citation (CanadaBuys/Canada.ca reference). Never silently paraphrase.
2. Confirm the outcome registry is complete: **6 Essential Outcomes (FCE-ESS-01…06) and 4 Desired Outcomes (FCE-DES-01…04). FCE-DES-01 and FCE-DES-03 must be explicitly present — their omission is a known failure mode.**
3. Derive requirements: ID `FCE-REQ-<AREA>-<NNN>` (AREA ∈ ING, MET, POL, KRN, PRV, AUD, EXP, SIM, TST, EDG, SEC, OPS). One requirement = one testable statement. "Shall" = binding; "should" = desired.
4. Assign ≥1 verification method per requirement from: inspection, analysis, simulation, unit test, integration test, property-based test, red-team test, benchmark, bench test, field test, flight test, accreditation-support review.
5. Write acceptance criteria as objective pass/fail conditions.
6. Emit RTM rows using `templates/rtm-row.md`. Render full cell text — never clip or truncate.

## Required reference files
- Solicitation text (docs/00_project_context/solicitation/ — request from main session if absent; do not fetch).
- Current RTM (docs/01_requirements/rtm.md).

## Optional supporting scripts
None at Phase A. (Future: RTM coverage checker — requires approval.)

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash, WebSearch, WebFetch, MCP connectors.

## Example usage
"Convert Essential Outcome 2 into requirements" → quote EO-2 verbatim → derive FCE-REQ-POL-010..014 → assign verification methods → RTM rows → coverage report.

## Validation checklist
- [ ] ESS 6/6 and DES 4/4 covered (FCE-DES-01, FCE-DES-03 confirmed).
- [ ] Every requirement singular, testable, correctly shall/should.
- [ ] Every requirement has ID, verification method, acceptance criterion.
- [ ] Solicitation text quoted with citation.
- [ ] No clipped table text.
- [ ] No compliance/certification claims inside requirements.

## Output template
```
## Outcome <ID>: "<verbatim solicitation text>" [source]
| Req ID | Statement (shall/should) | Verification | Acceptance criterion | Traces to |
|---|---|---|---|---|
Coverage: ESS n/6, DES n/4. Gaps: <list/none>.
Facts / Assumptions / Judgment / Uncertainty: <split>.
```

## Failure conditions (stop and escalate)
- Solicitation text unavailable or version uncertain → request it; do not proceed from memory.
- An outcome cannot be made measurable → flag to leadership, do not invent metrics.
- Requirement conflicts with fail-closed or AI-advisory-only principles → escalate to architect.
