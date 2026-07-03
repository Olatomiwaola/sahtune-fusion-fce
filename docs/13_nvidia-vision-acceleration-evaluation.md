# 13 — NVIDIA Vision-Acceleration Evaluation (OPTIONAL track) v0 (draft)

Owner: `fce-lead-systems-architect`. Skill: `fce-vision-acceleration-evaluation`.
This is an OPTIONAL evaluation/benchmark track. It is never a mandatory core
dependency and never the compliance authority. No installation is performed.
All vendor statements are VENDOR CLAIM (unverified) until measured by Kanatir.

## Hard separation

CV training/inference acceleration is strictly separated from FCE compliance
enforcement. No NVIDIA tool or model becomes the compliance authority. Any
accelerated path still enters at G1 and passes all seven gates (`05`) and
preserves all 15 mandatory metadata fields (`06`).

## Candidate taxonomy (used exactly)

- CV-CUDA — GPU pre/post-processing library (not a CV model).
- DALI — data loading/decoding/augmentation for pipelines.
- TAO — fine-tuning/optimizing vision/foundation models.
- DeepStream — real-time video analytics pipelines.
- TensorRT — optimized inference deployment.
- Jetson — edge compute hardware (candidate hardware).
- NVIDIA Agent Skills — external skill packages (uncontrolled external skills).

## Relevance

Relevant to evaluate for EO/IR preprocessing and synthetic video pipelines:
CV-CUDA, DALI, TensorRT, Jetson. Not relevant to the FCE core (policy,
classification, provenance, audit, compliance): none of the candidates belong in
the compliance-decision path. NVIDIA Agent Skills are out of scope as
uncontrolled external skills.

## Decision records

### DR-001 — CV-CUDA (pre/post-processing library)
- Context: EO/IR preprocessing for ingestion, and synthetic video generation.
- Relevant to FCE core: no; touches preprocessing only.
- Vendor claims (UNVERIFIED): GPU speedups over CPU preprocessing.
- Kanatir measurements: none.
- Risks: CUDA dependence, vendor lock-in, licensing, reproducibility, security
  review, export/supply-chain.
- Benchmark plan: baseline CPU/OpenCV vs candidate on named hardware, identical
  synthetic workload, per `fce-edge-benchmarking`.
- DND mapping (internal targets only): FCE-DES-01, FCE-DES-03.
- DECISION: EVALUATE LATER — optional evaluation track only. Approvals pending.

### DR-002 — DALI (data pipeline)
- Fit: synthetic training/data pipelines. Relevant to core: no.
- Vendor claims (UNVERIFIED): faster data loading/augmentation.
- DECISION: EVALUATE LATER — optional; pending rig approval.

### DR-003 — TAO (model fine-tuning)
- Fit: fine-tuning advisory CV models only (advisory, never enforcement).
- Relevant to core: no. DECISION: EVALUATE LATER — low priority; advisory-only.

### DR-004 — DeepStream (video analytics)
- Fit: real-time video analytics for advisory detection only.
- Relevant to core: no. DECISION: EVALUATE LATER — pending use-case need.

### DR-005 — TensorRT (inference deployment)
- Fit: optimized inference for advisory models at the edge.
- Relevant to core: no. DECISION: EVALUATE LATER — pair with Jetson eval.

### DR-006 — Jetson (edge hardware)
- Fit: candidate edge-class hardware for benchmarking (OPEN-03).
- Relevant to core: no (hardware host, not authority).
- DECISION: EVALUATE LATER — candidate benchmark hardware, named-hardware rig.

### DR-007 — NVIDIA Agent Skills (external skills)
- Treated as uncontrolled external skills.
- DECISION: REJECT for FCE use (no external installs; supply-chain and control
  risk). Re-evaluate only under explicit Kanatir approval and security review.

## Benchmark discipline

Report absolute numbers and deltas on named hardware, never marketing
multipliers. Baseline and candidate use identical workload, dataset (SYNTHETIC),
and harness. Any Kanatir result that differs from a vendor claim records both and
marks the vendor claim unverified.

## Facts / Assumptions / Vendor claims / Judgment / Uncertainty

- Facts: taxonomy categories; separation-of-concerns rule; no install performed.
- Assumptions: Jetson-class hardware is the likely benchmark target (OPEN-03).
- Vendor claims (unverified): all NVIDIA performance statements.
- Judgment: evaluate-later for preprocessing candidates; reject external skills.
- Uncertainty: whether any candidate is ever adopted; adoption would remain an
  optional evaluation track, decided by decision record with security sign-off.
