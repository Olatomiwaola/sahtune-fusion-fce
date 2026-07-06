"""Export package (JSONL) + JSON integrity manifest (FCE-REQ-EXP-001).

JSONL + manifest is the documented format at TRL 1-3 (CSV/PDF are design-only, no
three-format implementation claim). The caller emits an export-class audit record
whose event_detail carries the manifest's own sha-256, so the chain binds manifest
content (FCE-DR-AUD-001).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .chain import load_records
from .records import _is_semver


@dataclass(frozen=True)
class ExportResult:
    package_dir: Path
    manifest: dict
    manifest_sha256: str
    jsonl_path: Path
    manifest_path: Path


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def export_package(audit_path, out_dir, clock, package_id: str, format_version: str = "1") -> ExportResult:
    audit_path = Path(audit_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = audit_path.read_bytes()
    records = load_records(audit_path)
    if not records:
        raise ValueError("cannot export an empty chain")

    jsonl_path = out_dir / "audit.jsonl"
    jsonl_path.write_bytes(raw)

    bundle_versions = sorted({
        r["policy_bundle_version"] for r in records if _is_semver(r.get("policy_bundle_version"))
    })

    manifest = {
        "package_id": package_id,
        "created": clock.now,
        "format_version": format_version,
        "record_count": len(records),
        "first_event_id": records[0]["audit_event_id"],
        "last_event_id": records[-1]["audit_event_id"],
        "chain_head_hash": records[-1]["record_content_hash"],
        "files": [{"file": "audit.jsonl", "sha256": _sha256_bytes(raw)}],
        "bundle_versions_referenced": bundle_versions,
        "segment_links": [],
    }
    manifest_bytes = json.dumps(manifest, sort_keys=True, ensure_ascii=False).encode("utf-8")
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_bytes(manifest_bytes)
    manifest_sha256 = _sha256_bytes(manifest_bytes)

    return ExportResult(out_dir, manifest, manifest_sha256, jsonl_path, manifest_path)


def recompute_manifest_sha256(manifest_path) -> str:
    return _sha256_bytes(Path(manifest_path).read_bytes())
