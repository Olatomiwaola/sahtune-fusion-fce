---
name: fce-edge-benchmarking
description: Defines FCE latency, throughput, memory, CPU/GPU, thermal, power, and degradation profiling with all values marked as measured targets, not claims. Use for benchmark plans, performance budgets, profiling protocols, degraded-mode testing, or GPU baseline-vs-candidate comparisons.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Edge Benchmarking

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`.

## Purpose
Rigorous, reproducible performance measurement. **Every number is either "internal measured target — to be verified" or carries full measurement provenance. No exceptions. No vendor claims repeated as fact.**

## Trigger conditions
Benchmark plan/protocol work; latency budgets; SWaP-C analysis; degraded-mode profiling; acceleration comparisons (with fce-vision-acceleration-evaluation).

## Procedure
1. Define metrics: end-to-end and per-gate latency (all 7 gates + fusion handoff), throughput (objects/s), memory ceiling, CPU/GPU utilization, thermal envelope, power draw, degradation curves.
2. Every figure gets one of two labels: (a) TARGET — "internal measured target, to be verified," or (b) MEASURED — with hardware (exact model/SKU), workload, dataset (synthetic-labelled), software config, date, run count, variance, reproducibility notes.
3. Degraded-mode protocol covers all six constraint classes: compute limits, storage limits, network loss, degraded power, high CPU load, thermal constraints — with fail-closed behavior verified under each.
4. Baseline-vs-candidate protocol (GPU acceleration): identical workload + dataset + measurement harness; baseline = CPU/OpenCV/PyTorch pipeline; candidate = GPU-accelerated pipeline; named hardware both sides; report absolute numbers and deltas, never marketing multipliers.
5. Map results to Desired Outcomes only where valid (tactical latency, SWaP/edge constraints, real-time fusion support) — as internal targets, never DND requirements.

## Required reference files
RTM performance requirements, workload definitions, hardware candidate list, benchmark report template.

## Optional supporting scripts
None at Phase A. (Future: profiling harness — requires approval.)

## Allowed tools
Read, Grep, Glob, Write, Edit. (Bash added only when measurement is approved.)

## Disallowed tools
Bash (Phase A), WebSearch, WebFetch, MCP connectors, package installation.

## Example usage
"Set the policy-decision latency budget" → TARGET label → per-gate budget table → measurement protocol → REQ trace.

## Validation checklist
- [ ] Every number labelled TARGET or MEASURED(provenance).
- [ ] No vendor figures repeated as fact.
- [ ] Six degraded-mode classes covered; fail-closed verified per class.
- [ ] Baseline-vs-candidate protocol symmetric and named-hardware.
- [ ] REQ trace + verification method per benchmark.
- [ ] Internal-target framing (never DND requirement).

## Output template
Use `templates/benchmark-report.md`.

## Failure conditions (stop and escalate)
- Asked to publish an unmeasured figure as fact → refuse, relabel TARGET, flag.
- Hardware unavailable for a MEASURED claim → keep TARGET status.
- Result differs materially from vendor claim → record both, mark vendor claim unverified, feed decision record.
