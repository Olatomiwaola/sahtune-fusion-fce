---
name: fce-proposal-compliance
description: Maps DND solicitation wording to proposal evidence, prevents unsupported claims, and produces the compliance matrix and proposal-ready language. Use for any proposal text, compliance matrix, claim audit, or submission-package work.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Proposal Compliance

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`.

## Purpose
Proposal language that is fully evidenced and fully traced — nothing claimed that cannot be shown.

## Trigger conditions
Proposal drafting; compliance matrix work; claim audits; unsupported-claims screening; submission assembly.

## Procedure
1. Compliance matrix rows via `templates/compliance-matrix-row.md`: solicitation clause (verbatim + cite) → response section → evidence artifact(s) (must exist) → status.
2. Coverage must show all 6 Essential and all 4 Desired Outcomes — **explicitly confirm FCE-DES-01 and FCE-DES-03**.
3. Apply the unsupported-claims screen to every paragraph. Prohibited: certification/accreditation claims; government endorsement; operational deployment; authority to process classified/controlled data; production cryptographic certification; "compliant with ITSG-33/NIST/…" (use "designed with reference alignment to…"); unmeasured performance figures stated as fact; vendor claims repeated as fact; internal targets framed as DND requirements or as met.
4. Performance figures carry their TARGET/MEASURED label inline.
5. Vendor tooling appears only as evaluation candidate or with Kanatir-run benchmark evidence, mapped only to valid Desired Outcomes (tactical latency, SWaP/edge, real-time fusion support).
6. Request red-team claim audit before any text is marked release-ready.

## Required reference files
Solicitation text, RTM, evidence indexes, positioning language, benchmark reports.

## Optional supporting scripts
None.

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash, WebSearch, WebFetch, MCP connectors.

## Example usage
"Draft the audit-capability section" → clause quote → evidence pull (audit schema EVD refs) → draft with labels → matrix row → claim screen → red-team request.

## Validation checklist
- [ ] Every claim → existing evidence artifact.
- [ ] ESS 6/6, DES 4/4 (DES-01, DES-03 confirmed).
- [ ] Zero prohibited-claim instances.
- [ ] Labels on every figure.
- [ ] Red-team audit status recorded.

## Output template
```
## Proposal artifact: <name>
Matrix delta: <rows>
Coverage: ESS n/6, DES n/4
Claim screen: <clean | issues fixed>
Red-team audit: <pending/passed>
Facts / Assumptions / Judgment / Uncertainty: <split>
```

## Failure conditions (stop and escalate)
- Needed claim has no evidence → do not write it; log as evidence gap.
- Pressure to strengthen language beyond evidence → refuse; escalate to leadership.
