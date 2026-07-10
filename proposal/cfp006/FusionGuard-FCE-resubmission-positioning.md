# Sahtune Fusion Guard × FCE — Resubmission Positioning & Architecture Pack

**Role blocks:** product-strategy-reviewer (positioning) → proposal-compliance-writer (evaluator-facing language) → red-team-reviewer (§9, findings only).
**Discipline:** every capability claim traces to a named artifact at repo HEAD `04129fe`, or is marked **[requires artifact/link confirmation]**. No certification/accreditation/ATO/endorsement/classified-processing language. Standards = reference alignment only. Performance figures = TARGET.

**Standing confirmations needed before external use:**
- **C1** — "Fusion Guard" is ratified as the mission-facing capability name via DR-FG-POS-001 (2026-07-10, pending lead sign-off). **[sign-off pending]**
- **C2** — Which solicitation the original Fusion Guard proposal was submitted under, and its file/reference, so continuity language cites a real prior submission. **[requires artifact/link confirmation]**
- **C3** — Deployment-isolation / separate-process-boundary claims (blast-radius) are architectural intent; confirm the design artifact (`docs/04`, `docs/18`) and note no isolation test exists at TRL 3. **[requires artifact/link confirmation]**

**Agreed formal names (2026-07-10, no hyphen):** mission-facing capability = **Sahtune Fusion Guard**; implementation layer = **Sahtune Fusion Compliance Engine (FCE)**. On first use in any section, qualify as "a Sahtune Fusion capability" so the name does not read as a sixth top-level product; short forms "Fusion Guard" and "FCE" may be used after first use. The Sahtune-prefixed names are adopted partly to distinguish the capability from similarly named offerings by other vendors.

**Wording-consistency rule (binding, from DR-FG-POS-001):** "upstream compliance gate" means upstream of the downstream analytic-exploitation layer. The no-unauthorized-merge control operates at the fusion-merge decision point (G5 / ARCH-08) inside the FCE, per EVD-M5/M7. Never write it as if the FCE omits fusion.

---

## 1. Strategic recommendation — a Sahtune Fusion capability, not a sixth product

**Recommendation: keep Sahtune Fusion Guard inside Sahtune Fusion as a named capability; do not create a sixth product.**

Rationale, procurement-aware:
- **Coherence signal.** A defence evaluator reads a new product per RFP as fragmentation and integration risk. One product line (Sahtune) with challenge-specific mission configurations reads as a deliberate autonomy-software stack.
- **TRL integrity.** As a capability, readiness is claimed only from its own evidence (EVD-M1..M7), which an evaluator can audit — not from a whole-product claim.
- **Continuity.** The prior Fusion Guard submission is preserved as lineage rather than orphaned; the resubmission is an evidence-and-architecture upgrade of an existing capability.
- **Reuse.** The FCE gate is independently deployable (as design intent), so DND can obtain the trusted-fusion/compliance capability without buying the full analytics stack.

Sahtune Fusion Guard is the mission-facing name; Sahtune Fusion Compliance Engine (FCE) is the upstream compliance-gate implementation layer that strengthens it. Both live under Sahtune Fusion.

---

## 2. Corrected product hierarchy (evaluator-facing = simple)

Sahtune (product lineage)
- Sentinel
- Perception
- Fusion
  - **Sahtune Fusion Guard** — mission-facing trusted-fusion capability
  - **Sahtune Fusion Compliance Engine (FCE)** — upstream compliance-gate implementation layer for Fusion Guard
- Ground Control
- SwarmLink

Five products; Fusion Guard and FCE are capabilities within Fusion. Evaluator-facing wording stays one line:

> "Fusion Guard is a Sahtune Fusion capability. The revised architecture incorporates the Fusion Compliance Engine as its upstream policy-enforcement, provenance, and audit-control layer."

(That sentence is the approved verbatim external baseline; the full names Sahtune Fusion Guard / Sahtune Fusion Compliance Engine are used for headings and first mentions.)

---

## 3. Resubmission positioning paragraph (proposal-safe)

Sahtune Fusion Guard, a Sahtune Fusion capability, remains a Sahtune Fusion capability, not a standalone sixth product. In this resubmission, Fusion Guard is refined as an **evidence-gated mission configuration of Sahtune Fusion**, with the Sahtune Fusion Compliance Engine (FCE) providing the upstream compliance, policy-enforcement, provenance, and audit-control layer. The FCE gate intercepts incoming sensor and event data before it reaches downstream fusion analytics, and enforces machine-readable classification, release, provenance, and audit policy at that boundary; the no-unauthorized-merge control operates at the fusion-merge decision point (G5), inside the FCE. The capability is designed to be independently deployable: where an operational requirement does not need the full Sahtune analytics stack, Fusion Guard can be fielded as a lightweight upstream gate. This continues the previously submitted Fusion Guard concept **[C2: prior submission ref requires confirmation]** while strengthening it with the newer agent/skill engineering structure, evidence-gated topology, and stricter compliance-gate framing developed in the FCE work.

