# 01 — Executive Technical Concept

Owner: `fce-lead-systems-architect`.
Language gated by `fce-product-positioning` and `fce-documentation-style`.

## Positioning (website-safe, verbatim baseline)

"Fusion is the multi-sensor operating-picture layer inside Sahtune. For
defence and government workflows, Fusion includes a Fusion Compliance Engine
capability that enforces machine-readable classification, release, provenance,
and audit policies before sensor data reaches downstream analytics."

The Fusion Compliance Engine (FCE) is a capability inside Sahtune Fusion, not a
sixth product. The Sahtune line remains: Sentinel, Perception, Fusion, Ground
Control, SwarmLink. [FACT]

## Problem [ENGINEERING JUDGMENT]

Multi-sensor fusion mixes data of differing classification, releasability,
domain, and provenance. Without a deterministic control layer, fusion can
silently merge inputs policy would forbid, drop provenance, or emit outputs no
one can audit afterward.

## Concept

The FCE sits between sensor ingestion and downstream analytics. It binds
machine-readable metadata to every object and routes each object through seven
ordered gates (`05`). A deterministic Policy Decision Point (`07`) evaluates
each object against a signed, versioned policy bundle under default-deny.

Fusion outputs obey a no-unauthorized-merge invariant enforced by a Fusion
Compliance Kernel. Every decision emits a tamper-evident, hash-chained audit
record (`08`) sufficient to replay the decision sequence deterministically.

AI may advise only: anomaly detection, classification recommendation, conflict
detection, confidence scoring. AI never decides. The final compliance decision
is deterministic, rule-governed, and auditable.

## Design invariants [FACT — from `_SHARED_CONSTRAINTS.md`]

1. Default-deny / fail-closed on missing, malformed, expired, ambiguous, or
   unverifiable input.
2. AI advisory only; no decision rests solely on black-box AI output.
3. Deterministic enforcement; outcome does not vary by timing or thread order.
4. Total auditability; audit loss is itself a fail-closed trigger.
5. No-unauthorized-merge across domain, classification, and caveat.
6. Zero-trust boundaries between all components.

## What the FCE is not

- Not certified, accredited, endorsed, or authorized to operate or to process
  classified or controlled data. This package makes no such claim.
- Not a performance product; all numbers elsewhere are internal TARGETs to be
  verified on named hardware.
- Not dependent on any vendor accelerator; the NVIDIA track (`13`) is an
  optional evaluation track only, never in the compliance path.

## Scope

Architecture artifacts and TRL 1-3 planning. After requirements are baselined,
the project expects minimal local proof-of-concept code for schema validation,
policy evaluation, audit/provenance output, and synthetic/mock-data test
evidence. Production, operational, deployed, classified-processing, and
externally installed implementation work remains out of scope unless separately
approved.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: positioning baseline and invariants quoted from the library.
- Assumptions: mission framing (joint ISR, maritime, tactical edge, UAV) per
  `09`, pending solicitation confirmation.
- Judgment: the seven-gate decomposition and the AI-advisory boundary.
- Uncertainty: exact DND outcome wording (OPEN-01).
