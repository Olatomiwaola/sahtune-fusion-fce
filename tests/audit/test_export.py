"""Export manifest (T13) — FCE-REQ-EXP-001."""

from __future__ import annotations

import hashlib

from fce_poc.policy.attributes import InjectedClock
from fce_poc.audit.chain import load_records
from fce_poc.audit.export import export_package, recompute_manifest_sha256
from fce_poc.audit.records import new_record
from fce_poc.audit.writer import AuditWriter
from test_records import valid_body


def test_t13_export_manifest(tmp_path):
    audit_path = tmp_path / "a.jsonl"
    clock = InjectedClock(now=1000)
    writer = AuditWriter(audit_path, clock)
    writer.append(new_record(**valid_body("ingestion")))
    writer.append(new_record(**valid_body("policy-decision")))

    result = export_package(audit_path, tmp_path / "pkg", clock, package_id="PKG-1")

    # per-file sha-256 correct
    assert result.manifest["files"][0]["sha256"] == hashlib.sha256(audit_path.read_bytes()).hexdigest()
    # chain_head_hash matches the last record's content hash
    records = load_records(audit_path)
    assert result.manifest["chain_head_hash"] == records[-1]["record_content_hash"]
    # manifest sha-256 recompute matches
    assert result.manifest_sha256 == recompute_manifest_sha256(result.manifest_path)

    # export-class record carries the manifest sha-256
    exp = writer.append(new_record(**valid_body(
        "export",
        event_detail={"manifest_ref": "manifest.json",
                      "record_range": [records[0]["audit_event_id"], records[-1]["audit_event_id"]],
                      "manifest_sha256": result.manifest_sha256})))
    assert exp["event_detail"]["manifest_sha256"] == result.manifest_sha256

    # manifest tamper detected via recompute
    result.manifest_path.write_bytes(result.manifest_path.read_bytes() + b" ")
    assert recompute_manifest_sha256(result.manifest_path) != result.manifest_sha256
