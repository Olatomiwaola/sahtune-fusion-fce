# RT-M3S5 — Red-Team Findings, M3 Sprint 5 (Policy Decision Model v1)

Owner: `red-team-reviewer`. Raised 2026-07-04 (chat) against the M3 Sprint 5 policy model
v1 (`docs/07_policy-decision-model.md`), the disposition severity lattice
(`docs/12_decision_records/fce-dr-pol-001.md`), and the Sprint 6 evaluator file plan.
Basis commit 7d981fd.

RT-M3S5-01 is **FIXED pre-commit** (in-text). RT-M3S5-02 and -03 are **open,
non-blocking** for the v1 model. Tracked in
`docs/handoff/05_open-items-and-decision-register.md`.

| Finding | Severity | Status | Location |
|---|---|---|---|
| RT-M3S5-01 | High | **FIXED pre-commit** (override_immutable flag; RULE-POL-005 checks it) | override.py / RULE-POL-005 |
| RT-M3S5-02 | Medium | Open, non-blocking (H4 dependency; FU-M3S5-1) | attributes.py clock |
| RT-M3S5-03 | Medium | Open, non-blocking (real authN is H3/H4; label mechanism-simulated) | G1 / fixtures |

## RT-M3S5-01 — override immutability under-scoped

**Finding.** RULE-POL-005 as first drafted hard-coded RC-003 as the only
override-immutable code; B2 also bars overriding domain-mismatch blocks (RC-002),
leaving an invalid-override path where an authenticated operator could override an
RC-002 block.

**Location.** override.py / RULE-POL-005. **Trace.** FCE-REQ-OPS-002, FCE-REQ-KRN-011.
**Hook.** TST-POL-005d.

**Disposition.** **FIXED pre-commit.** The reason-code registry gains an
`override_immutable` flag (RC-002 and RC-003 both true), and RULE-POL-005 checks the
flag (`not data.reason_codes[...].override_immutable`) rather than a hard-coded code.
Verified by TST-POL-005d (override vs RC-002 → rejected).

## RT-M3S5-02 — override time-limit depends on an unverified clock

**Finding.** Override time-limit validity depends on an unverified clock (H4); clock skew
could extend an already-expired override.

**Location.** attributes.py clock. **Trace.** FCE-REQ-OPS-002. **Hook.** injected clock
only; TST-POL-005e.

**Disposition.** **Open, non-blocking.** At TRL 1-3 the evaluator uses an injected clock;
the H4 trusted-time dependency must be stated explicitly in EVD-M3 (tracked as FU-M3S5-1).
No trusted-time claim is made.

## RT-M3S5-03 — RC-011 has no authN mechanism at TRL 1-3

**Finding.** RC-011 (source authentication failure) has no defined authentication
mechanism at TRL 1-3; fixture authentication flags are self-declared, so tests prove
plumbing, not authentication.

**Location.** G1 / fixtures. **Trace.** FCE-REQ-SEC-001, FCE-REQ-SEC-002. **Hook.** label
RC-011 cases "mechanism-simulated" in `test_g1_reason_codes.py`.

**Disposition.** **Open, non-blocking.** Real source authentication is H3/H4 scope;
EVD-M3 must **not** claim authentication is demonstrated. RC-011 test cases are labelled
"mechanism-simulated" so the evidence cannot be read as an authN proof.

## Claim audit

**CLEAN.** No overclaim in the v1 policy model or the Sprint 6 evaluator plan: the model
is reference-pattern/spec only; determinism and fail-closed behaviour are stated as
to-be-tested at Sprint 6; no trusted-time or authentication capability is claimed at
TRL 1-3 (RT-M3S5-02/-03 gate those claims).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: RT-M3S5-01 is fixed in the committed docs/07 v1 (override_immutable flag +
  RULE-POL-005 flag check) with TST-POL-005d as the regression hook.
- ENGINEERING JUDGMENT: severities; -02/-03 rated non-blocking because they gate
  *claims*, not model correctness, at TRL 1-3.
- UNCERTAINTY: -02 and -03 close only when H4 (trusted time) and H3/H4 (authN) are
  delivered; EVD-M3 must carry both caveats.
