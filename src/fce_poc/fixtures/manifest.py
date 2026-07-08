"""Stage 1 — source manifest (GDR-001/-002/-003).

Values from disk not memory: sha-256 and record counts are recomputed from the raw
payloads; the OSD-01 licence value is extracted as a verbatim-CONTIGUOUS span of the
R4 page's visible text (STOP if the span is not found contiguously); the OSD-04
licence is extracted from the Stage-A registry page. Download-phase recording values
(query URLs/body, endpoints, access timestamps, HTTP status) are embedded from the
M6-05r recording. The framing sentence is verbatim; the acoustic_like disclosure is
read from docs/09 v1.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RAW = REPO / "data" / "raw"
DOCS09 = REPO / "docs" / "09_synthetic-dataset-plan.md"

FRAMING_SENTENCE = (
    "USGS and Sentinel-2 STAC data are reproducible public-source anchors for a "
    "TRL 1-3 compliance-engine proof of concept — never operational or "
    "CAF-equivalent data."
)

# Download-phase recording (M6-05r + download outputs). Hashes/counts are recomputed
# from disk below and cross-checked; these are the query/endpoint/time/status facts.
RECORDING = {
    "OSD-01": {
        "source_page": "https://earthquake.usgs.gov/fdsnws/event/1/",
        "api_endpoint": "https://earthquake.usgs.gov/fdsnws/event/1/query",
        "http_method": "GET",
        "query_params": {
            "format": "geojson", "starttime": "2025-06-01T00:00:00Z",
            "endtime": "2025-08-31T23:59:59Z", "minlatitude": "35.0",
            "maxlatitude": "37.5", "minlongitude": "-122.0", "maxlongitude": "-118.0",
            "minmagnitude": "1.5", "orderby": "time-asc", "limit": "200",
        },
        "access_timestamp": "2026-07-08T02:46:40Z",
        "http_status": 200,
        "raw_file": "osd01_usgs_events.geojson",
    },
    "OSD-04": {
        "source_page": "https://registry.opendata.aws/sentinel-2-l2a-cogs/",
        "api_endpoint": "https://earth-search.aws.element84.com/v1/search",
        "http_method": "POST",
        "query_body": {
            "collections": ["sentinel-2-l2a"], "bbox": [-122.0, 35.0, -118.0, 37.5],
            "datetime": "2025-06-01T06:49:28Z/2025-07-24T23:41:17Z", "limit": 100,
        },
        "collection": "sentinel-2-l2a",
        "access_timestamp": "2026-07-08T09:45:11Z",
        "http_status": 200,
        "raw_file": "osd04_stageB2_stac_items.geojson",
        "query_role": "ACTIVE (corrective B2 — datetime slice-aligned to the USGS effective span)",
    },
}

# Original Stage-B query retained as SUPERSEDED (M6-06b B2-3). Reason recorded verbatim.
SUPERSESSION_REASON = (
    "Superseded 2026-07-08: the original Stage-B slice (Earth Search default "
    "datetime-descending, limit=100) sampled 2025-08-22 onward while the USGS "
    "time-asc limit=200 slice ended ~1 month earlier — zero temporal candidate "
    "pairs (876 spatial-only). Corrective query constrains the STAC datetime to "
    "the USGS effective span read from the downloaded events file, guaranteeing "
    "slice alignment mechanically. Selection rule: earliest-200 USGS events define "
    "the span; STAC items within that span. No policy evaluation had consumed any "
    "data; no split existed. Slice-alignment correction, not source or result selection."
)
SUPERSEDED_STAGE_B = {
    "api_endpoint": "https://earth-search.aws.element84.com/v1/search",
    "http_method": "POST",
    "query_body": {"collections": ["sentinel-2-l2a"], "bbox": [-122.0, 35.0, -118.0, 37.5],
                   "datetime": "2025-06-01T00:00:00Z/2025-08-31T23:59:59Z", "limit": 100},
    "access_timestamp": "2026-07-08T02:59:37Z", "http_status": 200,
    "raw_file": "osd04_stageB_stac_items.geojson", "query_role": "SUPERSEDED",
}


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _visible_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?is)<script.*?</script>", " ", raw)
    t = re.sub(r"(?is)<style.*?</style>", " ", t)
    t = re.sub(r"(?is)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def osd01_licence_from_r4() -> str:
    """Verbatim-CONTIGUOUS span from the R4 page: public-domain core (+ non-USGS
    caveat) through the credit-request citation example. STOP (raise) if not found
    as one contiguous substring of the R4 visible text."""
    text = _visible_text(RAW / "osd01_licence_R4.html")
    start = text.find("USGS-authored or produced data")
    end_anchor = "(if the photographer/artist is known)"
    end = text.find(end_anchor)
    if start == -1 or end == -1 or end < start:
        raise ValueError("GDR-002: OSD-01 licence span not found contiguously in R4 — STOP")
    span = text[start:end + len(end_anchor)]
    if span not in text:
        raise ValueError("GDR-002: OSD-01 licence value is not verbatim-continuous R4 text — STOP")
    return span


def osd04_licence_from_stage_a() -> tuple[str, str]:
    """Sentinel-2 licence line + terms URL, from the Stage-A registry page."""
    text = _visible_text(RAW / "osd04_stageA_registry.html")
    m = re.search(r"Access to Sentinel data is free.*?Terms and Conditions", text)
    statement = m.group(0) if m else ""
    raw = (RAW / "osd04_stageA_registry.html").read_text(encoding="utf-8", errors="replace")
    tm = re.search(r'href="(https://scihub\.copernicus\.eu[^"]*TermsConditions)"', raw)
    terms_url = tm.group(1) if tm else ""
    if not statement or not terms_url:
        raise ValueError("GDR-002: OSD-04 licence statement/terms URL not found in Stage-A page — STOP")
    return statement, terms_url


def _acoustic_disclosure() -> str:
    """The acoustic_like assignment-basis cell from the docs/09 v1 fixture-source table."""
    for line in DOCS09.read_text(encoding="utf-8").splitlines():
        if line.startswith("| USGS seismic events (OSD-01)"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            return cells[2]
    raise ValueError("acoustic_like disclosure row not found in docs/09 v1 — STOP")


def _record_count(raw_file: str) -> int:
    return len(json.loads((RAW / raw_file).read_text(encoding="utf-8"))["features"])


def build_source_manifest() -> dict:
    r1 = _sha256_file(RAW / "osd01_licence_R1.html")
    r2 = _sha256_file(RAW / "osd01_licence_R2.html")
    r3 = _sha256_file(RAW / "osd01_licence_R3.html")
    r4 = _sha256_file(RAW / "osd01_licence_R4.html")
    osd01_licence = osd01_licence_from_r4()
    s2_statement, s2_terms = osd04_licence_from_stage_a()
    stage_a_hash = _sha256_file(RAW / "osd04_stageA_registry.html")

    usgs = dict(RECORDING["OSD-01"])
    usgs.update({
        "fixture_modality": "acoustic_like",
        "fixture_modality_disclosure": _acoustic_disclosure(),
        "raw_file_sha256": _sha256_file(RAW / usgs["raw_file"]),
        "record_count": _record_count(usgs["raw_file"]),
        "licence_note": osd01_licence,
        "licence_provenance_chain": [
            {"hop": "R1", "url": "https://earthquake.usgs.gov/fdsnws/event/1/", "sha256": r1,
             "role": "API base page; links to Legal"},
            {"hop": "R2", "url": "https://www.usgs.gov/policies-and-notices", "sha256": r2,
             "role": "policies index; links onward"},
            {"hop": "R3", "url": "https://www.usgs.gov/information-policies-and-instructions", "sha256": r3,
             "role": "information-policies index; links to Copyrights and Credits"},
            {"hop": "R4", "url": "https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits",
             "sha256": r4, "role": "verbatim licence/credit statement source"},
        ],
    })

    s2 = dict(RECORDING["OSD-04"])
    s2.update({
        "fixture_modality": "eo_ir",
        "raw_file_sha256": _sha256_file(RAW / s2["raw_file"]),
        "record_count": _record_count(s2["raw_file"]),
        "licence_note": s2_statement,
        "licence_terms_url": s2_terms,
        "endpoint_resolution_trail": {
            "stage_a_url": "https://registry.opendata.aws/sentinel-2-l2a-cogs/",
            "stage_a_sha256": stage_a_hash,
            "documented_stac_endpoint": "https://earth-search.aws.element84.com/v1",
            "confirmed_hostname": "earth-search.aws.element84.com",
        },
        "superseded_query": {
            **SUPERSEDED_STAGE_B,
            "raw_file_sha256": _sha256_file(RAW / SUPERSEDED_STAGE_B["raw_file"]),
            "record_count": _record_count(SUPERSEDED_STAGE_B["raw_file"]),
            "reason": SUPERSESSION_REASON,
        },
    })

    return {
        "_framing": FRAMING_SENTENCE,
        "schema_note": "M6 Sprint 12 source manifest (GDR-001/-002/-003). No raw payloads committed; data/raw/ is git-ignored.",
        "global": {
            "aoi_bbox": {"minlongitude": -122.0, "minlatitude": 35.0, "maxlongitude": -118.0, "maxlatitude": 37.5},
            "time_window": "2025-06-01T00:00:00Z/2025-08-31T23:59:59Z",
            "split_seed": 12918724377571503927,
            "split_key": "sha-256 over <stable_source_record_id>:<seed>",
        },
        "sources": {"OSD-01": usgs, "OSD-04": s2},
    }


def validate_manifest(m: dict) -> None:
    """GDR-001/-002/-003: each source must carry hash, record count/query params, and
    a licence note; missing any aborts the build."""
    for sid, s in m["sources"].items():
        if not s.get("raw_file_sha256"):
            raise ValueError(f"GDR-001: source {sid} missing raw_file_sha256 — abort")
        if not (s.get("query_params") or s.get("query_body")):
            raise ValueError(f"GDR-003: source {sid} missing query params/body — abort")
        if s.get("record_count") is None:
            raise ValueError(f"GDR-003: source {sid} missing record_count — abort")
        if not s.get("licence_note"):
            raise ValueError(f"GDR-002: source {sid} missing licence note — abort (source unapproved)")
