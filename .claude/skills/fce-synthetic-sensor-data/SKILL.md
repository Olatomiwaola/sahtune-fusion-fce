---
name: fce-synthetic-sensor-data
description: Creates synthetic mission scenarios and dataset specifications — EO/IR, radar-like tracks, acoustic-like events, SIGINT-like metadata, maritime AIS-like tracks, UAS telemetry — with all data clearly labelled synthetic. Use for any scenario design, dataset planning, test data specification, or mission replay data work.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Synthetic Sensor Data

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`. DND will not provide data — synthetic-first is a program requirement, and synthetic data precedes any live data.

## Purpose
Specify synthetic mission scenarios and datasets that exercise every FCE gate, policy action, and failure mode — every object visibly labelled SYNTHETIC.

## Trigger conditions
Scenario design; dataset specs; test-data needs; replay data; red-team data (tampered/malformed variants); modality coverage planning.

## Procedure
1. Scenarios use `templates/scenario-spec.md`. The four baseline scenarios: **Joint ISR Fusion** (EO/IR detections, radar-like tracks, SIGINT-like metadata, classification/domain conflicts); **Maritime Domain Awareness** (radar-like, AIS-like, EO/IR, anomaly events); **Tactical Edge Dismounted** (wearable events, UAS telemetry, EO/IR detections, degraded network); **UAV Mission Support** (EO/IR payload observations, platform telemetry, target-track estimates, operator requests, mission replay).
2. Each scenario defines: sensor modalities, object schema (data-model-engineer's schema), classification labels (project taxonomy — never real GoC markings), domain labels, deliberate policy conflicts, expected enforcement decisions, expected audit records, success criteria, failure cases, red-team cases.
3. Labelling: every object carries `data_origin: SYNTHETIC` plus a visible banner in any rendered artifact. Non-negotiable.
4. "-like" discipline: radar-like, AIS-like, SIGINT-like — plausible structure for pipeline exercise, never claimed as emulation of real systems.
5. Coverage targets (internal): minimum 2 modalities (EO/IR + radar-like) → stretch EO/IR + radar-like + acoustic-like + SIGINT-like + UAS telemetry.
6. Specification only until dataset generation is approved.

## Required reference files
Metadata schema, policy action list, scenario library (data/synthetic/scenarios/).

## Optional supporting scripts
None at Phase A. (Future: generators under scripts/generate_synthetic_data/ — requires approval.)

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash (until generation approved), WebSearch, WebFetch, MCP connectors.

## Example usage
"Spec the Maritime scenario conflicts" → 3 conflict cases (domain mismatch, caveat violation, ambiguous classification) → expected dispositions + audit events → red-team variants.

## Validation checklist
- [ ] All scenario-spec fields complete.
- [ ] SYNTHETIC labelling specified at object + artifact level.
- [ ] "-like" phrasing; no real-system emulation claims; project taxonomy only.
- [ ] Every gate + policy action exercised somewhere in the scenario set.
- [ ] Expected audit records enumerated.
- [ ] Red-team variants included.

## Output template
Use `templates/scenario-spec.md`.

## Failure conditions (stop and escalate)
- Request for realistic classified structure or real GoC markings → refuse; project taxonomy; flag.
- Request to generate actual datasets pre-approval → spec only; note pending approval.
