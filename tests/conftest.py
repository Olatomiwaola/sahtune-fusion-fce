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


# --- M3 Sprint 6 policy-evaluator fixtures -------------------------------------
# Kept in the single top-level conftest (a second conftest.py would collide on the
# module name `conftest` used by the M2 tests' `from conftest import load_fixture`).

from fce_poc.policy import InjectedClock, PIPAttribute, load_bundle  # noqa: E402

POLICY_DIR = REPO_ROOT / "data" / "fixtures" / "policy"
PINNED_VERSION = "0.1.0"


def _load_pip(name: str):
    return [
        PIPAttribute(
            attr_id=a["attr_id"],
            value=a["value"],
            authenticated=a["authenticated"],
            integrity_bound=a["integrity_bound"],
        )
        for a in load_json_policy(name)
    ]


def load_json_policy(name: str):
    with open(POLICY_DIR / name, encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def bundle():
    return load_bundle(POLICY_DIR / "bundle_proj-baseline_0.1.0.json")


@pytest.fixture
def pinned_version() -> str:
    return PINNED_VERSION


@pytest.fixture
def clock():
    return InjectedClock(now=100)


@pytest.fixture
def resolvable_classifications():
    return frozenset(load_fixture("taxonomy.json")["classification_label"])


@pytest.fixture
def valid_object() -> dict:
    # Reused M2 calibration object; passes G1 (source_authenticated defaults True).
    return load_fixture("valid_object.json")


@pytest.fixture
def pip_valid():
    return _load_pip("pip_valid.json")


@pytest.fixture
def pip_spoofed():
    return _load_pip("pip_spoofed.json")


@pytest.fixture
def pip_unauthenticated():
    return _load_pip("pip_unauthenticated.json")


@pytest.fixture
def make_request(valid_object, pip_valid):
    """Builder for an evaluation request with permit-happy defaults."""

    def _build(**overrides):
        request = {
            "object": dict(valid_object),
            "channel": {"domain": "DOMAIN-A"},
            "mission": "MISSION-ALPHA",
            "pip_attributes": list(pip_valid),
        }
        request.update(overrides)
        return request

    return _build
