"""R1 — full-chain integrity verification (FCE-REQ-AUD-002).

Recompute every content hash and verify every previous-hash link from genesis;
report the first failure point.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .writer import GENESIS_PREV_HASH, content_hash


@dataclass(frozen=True)
class ChainResult:
    ok: bool
    record_count: int
    first_failure_index: int | None
    reason: str | None


def load_records(path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    records = []
    with open(path, encoding="utf-8") as handle:
        for raw in handle.read().splitlines():
            records.append(json.loads(raw))
    return records


def verify_chain(path) -> ChainResult:
    path = Path(path)
    prev = GENESIS_PREV_HASH
    count = 0
    if not path.exists():
        return ChainResult(True, 0, None, None)
    with open(path, encoding="utf-8") as handle:
        raw_lines = handle.read().splitlines(keepends=True)
    for index, raw in enumerate(raw_lines):
        if not raw.endswith("\n"):
            return ChainResult(False, index, index, "partial trailing line")
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            return ChainResult(False, index, index, f"unparseable: {exc}")
        if record.get("previous_record_hash") != prev:
            return ChainResult(False, index + 1, index, "broken previous-hash link")
        if content_hash(record) != record.get("record_content_hash"):
            return ChainResult(False, index + 1, index, "content-hash mismatch")
        prev = record["record_content_hash"]
        count += 1
    return ChainResult(True, count, None, None)
