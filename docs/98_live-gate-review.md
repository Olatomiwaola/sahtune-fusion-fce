# 98 — Live Gate Review (Red-Team + Security-Assurance) v1

Supersedes the design-time self-review in `99_gate-review.md`.
Produced by live passes of the `red-team-reviewer` and `security-assurance-engineer`
agents over `docs/00`–`13`, `README`, and `99`. Read-only review; no files were
changed by the agents; no installs; `.claude/` untouched.

## Consolidated verdict

**APPROVE-WITH-CONDITIONS** (both agents concur).
Scope is design-only at TRL 1-3. No executable gate-bypass or permit-by-default
was demonstrated, so a block verdict is not warranted at design stage. However,
the red-team pass found latent specification-level bypass/escalation routes, so
the "no path skips the seven gates" assertion in `04`/`05`/`99` **must not be
treated as final** until conditions B1–B3 below are closed in the design text.
The threat-level item THR-KRN-001 (unauthorized merge) remains
blocking-until-verified by test.

## Blocking-in-text (close before the no-bypass claim stands, before any external-facing use, before TRL 4-5 entry)

| ID | Condition | Source | Affected REQ / element |
|---|---|---|---|
| B1 | Authenticate and integrity-bind every PIP-sourced attribute (mission, user, sensor, classification, domain, caveat, timestamp, network state, operational context); unverifiable attributes fail closed at G4. Add new threat THR-PIP-001. | RT-01, SEC Lens 1 | ARCH-06→ARCH-03, FCE-REQ-SEC-001, FCE-REQ-POL-011 |
| B2 | State explicitly that operator override (RC-007) cannot relax the no-unauthorized-merge invariant or a cross-domain/domain-mismatch block; override acts only within an already-permitted envelope. | RT-02 | ARCH-13, ARCH-08, FCE-REQ-OPS-002, FCE-REQ-KRN-010 |
| B3 | Make `policy_binding_state` FCE-authority-set only: force to `unvalidated` at G1 regardless of the ingested value; never trust it from the source (consider removing it from the source-supplied schema). | RT-03 | ARCH-01, `06` field 15, FCE-REQ-MET-010 |

**Status update:** B1, B2, and B3 are now **CLOSED IN TEXT** by the documentation
pass recorded in `97_b1-b3-closure-review.md` (edits to `04`, `05`, `06`, `07`,
`10`, `11`). They remain to be **demonstrated by test** at TRL 4-5 (tracked under
H9). The "no path skips the seven gates" assertion may now reference these
text closures, but is still not final until H9 verification.

## High-priority (close before TRL 4-5 exit)

| ID | Condition | Source |
|---|---|---|
| H1 | Enforce ARCH-08 as the sole fusion authority; add detection for objects declaring empty parentage with low labels (self-declared parentage evades high-water mark). | RT-04 |
| H2 | Define and verify the downgrade transformation-proof structure, its authority binding, and its verification point; until defined, disable downgrade or always route to human review. | RT-05 |
| H3 | Enumerate all admin, debug, maintenance, and telemetry interfaces with a per-interface authN/authZ and gate-traversal story, or state explicitly that none exist by design. | RT-06, SEC Lens 2 |
| H4 | Specify a trusted/attested time source that G3 freshness validates against; treat unverifiable `clock_source` as fail-closed; add clock-independent anti-replay (nonce/sequence). | RT-07, SEC Lens 5 |
| H5 | Add a security-critical bundle-change class (e.g., emergency permit revocation) that forces in-flight re-evaluation or fail-closed hold rather than completing under the G4-pinned version. | RT-08 |
| H6 | Specify append-only enforcement and external chain anchoring for the audit log; define the cryptographic root-of-trust and key management (bundle/object/audit signing, sensor credentials; secure storage, rotation, revocation) to replace placeholders; qualify "tamper-evident" as "once anchoring/signature is implemented and assessed." | RT-09, SEC Lens 8 (C5) |
| H7 | Specify the audit-chain-writer serialization/total-ordering model and test concurrent gate evaluation (avoid chain fork/ordering ambiguity). | SEC Lens 4 (C2) |
| H8 | Define deterministic cross-object bundle-version resolution at G5 so a merge of differently-pinned parents is deterministic. | SEC Lens 4 (C4) |
| H9 | Demonstrate no-bypass (FCE-REQ-KRN-001) and no-unauthorized-merge (FCE-REQ-KRN-010) by property-based and red-team test at TRL 4-5. | SEC Lens 6 (C3), RT-01/02/03 |
| H10 | Add anti-rollback / monotonic version-floor to update and policy-bundle workflows (rollback is a downgrade-attack surface). | SEC Lens 8 (C6) |
| H11 | Add edge at-rest protection, secure boot, and physical-tamper posture for audit/provenance stores; extend THR-EDG-002 to extraction/tamper. | SEC Lens 8 (C7) |
| H12 | Add a two-person / content-review control on policy-bundle publication (a validly-signed but over-broad authored permit causes underblocking; signature alone is insufficient). | SEC Lens 6 (C8) |
| H13 | Specify authentication of the destination/receiver on cross-domain release (ARCH-11) and authorization for who may pull audit exports (ARCH-10). | SEC Lens 2 |
| H14 | Extend the audit schema to represent unauthenticated-source-rejection events at G1 (so source-spoof attempts are logged and non-repudiable even with no authenticable actor). | RT-... / SEC Lens 7 (C10) |

