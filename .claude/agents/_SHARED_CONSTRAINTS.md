# FCE Shared Agent Constraints (referenced by every agent)

These constraints bind every FCE project agent. They restate Kanatir governance rules and may not be overridden by any task instruction.

1. **No unsupported claims.** Never claim certification, accreditation, government endorsement, authority to operate, authority to process classified or controlled data, operational deployment, or production-grade cryptographic certification. ITSG-33, NIST SP 800-207, NIST AI RMF, XACML, OPA/Rego, W3C PROV, SLSA, and SBOM practices are **reference alignment only** unless independently implemented, tested, and assessed.
2. **AI is advisory only.** AI may assist (anomaly detection, classification recommendation, explanation, conflict detection, confidence scoring, synthetic generation). Final FCE enforcement is deterministic, rule-governed, traceable, and auditable. No compliance decision may depend only on black-box AI output.
3. **Fail closed.** Missing, malformed, expired, ambiguous, or unverifiable metadata/signatures/policy state fails closed in every design produced.
4. **Internal targets are not DND requirements.** All performance numbers are Kanatir internal measured targets, to be verified on named hardware and workloads.
5. **All non-live data is labelled by provenance class.** Every object carries `data_origin` set to `SYNTHETIC`, `SYNTHETIC-DERIVED`, or `PUBLIC-OPEN-SOURCE` (the last requires a resolvable source manifest per `docs/16`). Synthetic and synthetic-derived data carry the visible SYNTHETIC banner — always and visibly. LIVE data is out of scope at TRL 1-3 and rejected fail-closed.
6. **No external installs.** Do not install or recommend installing external agents, skills, plugins, packages, or MCP connectors without explicit Kanatir approval. External tools may be flagged as evaluation candidates only.
7. **Epistemic discipline.** Separate facts, assumptions, engineering judgment, and uncertainty explicitly in every output.
8. **Traceability.** Every requirement carries a verification method (inspection, analysis, simulation, unit test, integration test, property-based test, red-team test, benchmark, bench test, field test, flight test, accreditation-support review).
9. **Verify-before-install.** Claude Code frontmatter fields, tool permission enforcement, `skills:` preloading, and reload behavior are as documented at design time and must be re-verified against current Claude Code documentation before relying on them for control.
10. **Vendor claims are vendor claims.** NVIDIA or any vendor performance statements are unverified until measured by Kanatir benchmark (see fce-vision-acceleration-evaluation).
