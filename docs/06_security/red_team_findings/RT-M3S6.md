# RT-M3S6 — Red-Team Findings, M3 Sprint 6 (Policy Evaluator PoC)

Owner: `red-team-reviewer`. Raised 2026-07-06 (chat) against the Sprint 6 policy
evaluator (`src/fce_poc/policy/`), fixtures (`data/fixtures/policy/`), and EVD-M3
(`evidence/laptop-poc/policy_eval_report.md`). Basis commit f48229e.

Findings 01–03 are the chat-side red-team block's review of the M3 evidence and test
coverage; 04–06 are code-level findings adopted by the reviewer. All are **NON-BLOCKING**
for the M3 code-correctness evidence. Tracked in
`docs/handoff/05_open-items-and-decision-register.md`.

| Finding | Severity | Status | Disposition |
|---|---|---|---|
| RT-M3S6-01 | Low | Fixed | EVD-M3 full-suite claim — **FIXED pre-commit (tail in f48229e)** |
| RT-M3S6-02 | Medium | Open | Determinism hash-compare limited to permit+reject → **M7** |
| RT-M3S6-03 | Low | Open | Lattice combination tested pairwise only → **M7** |
| RT-M3S6-04 | Low | Disclosed | Placeholder bundle signature, not verified crypto — H6 (TRL 4-5); no action at TRL 1-3 |
| RT-M3S6-05 | Medium | Open | Staleness / anti-replay not enforced (RC-004 unexercised) → **M7** (substantive fix H4) |
| RT-M3S6-06 | Low | Open | No-unauthorized-merge is label-coverage only, not parentage → **M5** (H1) |

## RT-M3S6-01 — EVD-M3 full-suite claim

**Finding.** EVD-M3 asserts a 68-test full-suite pass, but the verbatim pytest block in
the report is the 24-test policy suite; the full-suite count must be backed in the report,
not just stated.

**Evidence.** EVD-M3 result summary and closing line.

**Disposition.** **FIXED pre-commit (tail in f48229e).** EVD-M3 carries the full-suite
`68 passed` count line (report lines 46 and 131); the claim is backed in the committed
report. No further action.

## RT-M3S6-02 — determinism hash-compare limited to permit+reject

**Finding.** `test_determinism` hash-compares an identical-input re-evaluation for the
permit and the reject paths only. Determinism (FCE-REQ-POL-001) is therefore demonstrated
for two disposition classes, not for block / quarantine / segregate combinations.

**Evidence.** `tests/policy/test_determinism.py` (two cases: permit, G1 reject).

**Disposition.** Open, non-blocking. Deferred to **M7**: broaden the determinism
hash-compare across all disposition classes (property-based, identical-input re-eval).

## RT-M3S6-03 — lattice combination tested pairwise only

**Finding.** RULE-POL-006 lattice combination is exercised with 2-element sets
(`{permit, restrict}`, `{permit, block}`). Three-plus-element combinations and a full
total-order check are not tested.

**Evidence.** `tests/policy/test_deny_overrides.py` (TST-POL-006a/b pairwise).

**Disposition.** Open, non-blocking. Deferred to **M7**: exhaustive / property-based
lattice-combination test over the full D3 order.

## RT-M3S6-04 — bundle signature is a placeholder (not verified crypto)

**Finding.** `bundle.signature_ok` accepts `signature_placeholder == "valid"` — a string
flag, not a verified signature.

**Evidence.** `src/fce_poc/policy/bundle.py`; EVD-M3 ("no crypto claim"); docs/07
Hot-reload; shared constraint 1.

**Disposition.** DISCLOSED by design; no action at TRL 1-3. Real bundle signing /
root-of-trust / key management is **H6** (TRL 4-5). Low.

## RT-M3S6-05 — staleness / anti-replay not enforced

**Finding.** `evaluator._stale` returns fresh whenever a request omits
`object_timestamp_tick` / `freshness_window`, and RC-004 has no emitting path and no test
exercises it (the registry guard checks codes-used ⊆ registry, not registry ⊆ exercised).
Stale / replayed objects are not rejected on freshness grounds.

**Evidence.** `src/fce_poc/policy/evaluator.py` (`_stale`); RC-004 present but unemitted;
`tests/policy/test_registry_guard.py` (subset, not exhaustive-exercise).

**Trace.** none dedicated — missing-requirement flag: RTM v0.3 has no
timestamp-freshness/anti-replay row; flagged to requirements-traceability-engineer for a
candidate FCE-REQ row when H4 (trusted time) is scheduled. Nearest hosting rule:
RULE-POL-001, whose own trace (FCE-REQ-POL-011) does not cover freshness.
**Disposition.** Open, non-blocking. Deferred to **M7**: a test
for RC-004 emission under injected-clock staleness; substantive stale/replay defence needs
trusted/attested time (**H4**). Medium.

## RT-M3S6-06 — no-unauthorized-merge is label-coverage only

**Finding.** `bundle.covers_merge` authorizes a merge on classification/domain/caveat
label coverage; it does not verify true parentage or ARCH-08 sole-fusion-authority.

**Evidence.** `src/fce_poc/policy/bundle.py` (`covers_merge`); RULE-POL-002.

**Trace.** FCE-REQ-KRN-011, H1; matches the freeze-record field-13 parentage deferral.
**Disposition.** Open, non-blocking. Deferred to **M5** (Sprint 9/10) — true parentage
enforcement and self-declared-empty-parentage detection — not M7. Owner
sensor-fusion-engineer / architect. Low.

## Claim audit

**CLEAN.** EVD-M3 claims code-correctness only; it discloses the placeholder signature,
the injected clock (H4), and the mechanism-simulated PIP/RC-011 authN (H3/H4), and makes
no crypto, trusted-time, authentication, anti-replay, or parentage claim. Blocking: **no**.

## Facts / Assumptions / Judgment / Uncertainty

- FACT: findings 04–06 are properties of the committed Sprint 6 code (f48229e); 01 is
  fixed in that same commit; 02/03/05 are open test/defence-coverage gaps.
- ENGINEERING JUDGMENT: severities; carry-forward targets (02/03/05 → M7; 06 → M5;
  04 → H6).
- UNCERTAINTY: 05 closes with H4 trusted time; 06 with H1/M5 parentage enforcement.
