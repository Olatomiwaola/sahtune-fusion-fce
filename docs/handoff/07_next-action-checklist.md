# 07 — Next-Action Checklist

Immediate steps to move from Claude Code into the Claude Desktop sprint loop.

## A. Confirm repo state (Claude Code)
- [ ] Confirm this handoff package (`docs/handoff/*`) and the `README` update are
      committed.
- [ ] Confirm `main` is pushed to `origin`
      (`https://github.com/Olatomiwaola/sahtune-fusion-fce.git`).
- [ ] Verify GitHub shows the latest commit and the full `docs/` tree.

## B. Prepare Claude Desktop inputs
- [ ] Upload or select the source-of-truth docs for Desktop:
      `docs/00`–`15`, `docs/97`, `docs/98`, `docs/99`, and `docs/handoff/00`–`07`.
- [ ] Load the session rules (`docs/handoff/06_desktop-session-rules.md`) at the
      start of each Desktop chat.

## C. Start the sprint loop
- [ ] Begin with **M1 Sprint 1** using the prompt in
      `docs/handoff/03_sprint-by-sprint-desktop-prompts.md`.
- [ ] Keep one mission block per chat and one sprint per output.
- [ ] If M1 needs the verbatim solicitation text (OPEN-01), obtain it before
      finalizing the RTM (GATE-A).

## D. After each Desktop sprint
- [ ] Produce a **repo update note**: a list of `REPO-UPDATE: <file> — <change>`
      items plus any DR-* stubs for new decisions.
- [ ] Capture the sprint's evidence artifact reference (EVD-*).
- [ ] Check the sprint's review gate status in
      `docs/handoff/04_traceability-map.md`.

## E. Return to Claude Code
- [ ] Apply the `REPO-UPDATE` items to the target repo files.
- [ ] Read each changed file back from disk to verify clean content.
- [ ] Commit with a message naming the block and sprint (e.g.,
      "M1 S2: finalize RTM coverage report").
- [ ] Push to `origin` and update `docs/handoff/04_traceability-map.md` evidence cells.

## Guardrails (unchanged)
Docs-only until TRL 4-5 is approved; no source code; no installs; no
certification/ATO/endorsement/classified-processing/measured-performance claims;
project taxonomy only; synthetic data labelled SYNTHETIC.
