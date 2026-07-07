# RT-M5S9 — Red-Team Findings: M5 Sprint 9 Fusion-Kernel Candidate Set

Repo home: `docs/06_security/red_team_findings/RT-M5S9.md`. Reviewer:
`red-team-reviewer` (read-only; file written by the main session on its
behalf). Reviewed: Sprint 9 conditioned candidate set RU-M5-03..07 +
security conditions C1–C3 + FCE-REQ-KRN-012 (chat state, pre-write).
Dispositions: architect disposition block + lead concurrence 2026-07-06.
Claim audit: clean apart from RT-M5S9-06 (wording, fixed by disposition).
Blocking: NO (conditional amendments accepted into the write set).

Related: SEC-M5S9-01 (security-assurance finding, Medium — lifecycle-type
spoofing vs one-directional cross-check; mitigated by condition C3,
bidirectional check). C1–C3 accepted by lead 2026-07-06.

| ID | Severity | Finding | Component | REQ IDs | Test hook | Disposition |
|---|---|---|---|---|---|---|
| RT-M5S9-01 | Medium | Per-tuple membership `covers()` authorizes unintended tuple combinations (permit listing [T1,T2] silently covers [T1,T1], [T2,T2], any multiset from {T1,T2}); deny-by-default survives but permits are broader than authored intent | RU-M5-04 MERGE-PERMIT | FCE-REQ-KRN-011, FCE-REQ-KRN-012 | TST-POL-002 extension: [T1,T2] must not cover [T1,T1] | ACCEPTED 2026-07-06: `permitted_combinations` exact-multiset semantics; `max_parents` dropped (combinations fix their own cardinality) |
| RT-M5S9-02 | Low | Segregation set-bar evadable by set-composition change (add a third object = "different set") | RU-M5-03 §6 | FCE-REQ-KRN-011 | Superset re-request still denied absent covering combination | ACCEPTED 2026-07-06: bar labelled defense-in-depth only; every re-request faces full permit check |
| RT-M5S9-03 | Low | Degenerate/self-merge undefined: same `object_id` twice, or duplicate-source identical tuples; self-merge could launder an object into a fresh derived identity | RU-M5-03 §2 | FCE-REQ-KRN-011, FCE-REQ-KRN-012, FCE-REQ-PRV-002 | Duplicate `object_id` → refuse; [T,T] permitted only when enumerated | ACCEPTED 2026-07-06: ≥2 distinct object_ids required, duplicate refused fail-closed (RC-001 path); [T,T] resolved by -01 exact-multiset semantics |
| RT-M5S9-04 | Low | C3 reverse arm (ARCH-09-known derivation output presenting as non-derived) had no test vector in V1–V6 | RU-M5-03 vectors, RU-M5-07 | FCE-REQ-KRN-012 | New V7 | ACCEPTED 2026-07-06: V7 added (quarantine, `unrecorded_parentage`) |
| RT-M5S9-05 | Low | Override-vs-quarantine escalation depends on fixture `permitted_envelope` excluding quarantine — unverified assumption | Sprint 10 fixture | FCE-REQ-OPS-002, FCE-REQ-POL-012 | Override vs RC-005 quarantine and vs `unrecorded_parentage` quarantine → both rejected | ACCEPTED 2026-07-06 as Sprint 10 test hook (EVD-M5 obligation) |
| RT-M5S9-06 | Wording | Unqualified "verified parentage" in G5 pass condition implies authentication not present at TRL 1-3 (G1 authN is mechanism-simulated, H3/H4) | RU-M5-06 | FCE-REQ-KRN-012 | n/a (wording) | ACCEPTED 2026-07-06: reworded to "kernel-recorded parentage cross-checked against ARCH-09" |

## Residual risks (disclosed, unclaimed)

- Fresh-uuid forgery outside FCE custody is invisible to ARCH-09; bounded by
  G1 source authentication, mechanism-simulated at TRL 1-3 (H3/H4 open).
- ARCH-09 store integrity and external anchoring: H6 (open).
- G5-entry cross-check cost unquantified: TARGET only, M8 scope.
- H8 (general cross-object bundle-version resolution) remains open; §5
  same-version rule is a TRL 1-3 narrowing.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: candidate-set contents as reviewed in-chat 2026-07-06; disposition
  record per architect block + lead concurrence.
- Assumptions: Sprint 10 fixture honours the RT-M5S9-05 envelope exclusion.
- Judgment: severity rankings.
- Uncertainty: none material to these findings; repo state remains subject
  to raw verification before commit.
