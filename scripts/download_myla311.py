"""Download MyLA311 data from the LA Open Data Portal into data/raw/.

Usage:
    python scripts/download_myla311.py            # current-system 2026 data
    python scripts/download_myla311.py 2024       # any year in DATASETS

The portal (data.lacity.org) runs on Socrata, which exposes every dataset
as a full CSV export at a stable URL — no API key, no pagination, no
clicking through the website. Re-running overwrites the file with the
latest daily snapshot.

NOTE: LA migrated its 311 system in late 2025. Datasets through 2025 use
the old "Service Request Data" schema; "Cases" datasets (2026 onward, plus
the Mar-Dec 2025 transition dataset) use the new Salesforce-based schema
with different column names. The two schemas are NOT directly comparable
without mapping work.
"""

import sys
import urllib.request
from pathlib import Path

# Socrata dataset IDs, from https://data.lacity.org (search "MyLA311")
DATASETS = {
    # New system ("MyLA311 Cases", Salesforce schema)
    "2026": ("2cy6-i7zn", "myla311_cases_2026.csv"),
    "2025-cases": ("73a2-6ar5", "myla311_cases_mar_dec_2025.csv"),
    # Old system ("MyLA311 Service Request Data"; 2025 ends Nov 3, 2025)
    "2025": ("h73f-gn57", "myla311_requests_2025.csv"),
    "2024": ("b7dx-7gc3", "myla311_requests_2024.csv"),
    "2023": ("4a4x-mna2", "myla311_requests_2023.csv"),
    "2022": ("i5ke-k6by", "myla311_requests_2022.csv"),
    "2021": ("97z7-y5bt", "myla311_requests_2021.csv"),
    "2020": ("rq3b-xjk8", "myla311_requests_2020.csv"),
    "2019": ("pvft-t768", "myla311_requests_2019.csv"),
    "2018": ("h65r-yf5i", "myla311_requests_2018.csv"),
    "2017": ("eq98-9f8w", "myla311_requests_2017.csv"),
    "2016": ("ndkd-k878", "myla311_requests_2016.csv"),
    "2015": ("ms7h-a45h", "myla311_requests_2015.csv"),
}

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def download(key: str) -> Path:
    dataset_id, filename = DATASETS[key]
    url = f"https://data.lacity.org/api/views/{dataset_id}/rows.csv?accessType=DOWNLOAD"
    dest = RAW_DIR / filename

    print(f"Downloading {key} ({dataset_id}) -> {dest}")
    with urllib.request.urlopen(url) as response, open(dest, "wb") as f:
        downloaded = 0
        while chunk := response.read(1024 * 1024):
            f.write(chunk)
            downloaded += len(chunk)
            print(f"\r  {downloaded / 1e6:,.0f} MB", end="", flush=True)
    print(f"\nDone: {dest.stat().st_size / 1e6:,.1f} MB")
    return dest


def download_boundaries() -> Path:
    """LA City Council district boundaries (2021 adopted), GeoJSON."""
    url = "https://data.lacity.org/api/geospatial/pxeu-7j74?method=export&format=GeoJSON"
    dest = RAW_DIR / "la_council_districts_2021.geojson"
    print(f"Downloading council district boundaries -> {dest}")
    urllib.request.urlretrieve(url, dest)
    print(f"Done: {dest.stat().st_size / 1e6:,.1f} MB")
    return dest


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "2026"
    if key == "boundaries":
        download_boundaries()
    elif key not in DATASETS:
        sys.exit(f"Unknown dataset {key!r}. Options: {', '.join(DATASETS)}, boundaries")
    else:
        download(key)
