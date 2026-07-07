# FCE-DR-SCH-005 — data_origin propagation through kernel construction

Status: RATIFIED 2026-07-07 (M6 Sprint 11 close). Review chain recorded below.
Owner: `data-model-engineer` with `policy-engineer`.

## Decision

For every object constructed by the Fusion Compliance Kernel (ARCH-08) —
fused, derived, transformed, downgraded — the `data_origin` field (schema
v0.2.0 field 3) is set by the kernel at construction per these rules,
evaluated over the actual evaluated parent set:

1. If ANY parent carries `data_origin` SYNTHETIC or SYNTHETIC-DERIVED, and at
   least one parent carries PUBLIC-OPEN-SOURCE, the output is
   SYNTHETIC-DERIVED. The visible SYNTHETIC banner follows structurally.
2. If ALL parents carry SYNTHETIC, the output is SYNTHETIC.
   SYNTHETIC-DERIVED is reserved for public-lineage mutation/mixing or
   synthetic overlays derived from public inputs (lead ruling 2026-07-07).
3. If ALL parents carry PUBLIC-OPEN-SOURCE, the output is PUBLIC-OPEN-SOURCE
   if and only if transitive manifest resolvability holds: the output's
   `provenance_ref` resolves to parents whose source-manifest references
   resolve (GDR-001 satisfied transitively). Otherwise fail closed.
4. Check timing (RT-M6S11-03 disposition): transitive resolvability is
   verified at construction time as a minimum, AND re-verified fail-closed at
   any G2 re-entry of the constructed object. A constructed all-public object
   whose parent manifest entry is no longer resolvable fails closed on
   re-entry.
5. Write authority: `data_origin` on kernel-constructed objects is written
   ONLY by ARCH-08 at construction — never accepted from a caller, an
   adapter, or the object itself (same authority pattern as parentage,
   C2/C3, docs/18 §1). The field is not a self-declaration surface.

Segregation produces no derived object; no propagation occurs on block
(docs/07 segregation sentence, unchanged).

## Scope and non-scope

Documentation-level propagation rule on an existing field: no envelope change,
no new field, no schema version bump. Fixture construction (Sprint 12), banner
behaviour, and GDR-001's reach over constructed objects are bound by this DR.
LIVE remains out of scope at TRL 1-3 (FCE-DR-SCH-002, RC-010).

## Test hooks

- All-public permitted merge → output PUBLIC-OPEN-SOURCE with resolvable
  transitive manifest (positive).
- Mixed public+synthetic permitted merge → output SYNTHETIC-DERIVED, banner
  visible (positive).
- All-synthetic permitted merge → output SYNTHETIC (positive).
- Fused all-public object, parent manifest entry removed → fail closed at G2
  re-entry (RT-M6S11-03 hook).
- Caller-supplied data_origin on a construction request → ignored;
  kernel-written value governs (authority hook).

## Ratification record

Proposed: data-model-engineer (Sprint 11 review, amendment A3). Endorsed:
policy-engineer (Sprint 11, incl. transitive-resolvability condition and
kernel-write authority). Conditioned: red-team-reviewer RT-M6S11-03 (check
timing), dispositioned by lead 2026-07-07. All-SYNTHETIC case ruled by lead
2026-07-07. Lead concurrence recorded 2026-07-07. Binding before any Sprint 12
fixture build.

## Trace

FCE-REQ-PRV-001, FCE-REQ-PRV-002, FCE-REQ-MET-010, FCE-REQ-KRN-012.
