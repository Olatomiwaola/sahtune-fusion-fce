# 18 — Fusion-Kernel Merge Semantics v0.1

Owner: `sensor-fusion-engineer` with `fce-lead-systems-architect`.
Skills: `fce-policy-as-code` (merge-permit semantics), `fce-secure-architecture-review`.
Numbered docs/18 at write, 2026-07-06 (docs/17 reserved for the V&V plan).

v0.1 (M5 Sprint 9): initial spec. Incorporates security conditions C1–C3
(SEC-M5S9-01 mitigation, security-assurance review 2026-07-06) and red-team
dispositions RT-M5S9-01..06 (architect disposition + lead concurrence
2026-07-06). Closes RT-M3S6-06 / H1 at the interface level; test closure is
Sprint 10 (EVD-M5). No implementation code in Sprint 9.

## 1. Authority model — ARCH-08 sole fusion authority

Only the Fusion Compliance Kernel (ARCH-08) constructs fused or derived
objects. Construction is structurally coupled to the kernel decision:

- `parent_object_ids` on any kernel output is written by the kernel from its
  actual evaluated input set — never accepted from a caller, an adapter, or
  the object itself.
- Kernel-only write authority: fusion parent-link records in the provenance
  graph (ARCH-09) are writable only by ARCH-08. This is an explicit trust
  boundary (C2; docs/04 boundary list). If any other component could write
  fusion linkage, the G5-entry cross-check below would verify
  attacker-supplied truth.
- G5-entry bidirectional provenance cross-check (C3), run for every object
  arriving as a merge parent:
  - Forward: an object claiming a derived lifecycle type (tracklet, fused
    track, transformed object, downgraded object) must have kernel-recorded
    parentage in ARCH-09 matching its `parent_object_ids`.
  - Reverse: an object whose `object_id` appears in ARCH-09 as a derivation
    output must present as a derived type with matching parentage.
  - Any mismatch in either direction → quarantine (RC-001 path) with
    detection flag `unrecorded_parentage` and an audit event.
- A derived-type object with empty `parent_object_ids` fails closed at G2
  already (schema field 13); the kernel additionally asserts every claimed
  parent exists in ARCH-09 and was a member of the kernel's evaluated input
  set for the recorded decision.

This converts the no-unauthorized-merge invariant from label-coverage-only to
label-coverage-plus-kernel-recorded-parentage — the RT-M3S6-06 gap. Trace:
FCE-REQ-KRN-012 (RTM v0.5), FCE-REQ-KRN-011, FCE-REQ-PRV-002.

Residual (disclosed, not claimed): an object forged entirely outside FCE
custody under a fresh `object_id` is invisible to ARCH-09 and is bounded by
G1 source authentication, which is MECHANISM-SIMULATED at TRL 1-3 (H3/H4
open). ARCH-09 store integrity/anchoring is H6 (open).

## 2. ARCH-07 invocation (C1)

The Label Propagation Engine (ARCH-07) is a pure function invoked by ARCH-08
post-permit. Four properties (all four required; docs/04 amendment):

1. Executes inside ARCH-08's trust domain (its code integrity is kernel
   integrity).
2. Deterministic: identical parent label tuples yield identical output
   labels.
3. Side-effect-free: no I/O, no state, no writes.
4. Invocable only by ARCH-08.

ARCH-08 via ARCH-07 is the single writer of output labels. Input = parent
label tuples; output = most-restrictive combination per the docs/07
propagation rules (high-water mark), unless RC-006 authorized downgrade
applies (separate authority-gated path, never a product of merge
evaluation).

## 3. Interface contract

**MergeRequest** (caller → ARCH-08):

- Candidate parent set: at least two DISTINCT `object_id`s (RT-M5S9-03). A
  request containing a duplicate `object_id` is malformed and refused
  fail-closed (RC-001 path); no self-merge exists.
- Every parent is post-G4 with a validated envelope and FCE-set
  `policy_binding_state`.
