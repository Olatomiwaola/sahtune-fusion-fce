---
name: fce-documentation-style
description: Enforces Kanatir naming, formatting, diagrams, glossary, acronym discipline, and evidence-first writing across all FCE documents. Use when writing or reviewing any project document, checking terminology, or formatting deliverables.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Documentation Style

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`.

## Purpose
Consistent, evidence-first documentation: any reader can trace any claim, expand any acronym, and find any artifact.

## Trigger conditions
Writing/reviewing any docs/ artifact; terminology or naming questions; diagram conventions; glossary maintenance.

## Rules
1. **Naming.** Product: "Sahtune Fusion Compliance Engine (FCE)" on first use per document; "FCE" after. Always "a capability inside Sahtune Fusion" — never a product. Files: kebab-case. IDs: FCE-REQ-*, THR-*, TST-*, EVD-*, DR-* (decision records), RULE-*.
2. **Acronym discipline.** Expand on first use per document; maintain docs/00_project_context/glossary.md; no unexpanded acronym enters the glossary-less wild.
3. **Evidence-first writing.** Claims carry a trace (REQ/EVD/TST/DR ID) or one of the labels: FACT (cited), ASSUMPTION, ENGINEERING JUDGMENT, UNCERTAINTY, TARGET (internal, to be verified), MEASURED (provenance).
4. **Prohibited vocabulary** unless independently validated: certified, accredited, compliant with <standard>, endorsed, operationally deployed, approved for classified. Substitute: "designed with reference alignment to <primary source>."
5. **Diagrams.** Mermaid or described-text; every trust boundary drawn explicitly; data flows show all 7 gates in order.
6. **Tables.** Full cell text — never clipped or truncated; split tables rather than clip.
7. **Citations.** Primary sources only for standards: OASIS (XACML), openpolicyagent.org (OPA/Rego), W3C (PROV), CCCS (ITSG-33), NIST (SP 800-207, AI RMF), CanadaBuys/Canada.ca (solicitation).
8. **Decision records.** DR-<nnn>: context, options, decision, consequences, trace.

## Required reference files
docs/00_project_context/glossary.md; this skill.

## Optional supporting scripts
None.

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash, WebSearch, WebFetch, MCP connectors.

## Example usage
"Review the policy model doc" → naming/acronym pass → claim-label pass → prohibited-vocabulary scan → table completeness → citation check → issue list.

## Validation checklist
- [ ] Naming + ID schemes conform.
- [ ] Acronyms expanded; glossary updated.
- [ ] Every claim traced or labelled.
- [ ] Zero prohibited vocabulary.
- [ ] Tables complete; diagrams show boundaries/gates.
- [ ] Primary-source citations.

## Output template
```
## Style review: <doc>
Issues: <numbered, with fixes applied/proposed>
Glossary delta: <terms>
Result: <pass | pass-with-fixes | fail>
```

## Failure conditions (stop and escalate)
- Author insists on prohibited vocabulary → escalate to product-strategy-reviewer + leadership.
