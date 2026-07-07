"""ARCH-07 label propagation — pure function (docs/18 §2).

High-water-mark (most-restrictive) combination of parent labels. Pure: no I/O, no
clock, no state, no writes; deterministic; invoked only by ARCH-08 post-permit.
Output labels are computed here and nowhere else (single label writer via ARCH-08).
"""

from __future__ import annotations


def _classification_level(label) -> int:
    # PROJ-LEVEL-N: higher N = more restrictive. Non-conforming labels sort last-safe.
    try:
        return int(str(label).rsplit("-", 1)[1])
    except (ValueError, IndexError):
        return -1


def hwm(parent_tuples):
    """Most-restrictive (classification, domain, sorted-caveats) over the parents.

    parent_tuples: iterable of (classification, domain, caveats-iterable).
    Post-permit inputs share one domain (cross-domain is blocked upstream);
    a differing domain is a programming error and raises.
    """
    parents = list(parent_tuples)
    if not parents:
        raise ValueError("hwm() requires at least one parent tuple")

    classification = max((p[0] for p in parents), key=_classification_level)

    domains = {p[1] for p in parents}
    if len(domains) != 1:
        raise ValueError(f"hwm() called with mixed domains {domains} (cross-domain is blocked upstream)")
    domain = next(iter(domains))

    caveats = set()
    for p in parents:
        caveats.update(p[2] or [])

    return (classification, domain, sorted(caveats))
