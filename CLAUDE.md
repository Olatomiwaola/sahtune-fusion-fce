# CLAUDE.md — sahtune-fusion-fce

Sahtune Fusion Compliance Engine (FCE): TRL 1-3 laptop-scale proof of concept,
DND IDEaS W7714-248676/014. FCE is a hardened capability inside Sahtune
Fusion — not a standalone product. Reference-alignment only for all cited
standards; no certification, accreditation, or compliance claims anywhere in
this repository.

Authority pointers (this file never duplicates them):
- Sprint state: docs/handoff/08_sprint-tracker.md (single reference for
  current block/sprint/status).
- Working conventions: docs/handoff/10_working-conventions.md (rules 1-10,
  binding).
- Open items and decisions: docs/handoff/05_open-items-and-decision-register.md
  and evidence/laptop-poc/decision_register.md (append-only).
- Toolchain: .venv only — Python 3.12.13, pytest 9.1.0, stdlib-first;
  installs and network by explicit approval only (FCE-DR-POC-007).

## Claude Code execution discipline (binding — working-conventions rule 10)

1. Write/run environment only. Claude Code never runs role blocks, never
   launches review or specialist subagents, and never emits HANDOFF-format
   blocks. All role blocks, reviews, rulings, and design work happen in the
   block chat. A file supplied without an execution instruction is read and
   held — nothing more.
2. Chat drafts; Code writes — verbatim. Claude Code never authors, composes,
   completes, or paraphrases governance text, register entries, decision
   records, design content, evidence content, or commit-worthy prose. It
   executes chat-drafted text exactly as supplied. If required text is
   missing or garbled, it stops and reports what it lacks; it does not
   reconstruct from memory of prior pastes.
3. Transport by file. Multi-line content arrives as a file at an exact path.
   Terminal paste is accepted only for hashes, paths, and one-line commands.
   A transport file supersedes every pasted fragment of the same content.
4. Read-back gates every commit. For each edited or appended region: read it
   back raw from disk and emit it in the returned output BEFORE any git
   add/commit runs. A commit executed without its read-backs already emitted
   is a process violation (precedent: eafb980, M6). If any read-back deviates
   from the instruction file, stop before committing and report the deviation
   raw.
5. Raw output is the only evidence. Every claim about repo or filesystem
   state is accompanied by the raw command output that shows it. Narrated
   summaries, stat-line substitutes, and "verified, matches" assertions carry
   no evidentiary weight on their own.
6. Stop-and-report on divergence. If preconditions fail (wrong HEAD, dirty
   tree, unexpected file state), if a push is rejected, or if instruction and
   reality diverge in any way: stop, make no further changes, report raw.
   Never merge, rebase, force-push, or improvise recovery.
7. Approvals are one-time and narrow. No standing grants, no batching an
   approval across actions, no generalizing a permission from one run to the
   next, no background execution of anything not explicitly instructed in the
   current chat-drafted REPO-UPDATE.
