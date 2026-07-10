# Decision Record — FG-POS-001

**Title:** Ratification of Sahtune Fusion Guard as a Sahtune Fusion Capability Name
**Date:** 2026-07-10
**Status:** Approved — PENDING LEAD SIGN-OFF
**Owner:** Lead / product-strategy-reviewer
**Repo home (proposed):** `docs/12_decision_records/fg-pos-001.md` (append-only; standalone DR file)
**Trace:** `_SHARED_CONSTRAINTS.md`; fce-product-positioning approved baseline; RTM v0.5 (`docs/03_rtm.md`); EVD-M1..M7; repo HEAD `04129fe`.

> This DR is a **positioning/naming** decision only. It makes no change to the FCE architecture, schema, gate topology, RTM, evidence, or code baseline. It introduces no new requirement.

## Context

Kanatir previously submitted a proposal under the name **Fusion Guard**, describing a Sahtune Fusion capability for trusted sensor fusion, controlled data handling, auditability, and decision-support confidence **[C2: prior submission solicitation/date/filepath — requires artifact/link confirmation]**. Subsequent FCE work produced a stronger agent/skill engineering structure, an evidence-gated topology, and a stricter compliance-gate framing. A positioning decision is required so the resubmission preserves continuity with the prior Fusion Guard proposal without creating a sixth product or presenting Fusion Guard and FCE as unrelated product families.

## Decision

**Agreed formal product names (2026-07-10):** the mission-facing capability is **Sahtune Fusion Guard**; the implementation layer is **Sahtune Fusion Compliance Engine (FCE)**. No hyphen. Short forms "Fusion Guard" and "FCE" may be used after first use. The Sahtune-prefixed names are adopted partly to distinguish the capability from similarly named offerings by other vendors, while the embedded "Sahtune Fusion" signals a capability within the Fusion line rather than a top-level product.

Kanatir retains **Sahtune Fusion Guard** as a **mission-facing capability name within the Sahtune Fusion product lineage**. It is not a sixth product and not a standalone product family; it is a challenge-specific Sahtune Fusion capability focused on trusted sensor fusion, controlled data handling, auditability, provenance, and operator-reviewable decision support. The **Sahtune Fusion Compliance Engine (FCE)** is the upstream policy-enforcement, compliance-gate, provenance, and audit-control layer that implements and strengthens Fusion Guard's trusted-fusion functions.

**Approved product hierarchy (five products; Fusion Guard and FCE are capabilities within Fusion):**

Sahtune
- Sentinel
- Perception
- Fusion
  - Sahtune Fusion Guard — mission-facing trusted-fusion capability
  - Sahtune Fusion Compliance Engine (FCE) — upstream compliance-gate implementation layer
- Ground Control
- SwarmLink

## Options considered

1. **Promote Fusion Guard to a standalone (sixth) product.** Rejected — invites product-line inflation, whole-product TRL claims, and fragmentation objections; contradicts the fce-product-positioning baseline (five products).
2. **Drop the Fusion Guard name; submit as "FCE" only.** Rejected — breaks continuity with the already-submitted Fusion Guard proposal.
3. **Retain Fusion Guard as a mission-facing capability name inside Sahtune Fusion, implemented through the FCE compliance-gate layer.** **Selected** — preserves continuity and the five-product line; separates mission-facing naming from technical implementation.

## Consequences

**Architecture impact: NONE.** The seven-gate topology (G1–G7), PDP/PEP/PAP/PIP model, 15-field envelope v0.2.0, 18-field audit schema, hash-chain and replay, no-unauthorized-merge kernel (ARCH-08), RTM v0.5, and EVD-M1..M7 are unchanged. Fusion Guard names an existing capability; FCE remains its implementation layer.

**Wording-consistency requirement (binding).** "Upstream compliance gate" describes the FCE enforcement boundary relative to downstream analytic exploitation. It must NOT be written in a way that implies the FCE performs no fusion-merge control: the no-unauthorized-merge control operates at the fusion-merge decision point (G5 / ARCH-08) and is demonstrated by EVD-M5 and EVD-M7. Correct framing: the FCE governs ingestion through the compliance-controlled fusion-merge decision (G1–G5) and emits audited, policy-compliant fused objects; "downstream fusion analytics" is the exploitation layer that consumes those objects.

**Positioning constraints carried forward:**
- External description (approved, verbatim): "Fusion Guard is a Sahtune Fusion capability. The revised architecture incorporates the Fusion Compliance Engine as its upstream policy-enforcement, provenance, and audit-control layer."
- On first use, qualify "Sahtune Fusion Guard" as "a Sahtune Fusion capability" so it does not read as a top-level product.
- Prohibited: Fusion Guard as Kanatir's sixth product; Fusion Guard and FCE as separate product families; FCE certifies/accredits/authorizes classified processing; any claim of demonstrated isolation, edge deployment, or performance not backed by a named artifact.
- "Independently deployable" and "downstream failure isolation" are written as **architecture intent / design objective** until packaged-deployment and isolation tests exist. **[C3: architecture artifact `docs/04`/`docs/18` — requires artifact/link confirmation]**
- TRL claims are capability-specific and evidence-specific; Fusion Guard/FCE readiness is not inherited from or extended to other Sahtune modules.

## Conditions before external use (open)

- **C2** — prior Fusion Guard submission: solicitation name/number, submission date, file/path. **[open]**
- **C3** — architecture artifact supporting the Fusion Guard/FCE boundary. **[open]**
- RTM rows mapping Fusion Guard/FCE functions to evidence (see resubmission pack §8). **[drafted; verify at transport]**
- Red-team claim audit on final submission text. **[pending final text]**

## Sign-off

Lead: __________________________  Date: __________ (pending)
