# tests/test_bundle_seal.py
# Sprint 14 Layer 1 — sealed-bundle integrity gate (FCE-DR-POC-004; GDR-009-adjacent).
# Confirms the pinned Layer-1 / held-out bundle is byte-identical to the Sprint 12
# seal record before any evaluation runs under it. Fail closed on mismatch.
# Path anchored to repo root (cwd-robust), matching the repo convention.

import hashlib
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SEALED_BUNDLE = REPO_ROOT / "data" / "fixtures" / "policy" / "bundle_proj-baseline_0.2.0.json"
SEALED_SHA256 = "6a830b2474a362f799fab045f0f2c23ca0b9d117c8f1e1d0acc5b51a69c53502"


def test_sealed_bundle_sha_matches_seal_record():
    raw = SEALED_BUNDLE.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    assert got == SEALED_SHA256, (
        "proj-baseline@0.2.0 bundle SHA "
        f"{got} != sealed seal-record value {SEALED_SHA256}; "
        "fail closed — do not evaluate under an unsealed/mutated bundle."
    )
