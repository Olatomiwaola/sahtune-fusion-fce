# RT-M6S11 — Red-team review, Sprint 11 scenario library candidate set

Reviewed: docs/09 v1 candidate set (draft + chain amendments), 2026-07-07.
Reviewer: red-team-reviewer role block (M6 chat). Findings written to repo by
the main session on the reviewer's behalf (read-only role). All findings
dispositioned by lead 2026-07-07; none blocking. Claim audit: CLEAN.

| ID | Sev | Finding | Component | REQ | Disposition (lead 2026-07-07) |
|---|---|---|---|---|---|
| RT-M6S11-01 | High | TST-POL-007 as first minted placed the permitted channel subset in policy-decision event_detail, violating the closed D2 sub-schema (FCE-DR-AUD-001; FU-M4S8-1 required trio); the fixture's own record would be writer-refused | TST-POL-007 / docs/08 | FCE-REQ-POL-011, FCE-REQ-AUD-001 | Path (b): subset carried in rules-fired citation + FCE-REQ-OPS-001 explanation + expected-output text; docs/08 unchanged; writer-rejection hook added (unknown `permitted_channels` detail field refused fail-closed) |
| RT-M6S11-02 | Med | Item 2.5 routing underspecified — a relabeling implementation would create a label-write path outside ARCH-07/ARCH-08 single-writer authority | item 2.5 / TST-POL-008 | FCE-REQ-POL-011, FCE-REQ-PRV-001 | Routing is a delivery disposition only: envelope and labels unchanged; destination only in the routing-class audit record; envelope-hash-invariance hook added |
| RT-M6S11-03 | Med | DR-SCH-005 transitive-resolvability check timing unstated — construction-only check leaves re-entry carrying an unsupported class | FCE-DR-SCH-005 | FCE-REQ-PRV-002, FCE-REQ-MET-010 | Construction-time minimum + fail-closed re-verification at any G2 re-entry, stated in the DR; re-entry hook added |
| RT-M6S11-04 | Low | duplicate_object_id coverage was a hedge ("available if exercised") — neither fixture nor stated gap | variant matrix | FCE-REQ-MET-010 | Explicit duplicate-ID case added to the malformed family (quarantine via RC-001 path + flag, FCE-DR-SCH-004 D5) |
| RT-M6S11-05 | Low | Mechanical window-widening executes after partial data exposure; residual disclosure needed | trim protocol integration | FCE-REQ-ING-010 | Trim report states fired/not-fired with before/after candidate-pair counts; mitigations (pre-committed floor, additive-only, seed-deterministic split, pre-evaluation seal) recorded |

Claim audit: no certification/endorsement/ATO language; RC-004
fixture-vs-demonstration boundary carried; "-like" discipline held;
acoustic_like framed as fixture role with manifest disclosure; no vendor
claims; no internal targets framed as requirements. EVD-M6 must preserve
representation-vs-demonstration phrasing.