---

## 4. Technical architecture narrative (for a government evaluator)

**Upstream compliance gate.** The Sahtune Fusion Compliance Engine (FCE) layer sits between raw sensor/event ingestion and the downstream fusion analytics bus. Every incoming packet is validated against a machine-readable policy bundle, bound to classification/domain/release metadata, hash-recorded, and then permitted, restricted, blocked, quarantined, routed, or segregated before any analytics see it. The FCE governs ingestion through the compliance-controlled fusion-merge decision (gates G1–G5) and emits audited, policy-compliant fused objects; "downstream fusion analytics" is the exploitation layer that consumes those objects. The no-unauthorized-merge control operates at the fusion-merge decision point (G5 / ARCH-08), inside the FCE — "upstream compliance gate" means upstream of the exploitation layer, not that the FCE omits fusion. Demonstrated at laptop scale across the seven-gate pipeline (G1–G7). [FACT: EVD-M3 policy decision; EVD-M5 fusion-gate enforcement; EVD-M7 held-out run]

**Decoupled execution and enforcement boundary.** The gate is designed to be independently deployable and isolated from downstream analytics, so that a failure or compromise in downstream fusion cannot bypass policy enforcement, suppress audit generation, or defeat fail-closed ingestion. At TRL 3 the enforcement logic and fail-closed behaviour are demonstrated in-process; the separate-deployment/process-isolation boundary is architectural design intent and is **[C3: requires artifact/link confirmation — docs/04, docs/18; no isolation test at TRL 3]**.

**Versioned interface boundary.** Data crosses the boundary as a versioned event envelope (15-field schema frozen at v0.2.0) governed by a schema contract with fail-closed rejection of unknown or missing fields, and policy is applied from a version-pinned bundle. New sensor modalities, mappers, or policy rules are added by extending the envelope/bundle under version control rather than rewriting the core engine. [FACT: EVD-M2 schema validation; schema freeze FCE-DR-SCH-001/002; bundle pin `proj-baseline@0.2.0`]

**Audit and provenance.** Each accepted, blocked, quarantined, or routed event generates a tamper-evident, hash-chained audit record; fused or derived objects preserve lineage to their source events and audit identifiers via kernel-recorded parentage, and the decision sequence is deterministically replayable from audit records alone (94 records, integrity-manifest recompute verified on the held-out run). [FACT: EVD-M4 audit chain/replay; EVD-M5 parentage; EVD-M7 R1/R2]

**Fail-closed behaviour.** When required policy, source, labeling, authorization, or audit conditions are not satisfied, the event is blocked or quarantined rather than passed downstream: malformed/unknown-field and integrity-failed objects quarantine, unauthenticated policy-information attributes fail closed, and unauthorized cross-domain merges are segregated with a reason code and audit event. [FACT: EVD-M2; EVD-M5; EVD-M7 oracle cases]

**Evidence-gated validation.** Capability is not asserted generically: it is validated by a sealed held-out evaluation under a policy bundle pinned before results existed, with a blind split seed committed before any data was downloaded, and negative results reported verbatim (9/10 oracle match, 1 disclosed negative). [FACT: EVD-M6 seal; EVD-M7 report; decision register]

---

## 5. Operational Boundary Clause (proposal-safe)

> **Operational Boundary.** The Sahtune Fusion Guard capability, implemented through the Sahtune Fusion Compliance Engine (FCE) gate, operates as an upstream compliance, policy-enforcement, provenance, and audit-control boundary within the Sahtune Fusion product lineage. It is designed to be independently deployable and does not require the broader Sahtune analytics stack, nor any other challenge-specific Sahtune module (Sentinel, Perception, Ground Control, SwarmLink), to perform its compliance function. The FCE gate governs ingestion through the compliance-controlled fusion-merge decision and sits upstream of the downstream fusion analytics (exploitation) layer, maintaining a separate enforcement boundary: policy decisions, no-unauthorized-merge controls, fail-closed ingestion, and audit generation are performed at the gate and are designed not to be bypassable by downstream analytics failure. Maturity, evidence, and readiness claims for the Fusion Guard/FCE capability are specific to that capability and are traced only to its own artifacts; they are not inherited from, and do not extend to, other Sahtune modules. **[C3: separate-deployment isolation is design intent; isolation testing is follow-on TRL 4–5 work — requires artifact/link confirmation.]**

---

## 6. Wording to avoid (hard prohibitions)

