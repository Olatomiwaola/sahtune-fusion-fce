"""FCE audit writer PoC (M4 Sprint 8).

CANON-1 canonicalization + hashing, envelope integrity_hash, 18-field record
construction/validation, append-only JSONL writer with tail-verify, R1 chain
verification, R1+R2 replay, and JSONL export + integrity manifest. stdlib only;
injected clock (H4); signature is a placeholder (H6). No crypto/trusted-time claims.
"""

from .canonical import FloatInHashDomain, canonical_bytes, sha256_hex
from .chain import ChainResult, load_records, verify_chain
from .envelope_integrity import compute_integrity_hash, verify_integrity
from .export import ExportResult, export_package, recompute_manifest_sha256
from .records import RecordValidationError, new_record, validate_record_body
from .replay import ReplayResult, reconstruct
from .writer import AuditChainError, AuditWriter, GENESIS_PREV_HASH, content_hash

__all__ = [
    "FloatInHashDomain", "canonical_bytes", "sha256_hex",
    "ChainResult", "load_records", "verify_chain",
    "compute_integrity_hash", "verify_integrity",
    "ExportResult", "export_package", "recompute_manifest_sha256",
    "RecordValidationError", "new_record", "validate_record_body",
    "ReplayResult", "reconstruct",
    "AuditChainError", "AuditWriter", "GENESIS_PREV_HASH", "content_hash",
]
