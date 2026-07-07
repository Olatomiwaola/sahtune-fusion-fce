"""C3 bidirectional G5-entry parentage cross-check (docs/18 §1).

Runs over the provenance graph (ARCH-09) built from emitted audit records
(`provenance/links.py`). For every object arriving as a merge parent:

- Forward: an object claiming a derived lifecycle type must have kernel-recorded
  parentage in ARCH-09 matching its `parent_object_ids`.
- Reverse: an object recorded in ARCH-09 as a derivation output must present as a
  derived type with matching parentage.
- Empty `parent_object_ids` on a derived type is refused (G2 field-13 backstop +
  kernel assert).

Any mismatch → (False, "unrecorded_parentage"); the kernel quarantines RC-001.
"""

from __future__ import annotations

DERIVED_TYPES = frozenset(
    {"tracklet", "fused_track", "transformed_object", "downgraded_object"}
)
UNRECORDED_PARENTAGE = "unrecorded_parentage"


def check_parent(parent, graph):
    """Return (ok, flag). parent has .object_id, .lifecycle_type, .parent_object_ids."""
    recorded = graph.parents_of(parent.object_id)          # set of kernel-recorded parents
    is_output = parent.object_id in graph.derived_outputs
    claimed = set(parent.parent_object_ids or [])
    derived = parent.lifecycle_type in DERIVED_TYPES

    # Forward: derived type must have matching kernel-recorded parentage.
    if derived:
        if not claimed:
            return False, UNRECORDED_PARENTAGE  # empty parents on a derived type
        if recorded != claimed:
            return False, UNRECORDED_PARENTAGE  # self-declared / caller-supplied parentage

    # Reverse: a known derivation output must present as a derived type with match.
    if is_output and (not derived or recorded != claimed):
        return False, UNRECORDED_PARENTAGE

    return True, None
