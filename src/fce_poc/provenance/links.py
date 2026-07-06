"""Parent-link capture from emitted audit records (FCE-REQ-PRV-001/-002).

Builds the parent->child link set for the four Sprint 8 outcomes:
- accepted: ingestion origins (trusted source_object_ids) are lineage roots;
- transformed / fused: output_object_id has parents = source_object_ids;
- rejected: G1 reject/quarantine anchors to event_detail.ingest_attempt_id, NEVER
  to event_detail.source_asserted_object_id (untrusted — RT-M4S7-03).

Lineage reads trusted fields only; source_asserted_object_id is never consulted.
"""

from __future__ import annotations

from dataclasses import dataclass, field

_DERIVING_CLASSES = frozenset({"transformation", "fusion-decision"})
_REFUSED_DISPOSITIONS = frozenset({"reject", "quarantine"})


@dataclass
class ProvenanceGraph:
    links: set = field(default_factory=set)            # (parent, child)
    ingested: set = field(default_factory=set)         # trusted origin object ids
    reject_attempts: set = field(default_factory=set)  # ingest_attempt_id anchors
    derived_outputs: set = field(default_factory=set)  # outputs of deriving classes

    def parents_of(self, child) -> set:
        return {p for (p, c) in self.links if c == child}


def build_graph(records) -> ProvenanceGraph:
    graph = ProvenanceGraph()
    for rec in records:
        cls = rec.get("event_type")
        disposition = rec.get("disposition")
        output = rec.get("output_object_id")
        sources = list(rec.get("source_object_ids", []))
        detail = rec.get("event_detail", {}) or {}

        if cls == "ingestion":
            if disposition in _REFUSED_DISPOSITIONS:
                # Anchor to the FCE-authoritative attempt id, never source-asserted.
                attempt = detail.get("ingest_attempt_id")
                if attempt:
                    graph.reject_attempts.add(attempt)
            else:
                # Accepted ingestion: trusted origins become lineage roots.
                graph.ingested.update(sources)
            continue

        if output is not None:
            for parent in sources:
                graph.links.add((parent, output))
            if cls in _DERIVING_CLASSES:
                graph.derived_outputs.add(output)
    return graph


def ancestors(graph: ProvenanceGraph, node) -> set:
    seen = set()
    stack = list(graph.parents_of(node))
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(graph.parents_of(current))
    return seen


def roots_reached(graph: ProvenanceGraph, node) -> set:
    """Ancestor nodes that are themselves lineage roots (no parents)."""
    return {a for a in ancestors(graph, node) if not graph.parents_of(a)}
