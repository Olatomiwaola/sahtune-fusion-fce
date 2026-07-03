# 00 — Project Context, Inventory, and Glossary

Governed by `.claude/agents/_SHARED_CONSTRAINTS.md` and `fce-documentation-style`.

## Installed library inventory (verification detail)

### 14 FCE agents (FACT — from `.claude/agents/`)
1. fce-lead-systems-architect
2. requirements-traceability-engineer
3. data-model-engineer
4. policy-engineer
5. audit-forensics-engineer
6. sensor-fusion-engineer
7. edge-performance-engineer
8. security-assurance-engineer
9. red-team-reviewer
10. test-evaluation-engineer
11. trl-evidence-engineer
12. devsecops-engineer
13. proposal-compliance-writer
14. product-strategy-reviewer

`_SHARED_CONSTRAINTS.md` is a shared reference file bound into every agent, not a 15th agent.

### 13 FCE skills (FACT — from `.claude/skills/`)
1. fce-requirements-traceability
2. fce-policy-as-code
3. fce-threat-model
4. fce-secure-architecture-review
5. fce-audit-record-design
6. fce-test-and-evaluation
7. fce-edge-benchmarking
8. fce-evidence-pack
9. fce-synthetic-sensor-data
10. fce-vision-acceleration-evaluation
11. fce-proposal-compliance
12. fce-product-positioning
13. fce-documentation-style

## Operating structure applied (FACT — per `.claude/INSTALL.md`)
`fce-lead-systems-architect` orchestrates. The Requirements Traceability Matrix (RTM), owned by `requirements-traceability-engineer`, anchors everything. Design work fans out to the policy, data-model, audit, fusion, edge, and devsecops engineers, each preloading its matching skill. `security-assurance-engineer` (read-only plus reports) and `red-team-reviewer` (read-only) gate every trust-boundary change and every external-facing claim. `test-evaluation-engineer` and `trl-evidence-engineer` close the requirement-to-evidence loop. `proposal-compliance-writer` and `product-strategy-reviewer` control all outward language. The NVIDIA vision-acceleration track runs only through the `fce-vision-acceleration-evaluation` skill and its decision records.

## Open inputs and blockers
| ID | Item | Impact | Owner |
|---|---|---|---|
| OPEN-01 | DND IDEaS solicitation verbatim outcome text supplied and verified on 2026-07-03 | M1 Sprint 1 unblocked; GATE-A still requires Sprint 2 coverage audit and review | requirements-traceability-engineer |
| OPEN-02 | Classification taxonomy is a project-taxonomy placeholder, never real Government of Canada markings | Policy labels (`07`) use the project taxonomy only | policy-engineer |
| OPEN-03 | Target edge hardware model is unconfirmed (Jetson-class assumed) | Benchmark plans (`13`) remain TARGET-only | edge-performance-engineer |
| OPEN-04 | Laptop PoC data-source approval: choose at least two public source families from `docs/16_laptop-poc-validation-architecture.md` (leadership decision #6) | Required for source manifest, trim report, calibration/held-out fixture seal, and pre-lab validation evidence | test-evaluation-engineer / data-model-engineer |

## Shared identifier vocabulary (the spine used across all files)
- Outcomes: `FCE-ESS-01` through `FCE-ESS-06`, and `FCE-DES-01` through `FCE-DES-04`. Outcome text is verified verbatim Canada.ca challenge text in `02` and `03`.
- Capabilities: `CAP-01` through `CAP-12` (defined in `02`).
- Architecture elements: `ARCH-01` through `ARCH-14` (defined in `04`).
- Gates: `G1` through `G7` (defined in `05`).
- Requirements: `FCE-REQ-<AREA>-<NNN>`, where AREA is one of ING, MET, POL, KRN, PRV, AUD, EXP, SIM, TST, EDG, SEC, OPS.
- Policy rules: `RULE-*`. Reason codes: `RC-*`. Threats: `THR-<area>-*`. Tests: `TST-<class>-*`. Evidence: `EVD-*`. Decision records: `DR-*`.

## Glossary and acronyms (expand-on-first-use register)
| Term | Expansion and meaning |
|---|---|
| FCE | Fusion Compliance Engine — a capability inside Sahtune Fusion |
| PDP / PEP / PAP / PIP | Policy Decision Point / Policy Enforcement Point / Policy Administration Point / Policy Information Point (OASIS XACML reference pattern — reference alignment only) |
| Rego / OPA | Open Policy Agent rule language (openpolicyagent.org — reference pattern only) |
| PROV | W3C provenance data model (reference alignment only) |
| STRIDE | Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege |
| ITSG-33 | Canadian Centre for Cyber Security IT security risk-management guidance (reference alignment only) |
| SP 800-207 | NIST Zero Trust Architecture (reference alignment only) |
| SBOM / SLSA | Software Bill of Materials / Supply-chain Levels for Software Artifacts (reference alignment only) |
| EO/IR | Electro-Optical / Infrared |
| ISR | Intelligence, Surveillance, Reconnaissance |
| AIS | Automatic Identification System (maritime); used only as "AIS-like" synthetic structure |
| SWaP-C | Size, Weight, Power, and Cost |
| TRL | Technology Readiness Level |
| RTM | Requirements Traceability Matrix |
| High-water mark | Most-restrictive-combination labelling rule for merged or derived objects |

## Standing constraints echoed into every file
1. No unsupported claims (certification, accreditation, authority to operate, endorsement, classified processing, production cryptographic certification). Standards are reference alignment only.
2. AI is advisory only; final enforcement is deterministic, rule-governed, and auditable.
3. Fail closed on missing, malformed, expired, ambiguous, or unverifiable inputs.
4. Internal targets are not DND requirements.
5. Synthetic data is always visibly labelled SYNTHETIC.
6. No external installs without Kanatir approval; external tools are evaluation candidates only.
7. Separate facts, assumptions, engineering judgment, uncertainty, and vendor claims.
8. Every requirement carries a verification method.
