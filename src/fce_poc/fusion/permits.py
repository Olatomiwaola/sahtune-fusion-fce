"""MERGE-PERMIT coverage — exact-multiset match only (docs/18 §4, docs/07 MERGE-PERMIT).

`covers()` is true iff the request's parent-tuple multiset EXACTLY matches one
enumerated entry in a permit's `permitted_combinations`. No wildcards, no patterns,
no `max_parents`; each combination fixes its own cardinality (RT-M5S9-01). A
combination [T1, T2] does not cover [T1, T1] or [T2, T2]; [T, T] is legal only when
explicitly enumerated (RT-M5S9-03).
"""

from __future__ import annotations

from collections import Counter


def canonical_tuple(classification, domain, caveats):
    """Canonical (classification, domain, caveat) tuple — caveats order-insensitive."""
    return (classification, domain, tuple(sorted(caveats or [])))


def tuples_from_objects(objects):
    """Parent-tuple list from label-bearing objects (classification/domain/caveat)."""
    return [
        canonical_tuple(o.get("classification_label"), o.get("domain_label"), o.get("release_caveat", []))
        for o in objects
    ]


def _combination_counter(combination):
    # combination entry = list of [classification, domain, [caveats]]
    return Counter(canonical_tuple(c, d, cav) for (c, d, cav) in combination)


def covers(request_tuples, merge_permits) -> bool:
    """True iff the request tuple-multiset exactly equals some enumerated combination."""
    want = Counter(request_tuples)
    for permit in merge_permits:
        for combination in permit.get("permitted_combinations", []):
            if _combination_counter(combination) == want:
                return True
    return False
