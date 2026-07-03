# Sahtune Fusion Compliance Engine (FCE) — Architecture Package (Phase B/C)

**Status:** Design artifacts only. No implementation code. No external tools installed.
**Prepared by:** Acting as `fce-lead-systems-architect`, applying the 13 FCE skills as the operating structure, gated by `red-team-reviewer` and `security-assurance-engineer`.
**Date:** 2026-07-02.

The **Fusion Compliance Engine (FCE)** is a capability inside Sahtune Fusion. It is **not** a standalone product. See `01_executive-technical-concept.md`.

---

## How to read this package
Every claim in every file carries a trace ID or one of these labels (per `fce-documentation-style`):

| Label | Meaning |
|---|---|
| FACT (cited) | Verifiable, with a primary-source citation |
| ASSUMPTION | Working assumption, not yet confirmed |
| ENGINEERING JUDGMENT | Design opinion of the architect |
| UNCERTAINTY | Known unknown, flagged for resolution |
| TARGET | Kanatir internal measured target — to be verified on named hardware |
| MEASURED | Carries measurement provenance (none exist yet in this package) |
| VENDOR CLAIM (unverified) | Third-party statement, unverified by Kanatir benchmark |

**Prohibited vocabulary** (absent by design): certified, accredited, "compliant with <standard>", endorsed, operationally deployed, approved for classified. Standards appear only as *"designed with reference alignment to …"*.

---

## Files (one per architecture block)
| # | File | Owning skill / agent |
|---|---|---|
| 00 | `00_project-context.md` | fce-documentation-style, requirements-traceability |
| 01 | `01_executive-technical-concept.md` | fce-lead-systems-architect, product-positioning |
| 02 | `02_capability-decomposition.md` | requirements-traceability |
| 03 | `03_rtm.md` | requirements-traceability |
| 04 | `04_software-architecture-and-trust-boundaries.md` | lead-architect, secure-architecture-review |
| 05 | `05_seven-gate-data-flow.md` | lead-architect, sensor-fusion, secure-architecture-review |
| 06 | `06_metadata-schema.md` | data-model-engineer |
| 07 | `07_policy-decision-model.md` | policy-engineer / fce-policy-as-code |
| 08 | `08_audit-record-schema.md` | audit-forensics-engineer / fce-audit-record-design |
| 09 | `09_synthetic-dataset-plan.md` | sensor-fusion / fce-synthetic-sensor-data |
| 10 | `10_security-threat-model.md` | security-assurance, red-team / fce-threat-model |
| 11 | `11_failure-modes-and-mitigations.md` | test-evaluation, security-assurance |
| 12 | `12_trl-roadmap.md` | trl-evidence-engineer |
| 13 | `13_nvidia-vision-acceleration-evaluation.md` | fce-vision-acceleration-evaluation |
| 14 | `14_execution-architecture-m1-m9.md` | fce-lead-systems-architect |
| 15 | `15_trl1-3-build-plan.md` | fce-lead-systems-architect, trl-evidence-engineer |
| 97 | `97_b1-b3-closure-review.md` | red-team-reviewer, security-assurance-engineer |
| 98 | `98_live-gate-review.md` | red-team-reviewer, security-assurance-engineer |
| — | `99_gate-review.md` | red-team-reviewer, security-assurance-engineer |

### Claude Desktop handoff (`docs/handoff/`)
Prepared to continue the project sprint-by-sprint in Claude Desktop while keeping
Claude Code + GitHub as the source of truth. Files: `00_handoff-index.md`,
`01_architecture-completion-summary.md`,
`02_claude-desktop-operating-instructions.md`,
`03_sprint-by-sprint-desktop-prompts.md`, `04_traceability-map.md`,
`05_open-items-and-decision-register.md`, `06_desktop-session-rules.md`,
`07_next-action-checklist.md`.

> Layout note: the user requested one file per architecture block, so this package is flat and block-numbered. The canonical `fce-evidence-pack` folder taxonomy (`evidence/trl_*`, `docs/01_requirements/`, `docs/05_data_model/`, `docs/11_risk_register/`, `docs/12_decision_records/`) remains the future home for these artifacts; cross-references note the mapping.

---

## Pre-generation verification (requested)

| # | Check | Result |
|---|---|---|
| 1 | All 14 FCE agents visible | **PASS** — 14 agent files under `.claude/agents/` (excluding `_SHARED_CONSTRAINTS.md`, a shared reference file). Listed in `00_project-context.md`. |
| 2 | All 13 FCE skills visible | **PASS** — 13 skill directories under `.claude/skills/`. Listed in `00_project-context.md`. |
| 3 | FCE-DES-01 … FCE-DES-04 in the RTM | **PASS BY CONSTRUCTION, WITH CAVEAT** — no RTM existed on disk before this package (no `docs/` tree present). The RTM in `03_rtm.md` is newly created and explicitly includes all 10 outcomes: FCE-ESS-01…06 and FCE-DES-01…04 (DES-01 and DES-03 called out per skill requirement). **Caveat:** outcome wording uses the user-supplied **paraphrased anchors** (recorded in `02`), which are explicitly **not** verbatim DND text and have **not** been fabricated. Replace with the quoted solicitation source to finalize. |
| 4 | NVIDIA vision acceleration remains optional evaluation only | **PASS** — treated strictly as an optional evaluation/benchmark track, never a core dependency and never in the compliance-decision path. See `13_nvidia-vision-acceleration-evaluation.md` and the trust-boundary in `04`. |

### Top open input (blocking for RTM finalization only)
**The verbatim DND IDEaS solicitation text is not in the repository.** Design currently uses the user-supplied paraphrased anchors (see `02`). Per `fce-requirements-traceability`, final RTM outcome cells must quote the solicitation, not a paraphrase. Paste the solicitation (ideally into `docs/00_project_context/solicitation/`) to finalize the RTM outcome cells and compliance matrix without changing the architecture.

---

## Epistemic summary for the whole package
- **Facts:** the agent/skill inventory, the skill-mandated schema shapes (15 metadata fields, 18 audit fields, 9 audit event classes, 11 policy actions, 8 threat areas, 7 gates), and the governance constraints are drawn directly from the installed library files.
- **Assumptions:** the thematic content of each DND outcome, until the solicitation text is supplied; the target hardware class (Jetson-class edge) pending confirmation.
- **Engineering judgment:** the specific decomposition into 12 capabilities, 14 architecture elements, and the ordering of the 7 gates.
- **Uncertainty:** exact outcome wording; final classification taxonomy; hardware SKUs for benchmarking.
- **No** certification, ATO, endorsement, classified-processing, or performance claims appear anywhere in this package.