## Low-priority / documentation-level (track; several are quick text fixes)

| ID | Item | Source |
|---|---|---|
| L1 | Gate `data_origin: LIVE` behind an explicit authorization control or restrict the schema to SYNTHETIC at this TRL; SYNTHETIC banner keys off `data_origin`, fail-closed on absence. | RT-10 |
| L2 | Align G1 text ("object signature if present") with the schema; when a per-object signature is mandated, absence must fail closed, not pass. | RT-11 |
| L3 | State that audit replay is read-only reconstruction that cannot release data; any mission-replay re-ingestion re-traverses G1–G7. | RT-12, SEC Lens 6 |
| L4 | Keep "Protected B" strictly as a referenced external handling target (never a rendered/applied marking); re-check against the verbatim solicitation once OPEN-01/02 resolve. | RT-13 |
| L5 | Capture the freshness/clock evaluation reference in the audit record so replay is faithful to a freshness-driven disposition. | SEC Lens 5 (C9) |

## New threats to add to the register (`10`)

THR-PIP-001 (PIP attribute spoofing); override-vs-merge escalation; source-supplied
`policy_binding_state` pre-marking; self-declared empty parentage; downgrade-proof
forgery; emergency-revocation latency (hot-reload fail-open window); update
rollback/downgrade attack; edge key extraction / physical tamper;
unauthenticated-source-rejection audit gap; release-destination authentication gap.

## Claim audit — CLEAN (red-team confirmed, no finding)

No certification / accreditation / ATO; no government endorsement; no operational
deployment; no classified-processing authority; no verified performance stated as
fact (all TARGET); no vendor claim stated as fact (all VENDOR CLAIM, unverified);
no fabricated solicitation text (paraphrased anchors flagged, OPEN-01); no
unlabelled synthetic data; no AI-as-sole-authority path (every decision cites a
deterministic rule ID; deterministic-without-AI fallback present).

## Handoffs

- Missing requirements (B1, H1): route to `requirements-traceability-engineer`.
- Test formalization (B1–B3, H1–H9): route to `test-evaluation-engineer`; each
  finding carries a suggested red-team test hook.
- Crypto/key-management and edge-hardening (H6, H10, H11): `security-assurance-engineer`
  and `devsecops-engineer`.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: both agents returned approve-with-conditions; the listed findings are
  evidence-linked to file and section in the package.
- Assumptions: conditions close before TRL 4-5 and before any external trust.
- Judgment: B1–B3 are text-closable now; the remainder need design or test work.
- Uncertainty: cross-domain topology (OPEN-03), key management, and edge tamper
  cannot be fully assessed until deployment and crypto designs exist.
