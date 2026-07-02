---
name: fce-audit-record-design
description: Designs signed, exportable FCE audit schemas — lineage, chain-of-custody, transformation records, and forensics exports. Use for audit record schema, hash-chain design, audit export packages, replay-from-audit, or chain-of-custody work.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Audit Record Design

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`.

## Purpose
Audit records that make every FCE decision reconstructible, tamper-evident, and exportable — with signature elements as design placeholders until independently implemented and assessed.

## Trigger conditions
Audit schema work; event-class coverage; export design; replay design; chain-of-custody; forensics workflow.

## Procedure
1. Schema per `templates/audit-record.md` — all 18 fields mandatory (N/A must be explicit): audit event ID, event type, timestamp, actor/service identity, source object ID, output object ID, policy bundle version, policy rule IDs applied, decision, reason code, enforcement action, disposition, confidence (if applicable), cryptographic hash, previous audit hash, digital signature placeholder, export status, review status.
2. Cover all 9 event classes: ingestion, transformation, policy decision, fusion decision, routing, quarantine, downgrade, export, override.
3. Chain: each record's hash includes the previous record's hash (append-only, tamper-evident). W3C PROV cited (primary) for lineage concepts — reference alignment only.
4. Replay requirement: the decision sequence must be deterministically reconstructible from audit alone.
5. Exports: JSON/CSV/PDF with integrity manifest; forensic and accreditation-support review formats (labelled "support").
6. Overflow behavior: backpressure, rotation, fail-safe — audit loss is a fail-closed trigger, designed with the architect.
7. **Never** claim production-grade cryptographic certification; signature fields say "placeholder — pending independent implementation and assessment."

## Required reference files
Metadata schema, policy decision fields, threat model (audit-tampering rows).

## Optional supporting scripts
None at Phase A.

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash, WebSearch, WebFetch, MCP connectors.

## Example usage
"Design the override audit record" → event class = override → 18-field instantiation (authority, reason code, time limit, signature placeholder) → chain position → replay note → REQ trace.

## Validation checklist
- [ ] 18/18 fields; 9/9 event classes.
- [ ] Chain + append-only semantics explicit.
- [ ] Replay determinism stated.
- [ ] Export formats + manifest defined.
- [ ] Placeholder language on signatures; no crypto-cert claims.
- [ ] Overflow fail-safe present.

## Output template
Use `templates/audit-record.md` plus:
```
Event classes covered: <n/9>
Chain notes: <...>
Requirement trace: <REQ IDs>
Facts / Assumptions / Judgment / Uncertainty: <split>
```

## Failure conditions (stop and escalate)
- A decision path produces no audit event → blocking finding to architect.
- Schema cannot capture a policy action's required fields → joint session with policy-engineer.
