"""Shared test fixtures: calibration-fixture paths and loaders.

All fixtures are the calibration set only; no held-out material exists at M2
(held-out sealing is M6, GDR-003/004). Fixtures are loaded via `normalize()` — the
same normalization function the runtime path uses — per GDR-016.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fce_poc.taxonomy import load_taxonomy

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "data" / "fixtures" / "calibration"


def load_fixture(name: str) -> dict:
    """Load a calibration fixture JSON as a raw mapping."""
    with open(FIXTURE_DIR / name, encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURE_DIR


@pytest.fixture
def taxonomy():
    return load_taxonomy(FIXTURE_DIR / "taxonomy.json")


@pytest.fixture
def valid_raw() -> dict:
    return load_fixture("valid_object.json")
