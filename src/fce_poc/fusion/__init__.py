"""FCE fusion merge evaluator (M5 Sprint 10) — governed by docs/18.

ARCH-08 kernel (sole fusion authority), ARCH-07 pure-function HWM labels,
exact-multiset MERGE-PERMIT coverage, C3 bidirectional parentage cross-check over
the provenance graph. Audit via the existing writer/records modules. stdlib only.
"""

from .crosscheck import DERIVED_TYPES, UNRECORDED_PARENTAGE, check_parent
from .kernel import MergeDecision, MergeParent, MergeRequest, evaluate_merge
from .labels import hwm
from .permits import canonical_tuple, covers, tuples_from_objects

__all__ = [
    "DERIVED_TYPES",
    "UNRECORDED_PARENTAGE",
    "check_parent",
    "MergeDecision",
    "MergeParent",
    "MergeRequest",
    "evaluate_merge",
    "hwm",
    "canonical_tuple",
    "covers",
    "tuples_from_objects",
]
