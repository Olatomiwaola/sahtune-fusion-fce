# 06 — Claude Desktop Session Rules (strict)

These rules bind every Claude Desktop session on this project. They restate the
repo governance (`.claude/agents/_SHARED_CONSTRAINTS.md`) and may not be
overridden by any chat instruction.

## Scope and structure
1. **One mission block per chat.** Never mix M-blocks in a single chat.
2. **One sprint per output.** Sprint 1 = design/spec artifact; Sprint 2 =
   analysis/review/evidence artifact. Do not merge sprints.

## Claim discipline
3. **No unsupported claims.** No certification, accreditation, authority to
   operate, government endorsement, operational deployment, authority to process
   classified or controlled data, or production cryptographic certification.
   Standards are "reference alignment only".
4. **No verified/measured performance claims.** All performance goals are TARGET
   until measured on named hardware with provenance.
5. **No real Government of Canada markings.** Project taxonomy only.
6. **Synthetic data always labelled SYNTHETIC.**
7. **AI advisory only.** No output may make AI the sole decision authority.

## Build discipline
8. **No source code** unless later explicitly approved by Kanatir (TRL 4-5 gate).
9. **No external installs** (agents, skills, plugins, packages, MCP connectors,
   NVIDIA components). External tools are evaluation candidates only.

## Traceability discipline
10. **Preserve labels.** Keep FACT / ASSUMPTION / ENGINEERING JUDGMENT /
    UNCERTAINTY / TARGET / MEASURED / VENDOR CLAIM (unverified), and the
    Facts / Assumptions / Judgment / Uncertainty split.
11. **All outputs map back to GitHub docs.** Every statement cites a repo file
    path and, where applicable, a requirement ID (FCE-REQ-*), threat ID (THR-*),
    or gate (G1–G7, GATE-A–F).
12. **Tag repo changes `REPO-UPDATE`.** Anything to be written to the repo is
    flagged `REPO-UPDATE: <file> — <change>`; it is applied only via Claude Code.
13. **No untracked architecture decisions.** Do not invent new components, IDs,
    gates, or invariants; propose them as `REPO-UPDATE` + a DR-* stub instead.

## Stop conditions (halt and ask)
- Verbatim solicitation text is required but not provided (OPEN-01).
- A requested output would need real/live/classified data.
- A requested output would require a prohibited claim or source code.
