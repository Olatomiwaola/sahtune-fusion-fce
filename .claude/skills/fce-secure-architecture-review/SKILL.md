---
name: fce-secure-architecture-review
description: Reviews FCE trust boundaries, attack surfaces, unsafe defaults, race conditions, nondeterminism, policy bypass routes, logging gaps, and deployment risks. Use before finalizing any architecture change, for security design reviews, or when assessing any component or external tool's architectural risk.
allowed-tools: Read, Grep, Glob, Write
---

# FCE Secure Architecture Review

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`. NIST SP 800-207 and ITSG-33 cited from primary sources — reference alignment only.

## Purpose
A structured security lens applied to every architectural artifact before it is trusted.

## Trigger conditions
Any architecture change; new component/interface; trust-boundary modification; deployment design; external tool architectural assessment; pre-finalization gates.

## Review protocol (all 8 lenses, every time)
1. **Trust boundaries** — enumerated? Zero-trust between sensors, services, users, containers, networks, domains, mission apps, operators, policy bundles, logs, update mechanisms?
2. **Attack surfaces** — every interface listed with authN/authZ story? Service-to-service requests authenticated and authorized?
3. **Unsafe defaults** — any permit-by-default, unauthenticated path, or optional metadata? (Must be deny-by-default, fail-closed.)
4. **Race conditions** — policy reload vs in-flight objects; concurrent gate evaluation; audit-write ordering.
5. **Nondeterminism** — any enforcement path whose outcome varies by timing, AI output, or unordered evaluation? (Enforcement must be deterministic.)
6. **Policy bypass routes** — any path from ingestion to fusion skipping any of the 7 gates, including debug/admin/replay/accelerated (GPU) paths?
7. **Logging gaps** — any decision without an audit event? Overflow behavior fail-safe?
8. **Deployment risks** — edge constraints, update workflow integrity, bundle signing/verification points, degraded-mode posture.

## Required reference files
Architecture spec, ICDs, threat model, deployment view.

## Optional supporting scripts
None.

## Allowed tools
Read, Grep, Glob, Write (review reports only).

## Disallowed tools
Edit, Bash, WebSearch, WebFetch, MCP connectors.

## Example usage
"Review the Degraded-Mode Manager design" → 8-lens pass → findings (e.g., lens 6: replay path skips gate 4) → severity + REQ trace → verdict.

## Validation checklist
- [ ] All 8 lenses applied and reported (including explicit "no finding").
- [ ] Every finding: severity, component, REQ IDs, suggested owner.
- [ ] Verdict: approve / approve-with-conditions / block.
- [ ] Reference-alignment phrasing only.

## Output template
```
## Secure architecture review: <artifact> v<n>
| Lens | Finding | Severity | Component | REQ IDs | Owner |
Verdict: <approve | conditions | block>
Facts / Assumptions / Judgment / Uncertainty: <split>
```

## Failure conditions (stop and escalate)
- Bypass route found → automatic block verdict + red-team-reviewer notification.
- Reviewer pressured to soften a block → escalate to leadership; the verdict stands until re-reviewed.
