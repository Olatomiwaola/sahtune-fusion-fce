---
name: fce-vision-acceleration-evaluation
description: Evaluates NVIDIA CV-CUDA, DALI, TAO, DeepStream, TensorRT, Jetson, and NVIDIA Agent Skills as an OPTIONAL evaluation track for FCE EO/IR preprocessing, synthetic sensor generation, training-data pipelines, edge inference, and performance benchmarking. Use whenever NVIDIA tooling, GPU acceleration, CUDA, vision pipeline optimization, or edge inference hardware is mentioned or considered for the FCE.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# FCE Vision Acceleration Evaluation (NVIDIA track)

Kanatir-internal skill. Governed by `.claude/agents/_SHARED_CONSTRAINTS.md`. This is an **optional evaluation/benchmark track — never a mandatory core dependency, never the compliance authority.**

## Purpose
Disciplined evaluation of NVIDIA vision-acceleration tooling for possible use in FCE EO/IR preprocessing, synthetic video pipelines, training-data pipelines, edge inference, and benchmark demonstrations — producing an adopt / evaluate-later / reject decision record for each candidate.

## Tool taxonomy (use these categories exactly — miscategorization is a failure)
- **CV-CUDA** — GPU-accelerated **pre/post-processing library** for image/video AI pipelines. It is **not a computer-vision model.**
- **DALI** — data **loading, decoding, augmentation, and preprocessing** for training/data pipelines.
- **TAO** — **fine-tuning and optimizing** vision/foundation models.
- **DeepStream** — **real-time video analytics pipelines.**
- **TensorRT** — **optimized inference deployment.**
- **Jetson** — edge compute hardware platform (evaluation candidate hardware).
- **NVIDIA Agent Skills** — external skill packages; treated as **uncontrolled external skills.**

## Hard rules
1. **No installation** of external NVIDIA skills, packages, plugins, agents, or MCP connectors without explicit Kanatir approval. Evaluation is on paper and, post-approval, on isolated benchmark rigs.
2. **No performance claims** ("5x faster" etc.) unless measured on Kanatir-selected hardware and workload. All NVIDIA statements are **vendor claims until verified by Kanatir benchmark.**
3. **Separation of concerns:** CV training/inference acceleration is strictly separated from FCE compliance enforcement. No NVIDIA model or tool ever becomes the compliance authority; FCE enforcement remains deterministic, policy-governed, and auditable. Accelerated paths still pass all 7 gates and preserve all mandatory metadata.
4. **DND mapping discipline:** map candidate benefits to Desired Outcomes only where valid — tactical latency, SWaP/edge constraints, real-time fusion support — as internal targets.

## Trigger conditions
Any mention of NVIDIA tooling, GPU acceleration, CUDA, Jetson, vision pipeline optimization, inference optimization, or acceleration benchmarking in FCE context.

## Evaluation procedure (per candidate)
1. **Relevance:** which of the seven candidates are relevant to the use case; which are **not relevant to the FCE core** (record both lists).
2. **Fit:** where it could help — EO/IR preprocessing, synthetic video pipelines, model fine-tuning, edge benchmark, deployment optimization — with the correct taxonomy category.
3. **Risk assessment:** vendor lock-in, CUDA dependence, licensing terms, reproducibility, security review needs, uncontrolled external skills, unsupported claims, export/security implications, supply-chain risk (with security-assurance-engineer and devsecops-engineer).
4. **Compatibility:** license, hardware dependency, CUDA/Jetson version compatibility, benchmark validity.
5. **Benchmark plan:** baseline CPU/OpenCV/PyTorch pipeline vs GPU-accelerated candidate pipeline, identical workload/dataset, **named hardware**, per fce-edge-benchmarking protocol.
6. **Decision record** (`templates/decision-record.md`): **adopt / evaluate later / reject**, owned by fce-lead-systems-architect, with security and supply-chain sections. Architectural status if adopted: **optional benchmark/evaluation track, not mandatory core dependency.**

## Required reference files
fce-edge-benchmarking protocol, threat model, dependency policy (devsecops), decision-record index (docs/12_decision_records/).

## Optional supporting scripts
None. (Benchmark harnesses require approval.)

## Allowed tools
Read, Grep, Glob, Write, Edit.

## Disallowed tools
Bash, WebSearch, WebFetch, MCP connectors, any installer. (Vendor documentation is requested through the main session, which handles fetching under user oversight.)

## Example usage
"Should we use CV-CUDA for EO/IR preprocessing?" → taxonomy check (preprocessing library, not model) → fit: EO/IR preprocess + synthetic video → risks: CUDA dependence, license, reproducibility → benchmark plan vs OpenCV baseline on named hardware → decision record: evaluate later, pending rig approval.

## Validation checklist
- [ ] Taxonomy categories correct for every candidate named.
- [ ] Relevant vs not-relevant-to-FCE-core lists explicit.
- [ ] Zero vendor figures repeated as fact; all marked vendor-claim-unverified.
- [ ] Compliance separation stated; accelerated paths gate- and metadata-preserving.
- [ ] Benchmark plan named-hardware, baseline-symmetric.
- [ ] License/CUDA/Jetson/export/supply-chain/reproducibility all assessed.
- [ ] Decision record complete with adopt/evaluate-later/reject.
- [ ] DND mapping only to valid Desired Outcomes, as internal targets.
- [ ] No installation performed or implied without approval.

## Output template
```
## NVIDIA evaluation: <scope>
1. Relevant: <tools + category>   Not relevant to FCE core: <tools + why>
2. Potential help: <use-case mapping>
3. Risks: <lock-in, CUDA, licensing, reproducibility, security review, uncontrolled skills, claims, export/security>
4. Compatibility: <license/hardware/CUDA/Jetson/benchmark validity>
5. Benchmark plan: <baseline vs candidate, named hardware, workload>
6. Decision: <adopt | evaluate later | reject> — architectural status: optional evaluation track
Approvals required: <externals list>
Facts / Assumptions / Vendor claims (unverified) / Judgment / Uncertainty: <split>
```

## Failure conditions (stop and escalate)
- Any request to install NVIDIA components pre-approval → refuse; log approval request.
- Any draft placing NVIDIA tooling in the compliance decision path → blocking finding to architect + security-assurance-engineer.
- Vendor claim about to be published unverified → strip or relabel; flag.
