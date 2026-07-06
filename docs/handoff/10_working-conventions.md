# 10 — Project Working Conventions

Project working conventions (learned M2–M3).

1. Commit messages: single `git commit -m "<one logical line>"` only. No
   heredocs, no message files, no Co-Authored-By trailers — the terminal-paste
   pipeline corrupts multi-line text. Detail lives in the repo (tracker cell,
   register, DR, RT files), not the message.
2. Sprint-close hash recording: tracker cells citing "this sprint's commit"
   land as a trailing pointer commit, never via --amend (a commit cannot
   contain its own hash; amending dangles the cited commit).
3. EVD-* files are append-only after commit. Corrections and rescheduling
   notes go in as dated annotations; never rewrite committed evidence in place.
4. Verification is raw output only. Paste command output verbatim into chat;
   narrated summaries and hardcoded conclusion strings (e.g., `echo "[clean]"`)
   are not evidence. Read-back-from-disk before any commit that records state.
5. File content moves by upload, not terminal paste. Any file whose content
   chat must consume verbatim (fixtures, source docs) is uploaded to the chat
   directly; terminal paste is corruption-prone beyond short commands.
6. Approval hygiene in Claude Code: one-time approvals only; never grant
   standing "don't ask again" for git commit/add or directory access. Commit
   messages are reviewed character-for-character in chat before approval.
7. **Verification artifacts move by file upload** — test reports, evidence
   files, and multi-line verification output are transferred to chat by
   file upload; terminal paste is reserved for hashes, git one-liners, and
   short raw-output confirmations. (Extends rule 5 to verification
   artifacts. Ratified 2026-07-06, M5 open: architect recommendation +
   lead concurrence recorded in-chat.)
8. **Harness cannot-analyze / obfuscation warnings default to No** — if
   Claude Code reports it cannot fully analyze a test harness or flags
   obfuscation, the default answer is No: restructure until the harness
   verifies clean. A verification instrument whose readings cannot be
   trusted is itself a fail-closed trigger. (Ratified 2026-07-06, M5 open:
   architect recommendation + lead concurrence recorded in-chat.)

DR ratification = role-block review in chat + explicit project-lead
concurrence, both recorded in the DR or decision record update.
