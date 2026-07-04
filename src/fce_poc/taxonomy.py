"""Taxonomy fixture loader (fields 5, 8, 9, 10).

Loads the project-taxonomy value families used by the enum rules. Values are
populated from docs/07 at Sprint 4 (docs/07 not supplied to the freeze chat — the
PoC therefore loads them as a calibration fixture; see RT-M2S3-04 taxonomy-fixture
provenance). Any value outside the fixture fails closed — unknown value = reject.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Taxonomy:
    """Project-taxonomy enums. `contains` fails closed on unknown category/value."""

    modality: frozenset[str]
    classification_label: frozenset[str]
    domain_label: frozenset[str]
    release_caveat: frozenset[str]

    def contains(self, category: str, value: object) -> bool:
        allowed = getattr(self, category, None)
        if not isinstance(allowed, frozenset):
            return False  # unknown category -> fail closed
        return value in allowed


def load_taxonomy(path: str | Path) -> Taxonomy:
    """Load a taxonomy fixture JSON into a Taxonomy. Missing categories -> empty."""
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return Taxonomy(
        modality=frozenset(data.get("modality", [])),
        classification_label=frozenset(data.get("classification_label", [])),
        domain_label=frozenset(data.get("domain_label", [])),
        release_caveat=frozenset(data.get("release_caveat", [])),
    )
