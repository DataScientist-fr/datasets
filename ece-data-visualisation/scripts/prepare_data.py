#!/usr/bin/env python3
"""Fetch and verify two immutable teaching snapshots. Run from repository root."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UBER_COMMIT = "63bb878b76f47f69b4527d50af57aac26dead983"
SOURCES = {
    "uber_apr2014": {
        "url": f"https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/{UBER_COMMIT}/uber-trip-data/uber-raw-data-apr14.csv",
        "path": "uber/uber_apr2014.csv",
        "kind": "csv",
    },
    "green_taxi_2025_01": {
        "url": "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-01.parquet",
        "path": "nyc_trips/green_taxi_2025_01.csv",
        "kind": "parquet",
    },
}
GREEN_FIELDS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "trip_distance",
    "total_amount",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
]


def download(url: str, destination: Path) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "DataScientist-fr-ECE-DataViz/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        if int(getattr(response, "status", 200)) != 200:
            raise RuntimeError(f"HTTP error for {url}: {response.status}")
        with destination.open("wb") as output:
            shutil.copyfileobj(response, output)
    if destination.stat().st_size < 10_000 or destination.stat().st_size > 80_000_000:
        raise ValueError(f"Unexpected source size: {destination.stat().st_size}")
    with destination.open("rb") as file:
        head = file.read(512).lstrip().lower()
    if head.startswith((b"<", b"{")) or b"blobnotfound" in head:
        raise ValueError("HTML/XML/JSON error payload instead of dataset")
    return {"source_bytes": destination.stat().st_size, "source_sha256": sha256(destination)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prepare() -> None:
    import pyarrow.parquet as pq
    import pandas as pd

    with tempfile.TemporaryDirectory() as temp:
        tempdir = Path(temp)
        manifest = {"version": 1, "datasets": {}}
        for key, info in SOURCES.items():
            source = tempdir / ("source.parquet" if info["kind"] == "parquet" else "source.csv")
            hashes = download(info["url"], source)
            destination = ROOT / info["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            if info["kind"] == "csv":
                with source.open(newline="", encoding="utf-8-sig") as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    if header != ["Date/Time", "Lat", "Lon", "Base"]:
                        raise ValueError(f"Unexpected Uber CSV schema: {header}")
                    rows = sum(1 for _ in reader)
                if rows != 564516:
                    raise ValueError(f"Unexpected Uber row count: {rows}")
                shutil.copy2(source, destination)
            else:
                with source.open("rb") as f:
                    if f.read(4) != b"PAR1":
                        raise ValueError("Green Taxi source is not a Parquet file")
                parquet = pq.ParquetFile(source)
                columns = set(parquet.schema_arrow.names)
                missing = set(GREEN_FIELDS) - columns
                if missing:
                    raise ValueError(f"Missing Green Taxi fields: {sorted(missing)}")
                table = pq.read_table(source, columns=GREEN_FIELDS)
                rows = table.num_rows
                if rows < 1000:
                    raise ValueError(f"Too few Green Taxi trips: {rows}")
                df = table.to_pandas()
                df.to_csv(destination, index=False, date_format="%Y-%m-%d %H:%M:%S")
                with destination.open("r", newline="", encoding="utf-8") as f:
                    if next(csv.reader(f)) != GREEN_FIELDS:
                        raise ValueError("Green Taxi export header does not match specification")
            if destination.stat().st_size > 49_000_000:
                raise ValueError("Derived file too large for ordinary GitHub storage")
            manifest["datasets"][key] = {
                "source_url": info["url"],
                "source_kind": info["kind"],
                "file": info["path"],
                "rows": rows,
                "sha256": sha256(destination),
                "bytes": destination.stat().st_size,
                **hashes,
            }
        (ROOT / "MANIFEST.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    prepare()
