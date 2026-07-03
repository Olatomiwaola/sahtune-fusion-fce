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

## C. Continue the sprint loop
- [ ] Continue with **M1 Sprint 2** using the M1 Sprint 2 prompt in
      `docs/handoff/03_sprint-by-sprint-desktop-prompts.md`.
- [ ] Keep one mission block per chat and one sprint per output.
- [ ] Use the verified verbatim outcome text now registered in `docs/02` and
      `docs/03`; Sprint 2 must audit coverage before declaring GATE-A.

## D. After each Desktop sprint
- [ ] Produce a **repo update note**: a list of `REPO-UPDATE: <file> — <change>`
      items plus any DR-* stubs for new decisions.
- [ ] Capture the sprint's evidence artifact reference (EVD-*).
- [ ] Check the sprint's review gate status in
      `docs/handoff/04_traceability-map.md`.

## E. Return to Claude Code
- [ ] Apply the `REPO-UPDATE` items to the target repo files.
- [ ] Read each changed file back from disk to verify clean content.
- [ ] For M2-M7 Sprint 2 PoC work, run the local tests or scripts in Claude Code
      and capture actual output as evidence when available.
- [ ] Commit with a message naming the block and sprint (e.g.,
      "M1 S2: finalize RTM coverage report").
- [ ] Push to `origin` and update `docs/handoff/04_traceability-map.md` evidence cells.

## Guardrails (unchanged)
PoC code is allowed in TRL 1-3 after M1/GATE-A when the sprint calls for it.
Production/operational code, real/live/classified/controlled data, real GoC
markings, external installs, NVIDIA components, certification/ATO/endorsement/
classified-processing claims, and measured-performance claims remain prohibited.
Project taxonomy only; synthetic data labelled `SYNTHETIC`.
