"""G1-scope gate behaviour for M2.

Three G1 responsibilities, in the order they must run:

  1. force_policy_binding_state (RULE-VAL-017, B3/GDR-007) — policy_binding_state is
     FCE-authority-set only. It is forced to `unvalidated` at G1 regardless of any
     ingested value, and a source-supplied value is recorded as *detected*. This
     forcing executes BEFORE any G2 validation reads field 15 (the validator holds
     no rule for field 15 precisely because it is decided here, not validated).

  2. envelope-version gate (RULE-VAL-002, GDR-006) — schema_version must be a valid,
     supported semver; an unsupported version is rejected fail-closed before policy.

  3. data_origin gate (RULE-VAL-003) — data_origin must be one of the three v0.2.0
     provenance classes; any other value, including LIVE, is rejected fail-closed at
     G1 (FCE-DR-SCH-002, LIVE removed at TRL 1-3).

A G1 rejection means the object never reaches G2 evaluation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace

from .envelope import MISSING, Envelope

SUPPORTED_SCHEMA_VERSIONS = frozenset({"0.2.0"})
ALLOWED_DATA_ORIGINS = frozenset(
    {"SYNTHETIC", "SYNTHETIC-DERIVED", "PUBLIC-OPEN-SOURCE"}
)
FORCED_BINDING_STATE = "unvalidated"
BINDING_STATE_DETECTION_FLAG = "policy_binding_state_source_supplied"

_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class GateResult:
    """Outcome of the G1 version/origin gate."""

    passed: bool
    envelope: Envelope
    failed_rules: tuple[str, ...]


def force_policy_binding_state(env: Envelope) -> tuple[Envelope, tuple[str, ...]]:
    """Force field 15 to `unvalidated`; record detection of any source-supplied value.

    Runs before G2. The ingested value is never trusted. Detection fires when the
    source supplied a value for field 15 that is not the forced default (so a genuine
    pre-marking attempt such as `validated` is flagged; a well-formed object that
    omits the FCE-authority-set field is not).
    """
    supplied = env.policy_binding_state
    detected = supplied is not MISSING and supplied != FORCED_BINDING_STATE
    flags = (BINDING_STATE_DETECTION_FLAG,) if detected else ()
    forced = replace(env, policy_binding_state=FORCED_BINDING_STATE)
    return forced, flags


def g1_version_origin_gate(env: Envelope) -> GateResult:
    """Envelope-version gate + data_origin gate. Reject fail-closed before policy."""
    failed: list[str] = []

    version = env.schema_version
    if not (
        isinstance(version, str)
        and _SEMVER_RE.match(version)
        and version in SUPPORTED_SCHEMA_VERSIONS
    ):
        failed.append("RULE-VAL-002")

    origin = env.data_origin
    if not (isinstance(origin, str) and origin in ALLOWED_DATA_ORIGINS):
        failed.append("RULE-VAL-003")

    return GateResult(
        passed=not failed,
        envelope=env,
        failed_rules=tuple(sorted(failed)),
    )
