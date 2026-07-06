"""CANON-1 canonical serialization + hashing (FCE-DR-SCH-004 D1).

Single profile shared by the envelope integrity_hash and the audit
record_content_hash. Reference alignment to RFC 8785 only — no crypto claim.

Rules (D1):
- json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False), UTF-8,
  sha-256 lowercase hex.
- Order-insensitive list fields are sorted before serialization.
- Value domain: integers, strings, booleans, null, objects, lists. NO floats —
  any float anywhere raises FloatInHashDomain; the caller refuses fail-closed.
- Absent != null: this module hashes what it is given; requiredness is enforced
  by the writer before hashing.
"""

from __future__ import annotations

import hashlib
import json

# D1(5): declared order-insensitive list fields, sorted before serialization.
ORDER_INSENSITIVE_FIELDS = (
    "release_caveat",
    "parent_object_ids",
    "reason_codes",
    "policy_rule_ids",
    "source_object_ids",
)


class FloatInHashDomain(ValueError):
    """Raised when a float appears in the hashed value domain (D1(6))."""


def _element_sort_key(element):
    # Deterministic ordering for order-insensitive list members of any JSON type.
    return json.dumps(element, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _prepare(value):
    """Recursively reject floats and sort declared order-insensitive lists."""
    # bool must be checked before int (bool is an int subclass) — both are allowed.
    if isinstance(value, bool):
        return value
    if isinstance(value, float):
        raise FloatInHashDomain(f"float not permitted in the hashed domain: {value!r}")
    if isinstance(value, dict):
        out = {}
        for key, sub in value.items():
            prepared = _prepare(sub)
            if key in ORDER_INSENSITIVE_FIELDS and isinstance(prepared, list):
                prepared = sorted(prepared, key=_element_sort_key)
            out[key] = prepared
        return out
    if isinstance(value, list):
        return [_prepare(item) for item in value]
    # int, str, None pass through.
    return value


def canonical_bytes(obj) -> bytes:
    prepared = _prepare(obj)
    text = json.dumps(prepared, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return text.encode("utf-8")


def sha256_hex(obj) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()
