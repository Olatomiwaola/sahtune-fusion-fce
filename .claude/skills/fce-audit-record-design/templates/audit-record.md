# Audit record schema v<n> — event class: <class>
| # | Field | Type | Constraint | Example (SYNTHETIC) |
|---|---|---|---|---|
| 1 | audit_event_id | uuid | unique, required | |
| 2 | event_type | enum(9 classes) | required | |
| 3 | timestamp | RFC3339 + clock_source | required | |
| 4 | actor_identity | service/operator ID | authenticated | |
| 5 | source_object_id | uuid | required | |
| 6 | output_object_id | uuid | nullable w/ reason | |
| 7 | policy_bundle_version | semver+hash | required | |
| 8 | policy_rule_ids | list | required | |
| 9 | decision | enum | required | |
| 10 | reason_code | registry ref | required | |
| 11 | enforcement_action | enum(11 actions) | required | |
| 12 | disposition | enum | required | |
| 13 | confidence | float [0,1] | advisory only | |
| 14 | record_hash | sha-256 (design) | required | |
| 15 | previous_audit_hash | sha-256 (design) | chain | |
| 16 | signature | PLACEHOLDER | pending independent impl+assessment | |
| 17 | export_status | enum | required | |
| 18 | review_status | enum | required | |
