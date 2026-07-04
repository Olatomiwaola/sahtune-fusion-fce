# RT-M2S3 — Red-Team Findings, M2 Sprint 3 (Schema Freeze v0.2.0)

Owner: `red-team-reviewer`. Raised 2026-07-03 (chat) against the M2 Sprint 3 freeze
package: `docs/05_data_model/m2-schema-freeze-record.md`,
`docs/05_data_model/m2-validation-rules.md`, `docs/05_data_model/m2-poc-file-plan.md`,
and decision records `docs/12_decision_records/fce-dr-sch-001.md` /
`fce-dr-sch-002.md`. Basis commit 5dd2a10.

Originally all five findings were **OPEN and NON-BLOCKING** for the v0.2.0 freeze: each a
scope or definition gap already acknowledged in the freeze record, not a defect in the
frozen 15-field shape. **Update (M2 Sprint 4, 2026-07-04, basis ca75497): RT-M2S3-03 and
RT-M2S3-04 are RESOLVED** (see per-finding notes); the remaining three stay open and
non-blocking. Tracked in `docs/handoff/05_open-items-and-decision-register.md`.

| Finding | Title | Severity | Status | Disposition target |
|---|---|---|---|---|
| RT-M2S3-01 | object_id uniqueness scope undefined | Medium | Open | data-model-engineer, before Sprint 4 assertions (FU-M2S3-3) |
| RT-M2S3-02 | integrity_hash format-only deferral | Medium | Open | data-model-engineer, input domain due M4 (FU-M2S3-1) |
| RT-M2S3-03 | unknown/extra-field handling undefined | Medium | **RESOLVED** (FCE-DR-SCH-003; LAP-UNIT-010) | closed FU-M2S3-2 |
| RT-M2S3-04 | taxonomy fixture provenance | Low | **RESOLVED** (hash + docs/09+docs/06 provenance; FU-M2S4-1 for docs/07 registry) | EVD-M2 |
| RT-M2S3-05 | volatile pre-marking / source-supplied binding-state flag | Low | Open | data-model-engineer / policy-engineer |

## RT-M2S3-01 — object_id uniqueness scope undefined

**Finding.** Field 1 (`object_id`) is frozen as `uuid; unique; required`, but `docs/06`
does not define the scope of "unique" — global, per-run, or per-mission — and
duplicate-ID handling is unspecified. RULE-VAL-001 enforces presence and format only.
An attacker (or a faulty adapter) presenting a duplicate `object_id` could collide a new
object with an existing lineage node, corrupting provenance association without tripping
any frozen rule.

**Evidence.** Freeze record field 1 (UNCERTAINTY flagged); RULE-VAL-001 note
("Duplicate-ID handling pending uniqueness-scope decision").

**Recommendation.** Define the uniqueness scope and the duplicate-ID disposition
(reject vs quarantine) before Sprint 4 test assertions are finalized. Until then the PoC
must not claim uniqueness enforcement.

**Trace.** FCE-REQ-MET-010, FCE-REQ-PRV-001. Owner: data-model-engineer.

## RT-M2S3-02 — integrity_hash verification deferred (format-only)

**Finding.** Field 14 (`integrity_hash`) is frozen as `sha-256 (design); required`, but
`docs/06` does not define the hash input domain (which bytes/fields are hashed,
canonicalization). RULE-VAL-016 checks format only; the G2 "integrity check failure"
disposition is therefore UNTESTABLE at Sprint 4. A tampered object whose hash is
well-formed but does not cover the mutated fields would pass the format check and enter
the gate path.

**Evidence.** Freeze record field 14 (material UNCERTAINTY); G2 fail-closed spec
("UNTESTABLE at Sprint 4 pending hash-input-domain definition"); RULE-VAL-016.

**Recommendation.** Define the hash input domain and canonicalization; this is a
follow-up owned by data-model-engineer, due M4 (when the provenance/audit carriage is
specified). Sprint 4 output must label hash verification EXPLICITLY DEFERRED.

**Trace.** FCE-REQ-MET-010. Owner: data-model-engineer (due M4).

## RT-M2S3-03 — unknown / extra envelope field handling undefined

**Finding.** Neither `docs/06` nor the validation-rule list defines whether an envelope
carrying unknown or extra fields is accepted-and-ignored or rejected. An accept-and-ignore
default is a classic smuggling channel: unmodelled fields could carry data downstream
consumers misread, or mask a version mismatch. The gap is explicitly flagged but not
decided in the freeze package.

