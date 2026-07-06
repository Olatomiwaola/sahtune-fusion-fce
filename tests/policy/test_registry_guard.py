"""Registry + taxonomy guard.

Asserts (all must pass this sprint):
  - reason codes used by the evaluator are a subset of the docs/07 closed registry
    and are exactly RC-001..012;
  - the 11 actions and the D3 lattice dispositions all appear in docs/07;
  - the calibration taxonomy fixture's families set-equal the docs/07 D6 families
    AND the fixture still matches its retained sha-256 pin.
The fixture file itself is never edited by this test.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from fce_poc.policy import ACTIONS, REASON_CODES, SEVERITY_ORDER

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS07 = REPO_ROOT / "docs" / "07_policy-decision-model.md"
TAXONOMY_FIXTURE = REPO_ROOT / "data" / "fixtures" / "calibration" / "taxonomy.json"
PINNED_SHA256 = "59979c4d72b79cba6dec02892cc2940d609a705a2a724b5416ec275749bec240"

FAMILY_KEYS = {
    "Modality": "modality",
    "Classification label": "classification_label",
    "Domain label": "domain_label",
    "Release caveat": "release_caveat",
}


def _docs07_text():
    return DOCS07.read_text(encoding="utf-8")


def _d6_section(text):
    after = text.split("### Enumerated taxonomy registry", 1)[1]
    return after.split("\n## Model", 1)[0]


def _family_values(d6, header):
    # Slice from this bold header to the next bold header, collect single-column rows.
    block = d6.split(f"**{header}**", 1)[1].split("**", 1)[0]
    values = set()
    for line in block.splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        inner = s[1:-1].strip()
        if inner in ("Value", "") or set(inner) <= set("-: "):
            continue
        if "|" in inner:  # multi-column row (e.g. mapping table) -> not a family table
            continue
        values.add(inner)
    return values


def test_reason_codes_subset_of_docs07_registry():
    docs_codes = set(re.findall(r"RC-\d{3}", _docs07_text()))
    used = set(REASON_CODES)
    assert used <= docs_codes, f"codes not in docs/07: {used - docs_codes}"
    assert used == {f"RC-{i:03d}" for i in range(1, 13)}


def test_actions_and_lattice_present_in_docs07():
    text = _docs07_text()
    for action in ACTIONS:
        assert action in text, f"action missing from docs/07: {action}"
    for disposition in SEVERITY_ORDER:
        assert disposition in text, f"lattice disposition missing from docs/07: {disposition}"


def test_taxonomy_fixture_set_equals_docs07_d6_families():
    fixture = json.loads(TAXONOMY_FIXTURE.read_text(encoding="utf-8"))
    d6 = _d6_section(_docs07_text())
    for header, key in FAMILY_KEYS.items():
        assert _family_values(d6, header) == set(fixture[key]), f"family mismatch: {header}"


def test_taxonomy_fixture_matches_retained_sha256_pin():
    digest = hashlib.sha256(TAXONOMY_FIXTURE.read_bytes()).hexdigest()
    assert digest == PINNED_SHA256
