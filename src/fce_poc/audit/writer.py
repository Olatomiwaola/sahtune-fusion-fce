"""Append-only JSONL audit writer with tail verification and CANON-1 hash chain.

- Content hash (docs/08 field 14): CANON-1 over all 18 common fields + event_detail,
  EXCLUDING record_content_hash (14) and signature_placeholder (16), INCLUDING
  previous_record_hash (15). Genesis previous = 64 zeros.
- On open/start: tail verification (FU-M4S7-2) — the whole existing chain must parse
  and hash-link; a partial trailing line or broken link refuses fail-closed and the
  writer will not accept new events.
- Any validation failure or write/serialization error refuses fail-closed (exception;
  no partial emission).
"""

from __future__ import annotations

import json
from pathlib import Path

from .canonical import sha256_hex
from .records import validate_record_body

GENESIS_PREV_HASH = "0" * 64
_HASH_EXCLUDED = ("record_content_hash", "signature_placeholder")


class AuditChainError(Exception):
    """Raised when the on-disk chain fails tail/whole-chain verification."""


def content_hash(record: dict) -> str:
    """CANON-1 content hash over the record minus fields 14 and 16 (field 15 kept)."""
    hashable = {k: v for k, v in record.items() if k not in _HASH_EXCLUDED}
    return sha256_hex(hashable)


class AuditWriter:
    def __init__(self, path, clock):
        self.path = Path(path)
        self.clock = clock
        self._prev = GENESIS_PREV_HASH
        self._verify_tail_on_start()

    def _verify_tail_on_start(self) -> None:
        if not self.path.exists():
            self._prev = GENESIS_PREV_HASH
            return
        prev = GENESIS_PREV_HASH
        with open(self.path, encoding="utf-8") as handle:
            lines = handle.read().splitlines(keepends=True)
        for index, raw in enumerate(lines):
            if not raw.endswith("\n"):
                raise AuditChainError(f"partial trailing line at record {index} — refusing fail-closed")
            try:
                record = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise AuditChainError(f"unparseable record at line {index}: {exc}") from exc
            if record.get("previous_record_hash") != prev:
                raise AuditChainError(f"broken chain link at record {index}")
            if content_hash(record) != record.get("record_content_hash"):
                raise AuditChainError(f"content-hash mismatch at record {index}")
            prev = record["record_content_hash"]
        self._prev = prev

    def append(self, record_body: dict) -> dict:
        """Validate, chain, hash, and append one record. Returns the full record."""
        validate_record_body(record_body)
        record = dict(record_body)
        record["previous_record_hash"] = self._prev
        record["record_content_hash"] = content_hash(record)  # raises on float (fail-closed)
        line = json.dumps(record, ensure_ascii=False) + "\n"
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(line)
        self._prev = record["record_content_hash"]
        return record

    @property
    def chain_head_hash(self) -> str:
        return self._prev
