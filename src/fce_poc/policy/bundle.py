"""Policy bundle loading, version pinning, and signature-placeholder check.

docs/07 Hot-reload (FCE-DES-02): PAP loads signed bundles with version pinning;
invalid or unsigned bundles are rejected fail-closed with rollback to the last
good version. The signature check here is an EXPLICIT PLACEHOLDER — no crypto is
performed and no crypto claim is made (real root-of-trust is H6).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PolicyBundle:
    version: str
    signature_placeholder: str  # "valid" | "invalid" | "unsigned"
    permits: dict[str, Any]     # mission -> {classifications, domains, caveats}
    merge_permits: tuple[dict[str, Any], ...]

    @property
    def signature_ok(self) -> bool:
        # Placeholder only: unsigned/invalid -> fail closed. No crypto claim.
        return self.signature_placeholder == "valid"


def load_bundle(path: str | Path) -> PolicyBundle:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return PolicyBundle(
        version=data["version"],
        signature_placeholder=data.get("signature_placeholder", "unsigned"),
        permits=data.get("permits", {}),
        merge_permits=tuple(data.get("merge_permits", [])),
    )


def bundle_is_valid(bundle: PolicyBundle, pinned_version: str) -> bool:
    """Version pinning + signature placeholder. Both must hold or fail closed."""
    return bundle.signature_ok and bundle.version == pinned_version


def covers_merge(bundle: PolicyBundle, inputs) -> bool:
    """True iff some merge_permit covers the combined labels of all inputs.

    An input is covered by a permit when its classification/domain/caveats all
    fall within that permit's sets (docs/07 no-unauthorized-merge invariant).
    """
    for permit in bundle.merge_permits:
        classes = set(permit.get("classifications", []))
        domains = set(permit.get("domains", []))
        caveats = set(permit.get("caveats", []))
        if all(
            obj.get("classification_label") in classes
            and obj.get("domain_label") in domains
            and set(obj.get("release_caveat", [])) <= caveats
            for obj in inputs
        ):
            return True
    return False