- All parents carry the SAME pinned policy-bundle version (see §5).
- Proposed output lifecycle type (from the 11-type model).
- Advisory AI association inputs (confidence, association scores): advisory
  metadata only — never a pass/fail input, never consumed by `covers()`
  (shared constraint 2).

**MergeDecision** (ARCH-08 → caller):

- Disposition ∈ D3 lattice values; reason codes from the closed registry
  RC-001..012 only.
- On permit, an ATOMIC construction sequence: decision → high-water-mark
  label (ARCH-07 call) → object construction (kernel-written
  `parent_object_ids`) → ARCH-09 parent-link records → fusion-decision audit
  record. Failure at any step = no fused object exists; there is no
  partially-constructed output state (fail closed).
- On block: see §6.

Two distinct parents sharing an identical (classification, domain, caveat)
tuple T are a legal request; they merge iff the multiset [T, T] is explicitly
enumerated in a permitted combination (§4; RT-M5S9-03 resolved by
RT-M5S9-01 semantics). Legitimate same-sensor temporal fusion is expressible;
accidental authorization is impossible.

## 4. Explicit-permit check

Per the docs/07 MERGE-PERMIT schema (RU-M5-04): a request is covered iff its
parent-tuple multiset EXACTLY matches one enumerated entry in
`permitted_combinations` in the active bundle. Explicit enumeration only —
no wildcards, no patterns, no cardinality shortcuts at TRL 1-3
(RT-M5S9-01: per-tuple membership semantics rejected; a permit enumerating
[T1, T2] does not cover [T1, T1] or [T2, T2]). `max_parents` does not exist:
each combination fixes its own cardinality (architect disposition
2026-07-06).

Absent a covering combination: block, segregate (§6), RC-003, audit.
RC-003 is override-immune (B2, docs/07 registry): no operator authority,
reason code, or PIP attribute can create a permit or relax the block.

Trace: FCE-REQ-KRN-011, FCE-REQ-KRN-010.

## 5. Cross-object bundle-version rule (H8 narrowing)

The kernel requires all parents in a MergeRequest to carry the same pinned
bundle version. A mixed-version request is an ambiguous condition — which
law governs is undecidable — and quarantines with RC-005 and human review
(FCE-REQ-POL-012 path; NOT a block), with detection flag
`mixed_bundle_versions` recorded in the quarantine-class record's
`event_detail.detection_flags` (optional field added by the M5 Sprint 10 docs/08
amendment). Correction 2026-07-06 (lead concurrence, no new DR): the flag lives on
the quarantine-class record's `detection_flags`, not on a fabricated
policy-decision record; the same routing applies to the §1 `unrecorded_parentage`
cross-check flag.

ENGINEERING JUDGMENT: same-version-only is a deterministic TRL 1-3
narrowing, not a resolution of H8. H8 (general cross-object bundle-version
resolution) remains OPEN for TRL 4-5.

## 6. Segregation semantics

Segregation is a disposition, not a transformation: no derived object
exists and no label propagates (docs/07 amendment sentence, RU-M5-04).

- On block: inputs remain individually valid under their own labels for
  non-merge processing.
- The blocked parent set is recorded in provenance as a segregation event.
- Re-association bar: the same set is barred from re-association for the run
  unless a later bundle version supplies a covering combination;
  re-evaluation is a new MergeRequest with a new audit record. The bar is
  DEFENSE-IN-DEPTH ONLY (RT-M5S9-02): it is not a control. Every
  re-requested set — superset, subset, or recomposition — faces the full
  §4 permit check; evasion of the bar gains nothing against deny-by-default.
- Audit: fusion-decision record with `source_object_ids` = full parent set,
  `output_object_id` = null, RC-003, disposition segregate (docs/08 matrix).

## 7. Audit binding

