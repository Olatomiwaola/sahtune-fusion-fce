"""Provenance walk (T12) — FCE-REQ-PRV-001/-002."""

from __future__ import annotations

from fce_poc.policy.attributes import InjectedClock
from fce_poc.audit.chain import load_records
from fce_poc.audit.demo import ATTEMPT_R, OBJ_A, OBJ_B, OBJ_F, OBJ_T, build_sample
from fce_poc.provenance import build_graph, roots_reached


def test_t12_provenance_walk(tmp_path):
    path = tmp_path / "a.jsonl"
    build_sample(path, tmp_path / "pkg", InjectedClock(now=1000))
    graph = build_graph(load_records(path))

    # Transformed and fused outputs reach their original ingested objects.
    assert roots_reached(graph, OBJ_T) == {OBJ_A}
    assert roots_reached(graph, OBJ_F) == {OBJ_A, OBJ_B}
    assert {OBJ_A, OBJ_B} <= graph.ingested

    # No orphaned derived outputs: each has at least one parent link.
    assert graph.derived_outputs == {OBJ_T, OBJ_F}
    assert all(graph.parents_of(d) for d in graph.derived_outputs)

    # G1 rejects anchor to attempt IDs.
    assert ATTEMPT_R in graph.reject_attempts