Do not use, imply, or paraphrase:
- **certified / accredited / ATO / authority to operate / approved for classified or controlled data / classified-processing authority** — the FCE claims none of these.
- **"compliant with ITSG-33 / NIST / NASA / STANAG"** — substitute "designed with reference alignment to the disciplines of …".
- **government endorsement / DND-approved / operationally deployed / in service / fielded** (as present tense).
- **measured/guaranteed performance** stated as fact — all latency/throughput/SWaP figures are TARGET, to be verified; never "real-time" without the "TARGET, unmeasured" qualifier.
- **"meets DND requirements" / internal targets framed as met requirements** — targets are internal until verified with provenance.
- **whole-product or cross-module TRL claims** ("Sahtune is TRL X") — claim only the Fusion Guard/FCE capability TRL from its own evidence.
- **vendor tooling as a differentiator** (including NVIDIA) unless Kanatir-benchmarked with provenance.
- **"trusted time / cryptographically signed / tamper-proof"** — the current build uses placeholder crypto and injected/clock-bounded time (H4/H6); say "tamper-evident (hash-chained)" and disclose the boundary.
- **"fully autonomous compliance / no human needed"** — say auto-disposition of predefined policy conditions; undefined/ambiguous default-deny to human review.
- **"Sahtune Fusion Guard" written as a top-level product** parallel to Sentinel/Perception — always qualify as a Sahtune Fusion capability on first use.

---

## 7. Revised executive-summary paragraph (resubmission)

Sahtune Fusion Guard, a Sahtune Fusion capability, provides trusted sensor fusion, controlled data handling, auditability, and decision-support confidence. In this resubmission it is refined as an evidence-gated mission configuration of Sahtune Fusion: the Sahtune Fusion Compliance Engine (FCE) provides an upstream, independently deployable (by design) compliance gate that validates, labels, hash-records, routes, blocks, and audits sensor and event data against a version-pinned, machine-readable policy bundle before that data reaches downstream fusion analytics. The gate is deterministic and fail-closed — artificial intelligence is advisory only, and no enforcement decision depends solely on an AI output. The no-unauthorized-merge control operates at the fusion-merge decision point inside the FCE. The capability has completed an analytical and experimental proof of concept of its critical compliance functions (deterministic policy decision, no-unauthorized-merge enforcement, tamper-evident audit lineage, and fail-closed ingestion), validated through a sealed held-out evaluation under a pre-committed protocol with negative results reported verbatim. Readiness and evidence claims are specific to the Fusion Guard/FCE capability and are traced to named artifacts; they are not extended to other Sahtune modules. Where an operational requirement does not need the full analytics stack, Fusion Guard can be fielded as a lightweight upstream compliance gate.

---

## 8. RTM-style table (requirement → module/function → evidence expected → verification)

| # | Requirement (capability) | Module / function | Evidence (named artifact) | Verification method |
|---|---|---|---|---|
| R1 | Intercept and enforce policy on incoming events before downstream analytics | FCE gate G1–G4 ingestion/policy | EVD-M2 `unit_test_report.md`; EVD-M3 `policy_eval_report.md` | unit test, integration test |
| R2 | Deterministic policy decision (identical inputs + pinned bundle → identical decision) | PDP/PEP determinism | EVD-M3; EVD-M7 byte-identical replay | property-based test |
| R3 | No-unauthorized-merge across domains; segregate + reason code + audit | Fusion kernel G5 (inside FCE) | EVD-M5 `fusion_merge_report.md`; EVD-M7 held-out `unauthorized_merge` case | property-based test, red-team test |
| R4 | Tamper-evident, append-only audit; deterministic replay from records | Audit chain / replay | EVD-M4 `audit_report.md`; EVD-M7 R1/R2 (94 records, manifest match) | integration test, analysis |
| R5 | Provenance/lineage from source events to fused outputs via kernel-recorded parentage | Provenance graph | EVD-M4; EVD-M5; EVD-M7 `forged_parentage` case | property-based test |
| R6 | Fail-closed on missing policy/source/label/authz/audit conditions | All gates | EVD-M2 (malformed/unknown); EVD-M3 (RC paths); EVD-M7 oracle set | unit test, red-team test |
| R7 | Versioned interface boundary; add modalities/rules without core rewrite | Schema v0.2.0 + pinned bundle | EVD-M2; FCE-DR-SCH-001/002; seal record `sprint12_seal.md` | inspection, unit test |
| R8 | Evidence-gated validation under sealed, pre-pinned protocol; verbatim negatives | Held-out harness | EVD-M6 `fixture_report.md`; EVD-M7 `heldout_eval_report.md` | simulation, acceptance test |
| R9 | Independently deployable; downstream failure cannot bypass the gate | Deployment/isolation boundary | `docs/04`, `docs/18` architecture **[requires artifact/link confirmation; no isolation test at TRL 3]** | design review; test = TRL 4–5 |
| R10 | Explainable decisions + controlled override with accountability | Explanation surface / override | EVD-M7 (TST-EXP-001..004); RTM FCE-REQ-OPS-001/-002 | inspection, integration test |

