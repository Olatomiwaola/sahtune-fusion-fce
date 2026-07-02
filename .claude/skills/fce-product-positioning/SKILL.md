---
name: fce-product-positioning
description: Keeps the FCE positioned inside Sahtune Fusion, prevents product dilution and public overclaiming, and produces website-safe and proposal-safe language. Use for any positioning, naming, public description, website text, or product-line coherence question.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Product Positioning

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`.

## Purpose
One product line, honestly described: FCE is a named hardened capability inside Sahtune Fusion.

## Approved positioning baseline (verbatim)
"Fusion is the multi-sensor operating-picture layer inside Sahtune. For defence and government workflows, Fusion includes a Fusion Compliance Engine capability that enforces machine-readable classification, release, provenance, and audit policies before sensor data reaches downstream analytics."

## Trigger conditions
Positioning/naming decisions; website or public text; proposal positioning sections; product-line coherence checks.

## Rules
1. FCE = capability inside Sahtune Fusion. Never "product," "platform," "solution" as a standalone. The Sahtune line remains five products: Sentinel, Perception, Fusion, Ground Control, SwarmLink.
2. **Public-claim constraint (hard):** never imply certified classified processing, government endorsement, operational deployment, authority to process controlled/classified data, or compliance certification — unless validated through the solicitation, security authority, and applicable Canadian controls.
3. Two output registers, always labelled: **website-safe** (capability description, no performance figures, no standards names implying compliance) and **proposal-safe** (evidence-linked, labelled figures, reference-alignment phrasing).
4. Features described must exist in the approved architecture — no roadmap items as present tense.
5. Vendor tooling never appears as a differentiator unless Kanatir-verified by benchmark; then only with provenance.

## Required reference files
Approved architecture, positioning baseline (above), fce-documentation-style prohibited vocabulary.

## Optional supporting scripts
None.

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash, WebSearch, WebFetch, MCP connectors.

## Example usage
"Write the website blurb for FCE" → baseline-derived paragraph → register label: website-safe → prohibited-implication scan → present-tense audit → handoff.

## Validation checklist
- [ ] Capability framing; five-product line intact.
- [ ] All 5 prohibited implication classes absent.
- [ ] Register labelled; register rules met.
- [ ] Present tense = existing architecture only.
- [ ] Vendor mentions rule respected.

## Output template
```
## Positioning output — register: <website-safe | proposal-safe | internal>
Text: <...>
Baseline conformance: <yes/deviation+reason>
Prohibited-implication scan: <clean/issues fixed>
```

## Failure conditions (stop and escalate)
- Request to position FCE as a sixth product or to imply any prohibited claim → refuse; escalate to leadership with reasoning.
