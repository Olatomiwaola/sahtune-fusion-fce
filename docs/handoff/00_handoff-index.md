# 00 — Claude Desktop Handoff Index

Fusion Compliance Engine (FCE), a capability inside Sahtune Fusion. Docs-only
handoff. No implementation code, no installs, `.claude/` untouched.

## Project status
Design stage, TRL 1-3. The system architecture package (`docs/00`–`13`), the
B1–B3 closure (`97`), the live gate review (`98`), the M1–M9 execution
architecture (`14`), and the TRL 1-3 build plan (`15`) are complete as v0/draft
design artifacts. No build/implementation has started.

## What has been completed
- 14 FCE agents and 13 FCE skills installed under `.claude/` (inventory in `00`).
- 13-block architecture package (`docs/00`–`13`) with verification report (`README`).
- RTM covering 6/6 Essential and 4/4 Desired outcomes (`03`) — outcome wording
  now uses verified verbatim Canada.ca challenge text from M1 Sprint 1.
- Live red-team + security-assurance gate review (`98`); design-time self-review (`99`).
- B1–B3 blocking-in-text conditions closed in text (`97`).
- M1–M9 execution architecture (`14`) and TRL 1-3 build plan with 14 sprints (`15`).

## Current GitHub repo state
- Remote: `origin` → `https://github.com/Olatomiwaola/sahtune-fusion-fce.git`.
- Branch: `main`.
- Design docs through the TRL 1-3 build plan are committed.
- **Action:** after this handoff package is committed, confirm `origin/main` shows
  the latest handoff commit before relying on GitHub as the shared source of
  truth (see `07_next-action-checklist.md`).

## Latest known commits (most recent first)
```
c93244e Add TRL 1-3 build plan
781ca5b Add M1-M9 execution architecture
442a8e7 Close B1-B3 architecture review findings in docs
514c9e7 Add FCE architecture package
25407aa Add FCE Claude agent and skill library
```
The handoff package is the next commit after the list above.

## Where the source-of-truth docs live
- Governance/library: `.claude/agents/` (14 agents), `.claude/skills/` (13 skills).
- Architecture package: `docs/00`–`13`, plus `README`.
- Execution planning: `docs/14` (M1–M9), `docs/15` (TRL 1-3).
- Reviews: `docs/97` (B1–B3 closure), `docs/98` (live gate review), `docs/99` (self-review).
- Handoff (this folder): `docs/handoff/00`–`07`.

## How Claude Desktop should be used
Claude Code + the GitHub repo remain the single source of truth. Claude Desktop
is for sprint-by-sprint review, planning, rewriting, and discussion — one mission
block or one sprint per chat. Every Desktop output must cite repo file paths and
requirement IDs, and mark anything needing a repo change as `REPO-UPDATE`.
Approved changes are written back into repo files through Claude Code and
committed. Full rules: `02_claude-desktop-operating-instructions.md` and
`06_desktop-session-rules.md`.

## Handoff file map
| File | Purpose |
|---|---|
| `00_handoff-index.md` | This index: status, repo state, commits, how to use Desktop |
| `01_architecture-completion-summary.md` | What is designed and what is not done |
| `02_claude-desktop-operating-instructions.md` | Desktop vs Code roles and rules |
| `03_sprint-by-sprint-desktop-prompts.md` | 14 ready-to-paste sprint prompts (M1–M7) |
| `04_traceability-map.md` | Block/sprint → docs → REQ IDs → evidence → gate → repo target |
| `05_open-items-and-decision-register.md` | OPEN-01/02/03, H1–H14, L1–L5, leadership decisions |
| `06_desktop-session-rules.md` | Strict session rules |
| `07_next-action-checklist.md` | Immediate next actions |