Every MergeDecision emits exactly one fusion-decision audit record per the
docs/08 requiredness matrix (≥2 sources; output required iff permitted;
required semver; ≥1 rule ID). Emission failure halts the pipeline per G7
fail-closed (audit loss is a fail-closed trigger). Quarantine outcomes
(§1 cross-check, §5 mixed-version) emit quarantine-class records per the
matrix.

## 8. Test vectors (Sprint 10 targets, EVD-M5)

| Vector | Behaviour | Trace | Test/Evidence |
|---|---|---|---|
| V1 | Permitted same-domain merge, 2 parents → fused object, HWM label, kernel-written parentage | FCE-REQ-KRN-011, FCE-REQ-PRV-002 | TST-PRP-051 / EVD-M5 |
| V2 | Blocked cross-domain merge, no covering combination → RC-003, segregate, null output | FCE-REQ-KRN-011 | TST-RED-051 / EVD-M5 |
| V3 | Caller-supplied/self-declared parentage (forward cross-check) → quarantine, `unrecorded_parentage` | FCE-REQ-KRN-012 | TST-RED-052 / EVD-M5 |
| V4 | Derived-type object with empty parents → refused (G2 field 13 backstop + kernel assert) | FCE-REQ-KRN-012 | TST-PRP-052 / EVD-M5 |
| V5 | Mixed pinned bundle versions → quarantine, RC-005, review queue, `mixed_bundle_versions` flag | FCE-REQ-POL-012, FCE-REQ-POL-001 | TST-PRP-012 ext / EVD-M5 |
| V6 | Override attempt against V2's RC-003 block → rejected (override_immutable, B2) | FCE-REQ-OPS-002 | TST-RED-002 ext / EVD-M5 |
| V7 | ARCH-09-known derivation output presenting as non-derived (reverse cross-check) → quarantine, `unrecorded_parentage` | FCE-REQ-KRN-012 | TST-RED-052 / EVD-M5 |

## 9. Sprint 10 test hooks (red-team dispositions, 2026-07-06)

- RT-M5S9-01 hook: a bundle combination [T1, T2] does NOT cover [T1, T1] or
  [T2, T2] → TST-POL-002 extension.
- RT-M5S9-02 hook: superset re-request after segregation still denied absent
  a covering combination.
- RT-M5S9-03 hooks: duplicate `object_id` in a MergeRequest → refuse
  fail-closed; [T, T] permitted only when explicitly enumerated.
- RT-M5S9-05 hooks: override attempts against RC-005 quarantine and against
  `unrecorded_parentage` quarantine → both rejected (fixture
  `permitted_envelope` excludes quarantine; envelope check per
  RULE-POL-005).

## Requirement trace

FCE-REQ-KRN-011, FCE-REQ-KRN-012 (RTM v0.5), FCE-REQ-KRN-010,
FCE-REQ-KRN-001, FCE-REQ-POL-001, FCE-REQ-POL-012, FCE-REQ-PRV-002,
FCE-REQ-AUD-001, FCE-REQ-OPS-002, FCE-REQ-SEC-001.

## Facts / Assumptions / Judgment / Uncertainty

- Facts: RULE-POL-002 semantics and the formal invariant (docs/07 v1); D3
  lattice; closed reason-code registry; docs/08 fusion-decision and
  quarantine matrix rows; schema field 13 constraints; M5-01
  detection_flags requiredness (715daee).
- Assumptions: M3 bundle/PIP fixture layout is extensible to
  `permitted_combinations` without evaluator rework (Sprint 10 verifies);
  the 11-type lifecycle model is stable through M5.
- Judgment: bidirectional cross-check placement at G5 entry; atomic
  construction sequence; same-version narrowing with RC-005; segregation
  set-bar as defense-in-depth; duplicate-id disposition via RC-001 path;
  V1–V7 selection.
- Uncertainty: combination-enumeration scale at M6 scenario richness (DR if
  it breaks); G5-entry cross-check cost (TARGET only, M8); H4/H6/H7/H8 all
  open and disclosed, unclaimed.
