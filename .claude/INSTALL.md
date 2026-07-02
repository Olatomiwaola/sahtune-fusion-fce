# FCE Claude Code Library — Installation & Reload Guide

Controlled internal Kanatir project library: 14 subagents + 13 skills.
**No external agents, skills, plugins, or MCP connectors are included or required.**

## Install
Copy this `.claude/` directory into the root of the `sahtune-fusion-fce` repository (project scope), so paths read:
- `sahtune-fusion-fce/.claude/agents/*.md` (14 agents + _SHARED_CONSTRAINTS.md reference file)
- `sahtune-fusion-fce/.claude/skills/<skill-name>/SKILL.md` (13 skills, some with templates/)

Commit to version control so the whole team shares identical definitions.

## Reload behavior — VERIFY BEFORE INSTALL
Per Claude Code documentation as read on 2026-07-02 (re-verify against
https://code.claude.com/docs/en/sub-agents and https://code.claude.com/docs/en/skills before relying on this):
- Subagents are loaded at **session start**. Files added or edited directly on disk require a **session restart** to load. Agents created/edited via the `/agents` interface take effect immediately.
- Skills: the **directory name** is the invocation name (e.g., `/fce-threat-model`); the frontmatter `name` is a display label. Skill auto-invocation is driven by the `description` field.
- Verify with `/agents` (Library tab) that all 14 agents appear, and confirm each `/fce-*` skill is listed.

## Field/permission caveats — VERIFY BEFORE INSTALL (do not treat as permanent facts)
- Frontmatter fields used: agents — `name`, `description`, `tools`, `model`, `skills`; skills — `name`, `description`, `allowed-tools`. Confirm all are still supported and enforced in your installed Claude Code version.
- The `skills:` preload field on agents and `allowed-tools` enforcement semantics have changed between versions; test one agent and one skill before trusting tool restrictions for control.
- **Tool lists do not enforce path scoping.** Postures like "docs only" or "reports only" are enforced by convention, the agents' own instructions, review checklists, and human review — until/unless tool-level path permissions are verified in your version (check `permissions` settings in settings.json).
- If a field is unsupported in your version, the file still works as a system prompt; the affected restriction must then be enforced by review.

## How the library works together
`fce-lead-systems-architect` orchestrates. Requirements flow from `requirements-traceability-engineer` (RTM anchors everything). Design work fans out to policy/data-model/audit/fusion/edge/devsecops engineers, each preloading its matching skill. `security-assurance-engineer` (read-only + reports) and `red-team-reviewer` (read-only) gate every trust-boundary change and every external-facing claim. `test-evaluation-engineer` and `trl-evidence-engineer` close the loop from requirement to evidence. `proposal-compliance-writer` and `product-strategy-reviewer` control all outward language. The NVIDIA track runs only through `fce-vision-acceleration-evaluation` and its decision records. Every agent handoff ends in a structured block the main session can consume, and every agent is bound by `_SHARED_CONSTRAINTS.md`.

## Not yet generated (by design — awaiting later approvals)
Implementation code, FCE source code, synthetic datasets, benchmark harnesses, repository scaffold beyond `.claude/`.
