---
name: fce-threat-model
description: Produces STRIDE-style and mission-specific threat models for the FCE covering sensor, metadata, policy, audit, operator, network, edge hardware, and update workflows, with mitigations and residual risks. Use for any threat modelling, attack-surface, mitigation-mapping, or risk-register work.
allowed-tools: Read, Grep, Glob, Write
---

# FCE Threat Model

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`. ITSG-33 (CCCS) and NIST SP 800-207 cited from primary sources, reference alignment only.

## Purpose
Systematic threat identification and mitigation mapping across the full FCE attack surface, maintaining an explicit residual-risk register.

## Trigger conditions
New/changed components or trust boundaries; risk-register updates; mitigation reviews; security assessment of external tooling; red-team finding integration.

## Procedure
1. Enumerate assets per coverage area (all 8 mandatory): **sensor, metadata, policy engine, audit chain, operator, network, edge hardware, update workflows.**
2. Apply STRIDE per asset (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege), then add mission-specific threats (e.g., mid-mission policy manipulation, coalition-domain misrouting, degraded-mode exploitation, clock manipulation).
3. For each threat: ID (THR-<area>-<nnn>), actor, vector, precondition, impact, affected REQ IDs, mitigations, detection method, residual risk (accepted/tracked/blocking).
4. Map mitigations to ITSG-33 control families and SP 800-207 tenets — reference alignment only, primary citations.
5. Rank via the project register dimensions: severity, likelihood, detectability, mitigation maturity. Render full text — no clipped cells.
6. Baseline register rows must include at minimum: metadata spoofing, missing metadata, policy conflict, latency, overblocking, underblocking, audit tampering, operator misuse, dataset weakness, AI hallucination, edge failure, clock drift, policy hot-reload failure, domain misrouting, log overflow, dependency compromise.

## Required reference files
Architecture spec, trust-boundary docs, existing register (docs/11_risk_register/), red-team findings.

## Optional supporting scripts
None.

## Allowed tools
Read, Grep, Glob, Write (reports/registers only).

## Disallowed tools
Edit, Bash, WebSearch, WebFetch, MCP connectors.

## Example usage
"Threat-model the policy hot-reload path" → assets (bundle, signer, loader, cache) → STRIDE pass → THR-POL-0xx rows → mitigations (signed bundles, version checks, rollback) → residual risks.

## Validation checklist
- [ ] All 8 coverage areas addressed.
- [ ] Every threat row complete (actor→residual risk).
- [ ] All 16 baseline register risks present.
- [ ] Primary-source citations; reference-alignment phrasing.
- [ ] Fail-closed verified per failure mode.
- [ ] No clipped table text.

## Output template
```
## Threat model: <scope> v<n>
| THR ID | Area | Threat (STRIDE/mission) | Actor | Vector | Impact | Mitigations | Detection | Residual | Sev | Lik | Det | Mit maturity |
Residual-risk summary: <...>
Reference alignment: <ITSG-33 families / SP 800-207 tenets, cites>
Facts / Assumptions / Judgment / Uncertainty: <split>
```

## Failure conditions (stop and escalate)
- Mitigation would require claiming certification → rephrase as design control; flag.
- Threat implies missing requirement → route to requirements-traceability-engineer.
- Blocking residual risk on a trust boundary → escalate to architect + leadership.
