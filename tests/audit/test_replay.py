"""Replay tests: R2 reconstruction (T10) and detail-ID poisoning resistance (T11)."""

from __future__ import annotations

from fce_poc.policy.attributes import InjectedClock
from fce_poc.audit.chain import load_records
from fce_poc.audit.demo import ATTEMPT_R, OBJ_A, build_sample
from fce_poc.audit.replay import reconstruct
from fce_poc.provenance import build_graph


def test_t10_replay_r2_reconstruction(tmp_path):  # T10 FCE-REQ-AUD-003
    path = tmp_path / "a.jsonl"
    build_sample(path, tmp_path / "pkg", InjectedClock(now=1000))
    result = reconstruct(path)
    assert result.r1_ok is True
    assert result.ok is True
    assert result.errors == []
    assert len(result.decisions) == 8
    blocked = [d for d in result.decisions if "RC-003" in d.reason_codes]
    assert len(blocked) == 1
    assert blocked[0].disposition == "segregate"


def test_t11_replay_poisoning_ignores_asserted_id(tmp_path):  # T11 RT-M4S7-03
    path = tmp_path / "a.jsonl"
    build_sample(path, tmp_path / "pkg", InjectedClock(now=1000))
    records = load_records(path)
    # Record 4 is a G1 reject asserting OBJ_A via event_detail.source_asserted_object_id.
    reject = records[3]
    assert reject["event_detail"]["source_asserted_object_id"] == OBJ_A
    assert reject["source_object_ids"] == []  # trusted field empty

    result = reconstruct(path)
    # The reject decision's lineage fields never contain the asserted id.
    reject_decision = result.decisions[3]
    assert reject_decision.source_object_ids == ()
    assert OBJ_A not in reject_decision.source_object_ids

    # Provenance graph: the assertion injects no parent onto OBJ_A (still a root),
    # and the reject anchors to its attempt id.
    graph = build_graph(records)
    assert graph.parents_of(OBJ_A) == set()
    assert ATTEMPT_R in graph.reject_attempts