All rows except R9 map to committed evidence at HEAD `04129fe`; R9 is design-level and flagged.

---

## 9. Red-team critique (DRDC/DND evaluator perspective) — findings only

- **RT-1 (isolation is asserted, not shown).** R9/blast-radius separation is the load-bearing claim for "downstream failure cannot compromise the gate," yet at TRL 3 the PoC is single-process laptop scale. **Disposition:** frame as design intent + TRL 4–5 test item; do not state as demonstrated.
- **RT-2 ("independently deployable" vs demonstrated).** Deployability is architectural; no packaged/deployed artifact is in evidence. **Disposition:** say "designed to be independently deployable"; mark deployment artifact **[requires confirmation]**.
- **RT-3 (Fusion Guard name provenance).** If the evaluator cross-checks the prior submission and the name/lineage differs, continuity language is exposed. **Disposition:** resolve C1/C2 before submission; cite the prior file.
- **RT-4 (TRL dilution risk in reverse).** Naming FCE and Fusion Guard together can read as one capability inheriting another's maturity. **Disposition:** the Operational Boundary Clause confines readiness claims to the Fusion Guard/FCE capability; keep that clause adjacent to any TRL statement.
- **RT-5 (name product read).** "Sahtune Fusion Guard" should not read as a top-level product parallel to Sentinel. **Disposition:** always qualify "a Sahtune Fusion capability" at first use; the embedded "Sahtune Fusion" reduces but does not remove the risk.
- **RT-6 ("trusted fusion" overtone).** "Trusted" can imply an accreditation/assurance status. **Disposition:** define "trusted-fusion" operationally (deterministic, fail-closed, auditable) at first use.
- **RT-7 (audit "tamper-evident" vs "tamper-proof").** Hash-chaining is tamper-evident, not tamper-proof; crypto is placeholder (H6). **Disposition:** use "tamper-evident (hash-chained)"; disclose H6.
- **RT-8 (real-time claim).** Performance figures are TARGET only (OPEN-03). **Disposition:** qualify every performance mention as TARGET/unmeasured.

**Red-team status: PASS-WITH-CONDITIONS** — release-safe once C1–C3 are confirmed and the design-intent phrasing (RT-1/RT-2) and first-use qualifier (RT-5) are retained.

---

## 10. Final recommended wording block (paste-ready)

> **Sahtune Fusion Guard — a Sahtune Fusion capability (resubmission).**
> Sahtune Fusion Guard, a Sahtune Fusion capability, provides trusted sensor fusion, controlled data handling, auditability, and decision-support confidence — it is not a standalone product. In this resubmission, Fusion Guard is refined as an evidence-gated mission configuration of Sahtune Fusion, with the Sahtune Fusion Compliance Engine (FCE) providing its upstream policy-enforcement, provenance, and audit-control layer.
>
> The FCE gate intercepts incoming sensor and event data before it reaches downstream fusion analytics and, against a version-pinned machine-readable policy bundle, validates, labels, hash-records, routes, blocks, quarantines, or segregates each event. The FCE governs ingestion through the compliance-controlled fusion-merge decision (gates G1–G5) and emits audited, policy-compliant fused objects that downstream fusion analytics consume; the no-unauthorized-merge control operates at the fusion-merge decision point inside the FCE. Decisions are deterministic and fail-closed; artificial intelligence is advisory only and no enforcement decision depends solely on an AI output. Each accepted, blocked, or routed event produces a tamper-evident (hash-chained) audit record, and fused outputs preserve lineage to their source events and audit identifiers.
>
> The capability is designed to be independently deployable: where an operational requirement does not need the full Sahtune analytics stack, Fusion Guard can be fielded as a lightweight upstream compliance gate. It maintains a separate enforcement boundary upstream of the downstream fusion analytics (exploitation) layer, so that policy enforcement, audit generation, no-unauthorized-merge controls, and fail-closed ingestion are designed not to be bypassable by downstream analytics failure. Deployment-isolation testing is planned follow-on work.
>
> Sahtune Fusion Guard / FCE has completed an analytical and experimental proof of concept of its critical compliance functions, validated through a sealed held-out evaluation under a pre-committed protocol with negative results reported verbatim. Readiness and evidence claims are specific to this capability, traced to named artifacts, and are not extended to other Sahtune modules (Sentinel, Perception, Ground Control, SwarmLink). The capability is designed with reference alignment to the disciplines of policy-as-code, zero-trust architecture, and provenance modelling; it does not claim certification, accreditation, authority to operate, or authority to process classified or controlled data. All performance figures are internal targets, to be verified.
