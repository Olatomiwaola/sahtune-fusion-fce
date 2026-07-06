"""Writer + chain tests: non-null confidence (T3), tamper set (T8), torn write (T9)."""

from __future__ import annotations

import json

import pytest

from fce_poc.policy.attributes import InjectedClock
from fce_poc.audit.chain import verify_chain
from fce_poc.audit.demo import build_sample
from fce_poc.audit.records import RecordValidationError, new_record
from fce_poc.audit.writer import AuditChainError, AuditWriter
from test_records import valid_body  # reuse the per-class builder (same dir on sys.path)


def test_t3_non_null_confidence_refused(tmp_path):  # T3 D1(6), docs/08 field 13
    writer = AuditWriter(tmp_path / "a.jsonl", InjectedClock(now=1))
    with pytest.raises(RecordValidationError):
        writer.append(new_record(**valid_body("policy-decision", confidence=1)))


def test_t8_chain_tamper_edit_delete_reorder(tmp_path):  # T8 FCE-REQ-AUD-002
    path = tmp_path / "a.jsonl"
    build_sample(path, tmp_path / "pkg", InjectedClock(now=1000))
    lines = path.read_text().splitlines()

    # (a) edit a record's content without recomputing its hash -> R1 fails.
    edited = list(lines)
    rec = json.loads(edited[2])
    rec["actor_identity"] = "tampered"
    edited[2] = json.dumps(rec, ensure_ascii=False)
    path.write_text("\n".join(edited) + "\n")
    assert verify_chain(path).ok is False

    # (b) delete a record -> R1 fails.
    path.write_text("\n".join(lines[:3] + lines[4:]) + "\n")
    assert verify_chain(path).ok is False

    # (c) reorder two records -> R1 fails.
    reordered = list(lines)
    reordered[1], reordered[2] = reordered[2], reordered[1]
    path.write_text("\n".join(reordered) + "\n")
    assert verify_chain(path).ok is False


def test_t9_torn_write_refuses_fail_closed(tmp_path):  # T9 FU-M4S7-2, RT-M4S7-02
    path = tmp_path / "a.jsonl"
    build_sample(path, tmp_path / "pkg", InjectedClock(now=1000))
    text = path.read_text()
    # Truncate mid-last-line (drop the final newline and some trailing bytes).
    torn = text[: -len(text.splitlines()[-1]) // 2]
    path.write_text(torn)
    # Corrupted-tail chain verify fails.
    assert verify_chain(path).ok is False
    # Writer start refuses fail-closed on the partial tail.
    with pytest.raises(AuditChainError):
        AuditWriter(path, InjectedClock(now=2000))
