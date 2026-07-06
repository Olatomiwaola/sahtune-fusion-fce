# RT-M4S7 — Red-Team Findings: Audit Record Schema v1 + FCE-DR-AUD-001 + FCE-DR-SCH-004 (M4 Sprint 7)

Reviewer role: red-team-reviewer (read-only). Date: 2026-07-06.
Artifacts: docs/08_audit-record-schema.md v1 draft (as amended),
FCE-DR-AUD-001, FCE-DR-SCH-004. Ten attack classes considered. Claim audit:
CLEAN. Blocking: NO.

| ID | Sev | Finding | Component | REQ IDs | Disposition |
|---|---|---|---|---|---|
| RT-M4S7-01 | Medium | Whole-chain substitution undetectable from the file alone: attacker with filesystem write regenerates a self-consistent chain from the public genesis constant; R1 passes. External chain-head anchoring is H6 (open). | chain design | FCE-REQ-AUD-002 | Disclosure obligation FU-M4S7-1 (EVD-M4 boundary statement); manifests carry chain_head_hash as partial mitigation for exported packages. No TRL 1-3 test possible. |
| RT-M4S7-02 | Medium | Torn write defeats fail-closed intent silently: crash mid-line leaves a partial record; naive restart appends past it and the pipeline runs between crash and later detection. | writer | FCE-REQ-AUD-002, FCE-REQ-KRN-001 | FU-M4S7-2: tail-verify-on-start (refuse fail-closed on partial/broken tail) + torn-write corruption test, Sprint 8. |
| RT-M4S7-03 | Low | Replay poisoning via detail-asserted IDs: later forensic tooling joins on event_detail.source_asserted_object_id, reintroducing untrusted identity into lineage. | replay spec | FCE-REQ-AUD-003, FCE-REQ-PRV-002 | Spec line present (R2 reads source_object_ids/output_object_id only). Sprint 8 test hook: collision fixture — misleading source_asserted_object_id equal to a real object_id; assert lineage ignores it. |
| RT-M4S7-04 | Low | Sentinel abuse across classes: forged N/A-PRE-G4 on a policy-decision record hides the bundle version that fired. | requiredness matrix | FCE-REQ-AUD-001 | Sprint 8 test hook: per-class sentinel-legality rejection tests (explicit cases, not only generic matrix tests). |
| RT-M4S7-05 | Low | Cross-run object_id collision mis-joins lineage when aggregating multiple chains (per-run uniqueness, FCE-DR-SCH-004 D5). | export/replay | FCE-REQ-PRV-002 | FU-M4S7-3: compound-key disclosure — (package_id or run_id, object_id) — in docs/08 (done) and EVD-M4. |

Boundary-concern check (architect conditional): no trust boundary moved by
either DR; the G1 identity amendment strengthens an existing boundary. No
security-assurance block demanded before ratification.

Claim audit detail: RFC 8785 / W3C PROV / XACML phrased as reference
alignment only; signature placeholder (H6), injected clock (H4),
single-writer (H7), envelope-only hash binding, and mechanism-simulated
authentication all disclosed; JSONL+manifest scoped against FCE-REQ-EXP-001
without a three-format implementation claim; no
certification/accreditation/ATO language found.
