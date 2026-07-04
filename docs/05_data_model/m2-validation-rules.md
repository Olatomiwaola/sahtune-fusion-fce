# M2 Sprint 3 — Schema Validation Rules v0.2.0

Repo home (proposed, ENGINEERING JUDGMENT): `docs/05_data_model/m2-validation-rules.md`.
Owner: `data-model-engineer`. One rule per mandatory field/constraint of
`docs/06_metadata-schema.md` v0.2.0; every rule traces to a requirement ID and a planned
test ID. Rule IDs RULE-VAL-001..018 are minted in Sprint 3 under the RULE-* scheme
(fce-documentation-style). Test IDs LAP-UNIT-001..005 are pre-existing (`docs/16`);
LAP-UNIT-006..009 are minted in Sprint 3 in the PoC file plan.

| Rule ID | Rule (full text) | REQ trace | Planned test |
|---|---|---|---|
| RULE-VAL-001 | object_id present, valid uuid. Duplicate-ID handling pending uniqueness-scope decision (freeze record, field 1); presence/format enforced now. | FCE-REQ-MET-010, FCE-REQ-PRV-001 | LAP-UNIT-001, LAP-UNIT-002, LAP-UNIT-007 |
| RULE-VAL-002 | schema_version present, valid semver, and a supported version; unsupported version rejected by the envelope-version gate before policy. | FCE-REQ-MET-010 | LAP-UNIT-004 |
| RULE-VAL-003 | data_origin present and in {SYNTHETIC, SYNTHETIC-DERIVED, PUBLIC-OPEN-SOURCE}; any other value, including LIVE, rejected fail-closed at G1. | FCE-REQ-MET-010, FCE-REQ-ING-010 | LAP-UNIT-006 |
| RULE-VAL-004 | If data_origin = PUBLIC-OPEN-SOURCE, a resolvable source-manifest reference must be present (GDR-001 hook; full manifest verification is M6 scope — at M2 the reference field's presence is enforced). | FCE-REQ-MET-010, FCE-REQ-PRV-001 | LAP-UNIT-008 |
| RULE-VAL-005 | If data_origin in {SYNTHETIC, SYNTHETIC-DERIVED}, the visible SYNTHETIC banner flag is set on the disposition output (banner rendering is presentation scope; the flag is validator output). | Shared constraint 5; FCE-REQ-MET-010 | LAP-UNIT-001 |
| RULE-VAL-006 | source_sensor_id present, non-empty string (authentication of the sensor identity is G1/PIP scope — RC-008 path, not this rule). | FCE-REQ-MET-010, FCE-REQ-PRV-001 | LAP-UNIT-002, LAP-UNIT-007 |
| RULE-VAL-007 | modality present and within the taxonomy-fixture enum; unknown value fails closed. | FCE-REQ-MET-010, FCE-REQ-ING-010 | LAP-UNIT-007 |
| RULE-VAL-008 | acquisition_timestamp present, valid RFC3339, with clock_source present and non-empty. | FCE-REQ-MET-010, FCE-REQ-PRV-001 | LAP-UNIT-002, LAP-UNIT-007 |
| RULE-VAL-009 | ingest_timestamp present, valid RFC3339. | FCE-REQ-MET-010, FCE-REQ-PRV-001 | LAP-UNIT-007 |
| RULE-VAL-010 | classification_label present and within the project-taxonomy fixture enum; unknown value fails closed; no real Government of Canada marking accepted or rendered. | FCE-REQ-MET-010, FCE-REQ-POL-011 | LAP-UNIT-002, LAP-UNIT-007 |
| RULE-VAL-011 | domain_label present and within the project-taxonomy fixture enum; unknown value fails closed. | FCE-REQ-MET-010, FCE-REQ-POL-011 | LAP-UNIT-007 |
| RULE-VAL-012 | release_caveat present as a list; empty list permitted; null fails closed; every member within the taxonomy fixture. | FCE-REQ-MET-010 | LAP-UNIT-009 |
| RULE-VAL-013 | handling_instructions present, non-empty string. | FCE-REQ-MET-010 | LAP-UNIT-002 |
| RULE-VAL-014 | provenance_ref present, non-empty, uri/graph-node-id shape (resolvability is M4 provenance-graph scope). | FCE-REQ-MET-010, FCE-REQ-PRV-001 | LAP-UNIT-002, LAP-UNIT-007 |
| RULE-VAL-015 | parent_object_ids present as a list of valid uuids; null fails closed; must be non-empty for derived/merged lifecycle types and empty otherwise (lifecycle type per fixture declaration at M2). | FCE-REQ-MET-010, FCE-REQ-PRV-002 | LAP-UNIT-007, LAP-UNIT-009 |
| RULE-VAL-016 | integrity_hash present, sha-256 format. Hash VERIFICATION explicitly deferred pending hash-input-domain definition (freeze record, field 14); format check only at Sprint 4, deferral labelled in test output. | FCE-REQ-MET-010 | LAP-UNIT-007 |
| RULE-VAL-017 | policy_binding_state is FCE-authority-set: forced to `unvalidated` at G1 regardless of any ingested value; ingested value never trusted; a source-supplied value is recorded as detected in the disposition output. | FCE-REQ-MET-010; B3 (`docs/97`); GDR-007 | LAP-UNIT-003 |
| RULE-VAL-018 | Disposition determinism: identical envelope input yields identical disposition, reason code, and detection flags on repeated evaluation. | FCE-REQ-POL-001 (validation layer) | LAP-UNIT-001, LAP-UNIT-007 (repeat-evaluation assertions; full determinism suite is LAP-UNIT-005 at M3) |

Failure disposition for RULE-VAL-001 and RULE-VAL-004..016: quarantine at G2 with
RC-001 per the freeze record's G2 specification. RULE-VAL-002 (unsupported version) and
RULE-VAL-003 (LIVE/unknown origin) reject before policy at the G1/version-gate boundary.
RULE-VAL-017 is a forcing rule, not a rejection rule.

Gap flagged: unknown/extra envelope fields — accept-and-ignore vs reject is not defined
in `docs/06` and is not decided here (raised to red-team review and the architect;
interim Sprint 4 behaviour must be an explicit, tested choice, default fail-closed).

## Facts / Assumptions / Judgment / Uncertainty

- FACT: every rule restates a constraint present in `docs/06` v0.2.0, `docs/97` (B3),
  or `docs/16` (GDR-001/006/007); no new constraint semantics invented.
- ASSUMPTION: taxonomy enum fixtures populated from `docs/07` at Sprint 4 without change.
- ENGINEERING JUDGMENT: rule granularity and test-ID mapping.
- UNCERTAINTY: unknown-field handling; integrity-hash verification pending input-domain
  definition; object_id uniqueness scope.
