"""FCE laptop-PoC schema-validation package (M2, Sprint 4).

Scope per docs/05_data_model/m2-poc-file-plan.md and leadership decision #5:
Python 3.12, standard library plus pinned pytest only. This package implements
envelope normalization (GDR-016), the G1 gates (RULE-VAL-002/003/017), and the
G2 validator (RULE-VAL-001, 004-016, plus interim unknown-field handling).

Explicit non-scope at Sprint 4: no policy evaluation (M3), no audit writer (M4 —
only a stub interface here), no merge logic (M5), no open-source download (M6),
no held-out evaluation (M7), no performance figures (M8), no integrity-hash
verification (deferred pending input-domain definition, see RULE-VAL-016).
Green results here are code-correctness evidence only — never a concept-validation
or proof claim (docs/16 layer separation).
"""

from .envelope import MISSING, Envelope, normalize
from .gates import (
    ALLOWED_DATA_ORIGINS,
    SUPPORTED_SCHEMA_VERSIONS,
    FORCED_BINDING_STATE,
    force_policy_binding_state,
    g1_version_origin_gate,
)
from .taxonomy import Taxonomy, load_taxonomy
from .validator import Disposition, NullAuditSink, evaluate, validate_g2

__all__ = [
    "MISSING",
    "Envelope",
    "normalize",
    "ALLOWED_DATA_ORIGINS",
    "SUPPORTED_SCHEMA_VERSIONS",
    "FORCED_BINDING_STATE",
    "force_policy_binding_state",
    "g1_version_origin_gate",
    "Taxonomy",
    "load_taxonomy",
    "Disposition",
    "NullAuditSink",
    "evaluate",
    "validate_g2",
]
