---
name: fce-evidence-pack
description: Creates and maintains the standard FCE evidence folder structure for requirements, architecture, tests, logs, decisions, risks, demos, and TRL evidence, with evidence checklists. Use for evidence organization, evidence-gap analysis, TRL evidence packaging, or accreditation-support package assembly.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Evidence Pack

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`.

## Purpose
Keep evidence organized, indexed, and gap-audited so every claim anywhere in the project can point to an artifact that exists.

## Trigger conditions
Evidence folder work; evidence indexing; gap analysis; TRL band packaging; demo evidence capture; accreditation-support assembly (labelled "support" only).

## Procedure
1. Maintain the canonical structure: evidence/trl_1_3/, evidence/trl_4_5/, evidence/trl_6_9/, each containing: requirements/, architecture/, tests/, logs/, decisions/, risks/, demos/ with an INDEX.md per folder.
2. Every artifact entry: ID (EVD-<nnn>), title, path, type, produced-by (agent/person), date, linked REQ/TST/THR IDs, status (draft/verified).
3. Gap audit: walk exit criteria for the active TRL band; report criterion → evidence status (missing/draft/verified).
4. Checklists via `templates/evidence-checklist.md`.
5. Accreditation-support packages are always labelled "accreditation-support" — never "accredited" or "certified."

## Required reference files
TRL exit criteria (docs/09_trl_evidence/), RTM, test results, decision records.

## Optional supporting scripts
None at Phase A. (Future: index generator — requires approval.)

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash, WebSearch, WebFetch, MCP connectors.

## Example usage
"Package TRL 1–3 evidence" → walk 5 exit criteria → index existing artifacts → gap list → checklist emission.

## Validation checklist
- [ ] Canonical structure intact; INDEX.md current per folder.
- [ ] Every entry has ID, links, status.
- [ ] Gap report matches exit criteria exactly.
- [ ] No "accredited/certified" labels.
- [ ] Referenced paths exist.

## Output template
```
## Evidence action: <scope>
Index delta: <EVD IDs added/updated>
Gap report: <criterion → status>
Checklist: <ref>
Facts / Assumptions / Judgment / Uncertainty: <split>
```

## Failure conditions (stop and escalate)
- Claim found without evidence path → flag to trl-evidence-engineer + red-team-reviewer.
- Evidence artifact missing at referenced path → mark broken, escalate; never fabricate.
