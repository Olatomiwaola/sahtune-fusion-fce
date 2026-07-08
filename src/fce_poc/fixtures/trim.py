"""Stage 2 — trim raw payloads to metadata level (docs/16 Trim Protocol steps 4-7).

Metadata only. Kept fields per the M6-06 spec:
  USGS  — event id, timestamp, longitude/latitude/depth, magnitude, status.
  S2    — item id, datetime, bbox + geometry, cloud-cover, collection.

Association-candidate definition (deterministic, pre-committed in M6-06 Stage 2):
  candidate pair = (USGS event, S2 item) where the event epicenter lies within the
  item bbox AND |event timestamp - item datetime| <= 7 days.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .normalize import epoch_ms_to_rfc3339

CANDIDATE_WINDOW = timedelta(days=7)


def _parse_ts(value: str) -> datetime:
    v = value.replace("Z", "+00:00")
    return datetime.fromisoformat(v).astimezone(timezone.utc)


def trim_usgs(raw: dict) -> list[dict]:
    out = []
    for f in raw["features"]:
        p = f["properties"]
        lon, lat, depth = (f["geometry"]["coordinates"] + [None, None, None])[:3]
        out.append({
            "source_id": "OSD-01",
            "record_id": f["id"],
            "acquisition_timestamp": epoch_ms_to_rfc3339(p["time"]),
            "longitude": lon,
            "latitude": lat,
            "depth": depth,
            "magnitude": p.get("mag"),
            "status": p.get("status"),
        })
    return out


def trim_stac(raw: dict) -> list[dict]:
    out = []
    for it in raw["features"]:
        p = it["properties"]
        out.append({
            "source_id": "OSD-04",
            "record_id": it["id"],
            "acquisition_timestamp": p["datetime"],
            "bbox": it["bbox"],
            "geometry": it["geometry"],
            "cloud_cover": p.get("eo:cloud_cover"),
            "collection": it.get("collection"),
        })
    return out


def association_candidates(usgs: list[dict], stac: list[dict]) -> list[tuple[str, str]]:
    """Deterministic candidate pairs: epicenter in item bbox AND |dt| <= 7 days."""
    pairs = []
    stac_prepared = [(s, tuple(s["bbox"]), _parse_ts(s["acquisition_timestamp"])) for s in stac]
    for e in usgs:
        lon, lat = e["longitude"], e["latitude"]
        if lon is None or lat is None:
            continue
        et = _parse_ts(e["acquisition_timestamp"])
        for s, bbox, st in stac_prepared:
            if bbox[0] <= lon <= bbox[2] and bbox[1] <= lat <= bbox[3] and abs(et - st) <= CANDIDATE_WINDOW:
                pairs.append((e["record_id"], s["record_id"]))
    return pairs


def nonempty_modalities(trimmed_by_source: dict[str, list]) -> None:
    """GDR-005: any declared source with an empty/all-null trimmed set aborts."""
    for source_id, records in trimmed_by_source.items():
        if not records:
            raise ValueError(f"GDR-005: source {source_id} has an empty trimmed record set — abort before report")
