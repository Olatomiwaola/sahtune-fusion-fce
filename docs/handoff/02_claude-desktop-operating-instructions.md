# 02 — Claude Desktop Operating Instructions

How to run the FCE project sprint-by-sprint in Claude Desktop without losing
repo traceability.

## Roles
- **Claude Code + GitHub repo = source of truth.** All architecture, schemas,
  policy, audit, tests, and evidence live in the repo. Only Claude Code writes
  repo files and commits.
- **Claude Desktop = review, planning, rewriting, and discussion.** Desktop
  proposes and drafts; it does not own the repo and does not commit.

## Working rules
1. **Claude Code remains the source of truth.** If Desktop and repo disagree, the
   repo wins until a change is written back through Claude Code.
2. **One mission block per chat.** Do not mix M-blocks in a single Desktop chat.
3. **One sprint per output.** Sprint 1 = design/spec artifact; Sprint 2 =
   analysis/review/evidence artifact. Keep them separate.
4. **Cite everything.** Every Desktop output must reference repo file paths
   (e.g., `docs/07_policy-decision-model.md`) and requirement IDs (e.g.,
   `FCE-REQ-POL-012`). No claim without a trace.
5. **Mark repo changes as `REPO-UPDATE`.** Anything that should change a repo file
   is tagged `REPO-UPDATE: <file> — <change>` so Claude Code can apply it.
6. **Write-back through Claude Code.** Desktop-approved changes are applied to repo
   files and committed only in Claude Code, then re-read to verify on disk.
7. **No untracked architecture decisions.** Desktop must not invent new
   components, IDs, gates, or invariants that are not in the repo. Proposed new
   decisions are logged as `REPO-UPDATE` plus a decision-record stub (DR-*), not
   silently assumed.

## Preserve epistemic discipline
Every Desktop output keeps the labels used across the repo: FACT (cited),
ASSUMPTION, ENGINEERING JUDGMENT, UNCERTAINTY, TARGET, MEASURED, VENDOR CLAIM
(unverified). Keep the Facts / Assumptions / Judgment / Uncertainty split.

## Hard prohibitions (same as repo governance)
No source code (unless later explicitly approved), no external installs, no
certification / accreditation / ATO / endorsement / classified-processing claims,
no verified/measured performance claims (all TARGET), no real GoC markings
(project taxonomy only), no unlabelled synthetic data, no AI-as-sole-authority.

## Round-trip in one line
Desktop drafts and reviews a single sprint → tags `REPO-UPDATE` items → Claude
Code writes them to repo files, reads back, and commits → GitHub stays the source
of truth.
