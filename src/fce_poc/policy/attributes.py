"""PIP attribute model and the injected clock.

RT-M3S5-02 / H4: the clock is INJECTED only — this module never reads the wall
clock. Override time-limit evaluation depends on the injected clock; trusted /
attested time is H4 and remains open (stated in EVD-M3, FU-M3S5-1).

RT-M3S5-03 / H3-H4: `authenticated` / `integrity_bound` are fixture-supplied
flags — mechanism-simulated, not demonstrated authentication (stated in EVD-M3).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PIPAttribute:
    """A PIP-sourced attribute (docs/07 PIP; B1 / FCE-REQ-SEC-002)."""

    attr_id: str
    value: object
    authenticated: bool
    integrity_bound: bool

    @property
    def valid(self) -> bool:
        return self.authenticated and self.integrity_bound


@dataclass(frozen=True)
class InjectedClock:
    """Injected monotonic tick. No wall-clock reads anywhere (H4)."""

    now: int


def all_attributes_valid(attributes) -> bool:
    """RULE-POL-004: every PIP attribute authenticated AND integrity-bound (B1)."""
    return all(a.valid for a in attributes)


def failing_attribute_ids(attributes) -> tuple[str, ...]:
    return tuple(sorted(a.attr_id for a in attributes if not a.valid))