**Evidence.** RULE-VAL list gap note ("unknown/extra envelope fields — accept-and-ignore
vs reject is not defined … default fail-closed"); PoC file plan UNCERTAINTY
("unknown-field handling decision must be made before test_validator.py is finalized").

**Recommendation.** Make the disposition an explicit, tested choice before Sprint 4
tests are written; interim default fail-closed. Owner: architect, before Sprint 4 tests.

**Resolution (M2 Sprint 4).** RESOLVED by **FCE-DR-SCH-003**: unknown/extra envelope
fields reject fail-closed at G2 with RC-001. Verified by **LAP-UNIT-010**
(`tests/test_validator.py::test_lap_unit_010_unknown_field_rejected`). Follow-up
FU-M2S3-2 is closed. Revisit trigger recorded in the decision record (first external
adapter or TRL 4-5).

**Trace.** FCE-REQ-MET-010. Owner: architect.

## RT-M2S3-04 — taxonomy fixture provenance

**Finding.** Fields 8 (`classification_label`), 9 (`domain_label`), and members of 10/12
validate against a taxonomy loaded as a fixture, because `docs/07` was not supplied to
the freeze chat. The fixture's provenance is therefore uncontrolled at freeze time: a
fixture that diverges from the authoritative `docs/07` taxonomy would let the PoC accept
values the real policy model rejects (or vice versa), and there is no guard binding the
fixture to `docs/07`.

**Evidence.** Freeze record fields 8/9 ("taxonomy enum values sourced from `docs/07` at
Sprint 4 … docs/07 not supplied to this chat — gap flagged; PoC loads values as a
fixture, fail-closed on unknown values"); RULE-VAL-007/010/011 ("taxonomy-fixture
enum").

**Recommendation.** At Sprint 4, populate the taxonomy fixture directly from `docs/07`
and record its provenance in EVD-M2; add a consistency check that the fixture equals the
`docs/07` value families. Fail-closed-on-unknown is the correct interim posture.

**Resolution (M2 Sprint 4).** RESOLVED by hash + provenance. `docs/07` was found to carry
the project-taxonomy **disclaimer only** — it enumerates no values (no registry yet), so
the fixture was populated from the **docs/09 + docs/06 enumerations** (values: PROJ-LEVEL-1..3,
DOMAIN-A/DOMAIN-B, modalities from docs/09; release_caveat PROJ-CAVEAT-X from docs/06;
lower_snake token form per the docs/06 example). The fixture is hash-pinned in EVD-M2
(sha-256 `59979c4d…bec240`), and unknown values fail closed. Authoring the enumerated
registry in `docs/07` (with a fixture-equality guard) is carried forward as **FU-M2S4-1**
(owner policy-engineer, due M3 Sprint 5, consumes OPEN-02 / leadership decision #2).

**Trace.** FCE-REQ-MET-010, FCE-REQ-POL-011. Owner: data-model-engineer (Sprint 4).

## RT-M2S3-05 — volatile pre-marking / source-supplied binding-state flag

**Finding.** Field 15 (`policy_binding_state`) is FCE-authority-set and forced to
`unvalidated` at G1 (B3, GDR-007); a source-supplied value is not rejected but is
recorded as detected in the disposition output (RULE-VAL-017). The detection flag is the
only signal that an upstream component attempted to pre-mark an object's binding state.
Because the flag is disposition-output only and audit emission is deferred to M4, a
source pre-marking attempt at TRL 1-3 leaves no durable, tamper-evident record — the
signal is volatile and could be dropped without trace before the M4 audit writer exists.

**Evidence.** Freeze record field 15 and G2 spec (source-supplied binding state:
"detection recorded in disposition output … formal audit emission is M4 scope");
RULE-VAL-017; FCE-DR-SCH-001 (`policy_binding_state` is the only policy-adjacent
envelope field).

**Recommendation.** Confirm the detection flag is asserted and tested at Sprint 4
(LAP-UNIT-003) and explicitly note the no-durable-audit limitation until M4; ensure the
M4 audit schema logs pre-marking-detection events (relates to H14). Non-blocking at
TRL 1-3.

**Trace.** FCE-REQ-MET-010; B3 (`docs/97`); GDR-007; THR-MET-003. Owner:
data-model-engineer / policy-engineer.

## Facts / Assumptions / Judgment / Uncertainty

- FACT: all five findings restate gaps already flagged in the Sprint 3 freeze package;
  none contradicts the frozen 15-field shape.
- ENGINEERING JUDGMENT: severities and disposition targets assigned by the red-team
  review; all rated non-blocking for the v0.2.0 freeze.
- UNCERTAINTY: RT-M2S3-01/02/03 must be resolved before their Sprint 4 test assertions
  are final; closure is verified at H9/M7.
