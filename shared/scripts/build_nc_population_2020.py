"""Build 2020 Census population per Neighborhood Council.

Produces shared/datasets/processed/nc_population_2020.csv (NAME, pop2020).

Method: sum 2020 Census block populations (POP20) into certified NC
polygons, assigning each block by its internal point. Validation: LA
County block total equals the official 2020 count (10,014,009); the sum
over all 99 NCs is ~3.82M vs the official city total 3.90M (the gap is
city territory outside NC boundaries plus boundary/centroid effects).

Why not the Census API: block-level queries now require an API key. The
TIGER2020 state block shapefile carries POP20 directly, no key needed.
The 382MB state download is the one heavy step; it is cached in shared/datasets/raw/
and can be deleted after the CSV is built.

Usage: python scripts/build_nc_population_2020.py
"""

import urllib.request
from pathlib import Path

import geopandas as gpd

RAW = Path(__file__).resolve().parent.parent / "datasets" / "raw"
OUT = Path(__file__).resolve().parent.parent / "datasets" / "processed" / "nc_population_2020.csv"

NC_URL = ("https://maps.lacity.org/lahub/rest/services/Boundaries/MapServer/18/"
          "query?where=1%3D1&outFields=*&outSR=4326&f=geojson")
BLOCKS_URL = "https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/tl_2020_06_tabblock20.zip"

nc_path = RAW / "la_neighborhood_councils.geojson"
blocks_path = RAW / "tl_2020_06_tabblock20.zip"

if not nc_path.exists():
    print("Downloading certified NC boundaries...")
    urllib.request.urlretrieve(NC_URL, nc_path)
if not blocks_path.exists():
    print("Downloading CA 2020 block shapefile (382 MB, one-time)...")
    urllib.request.urlretrieve(BLOCKS_URL, blocks_path)

print("Reading blocks (attribute-only)...")
blocks = gpd.read_file(
    blocks_path,
    columns=["GEOID20", "COUNTYFP20", "POP20", "INTPTLAT20", "INTPTLON20"],
    ignore_geometry=True,
)
la = blocks[blocks["COUNTYFP20"] == "037"].copy()
assert la["POP20"].sum() == 10_014_009, "LA County total should match official 2020 count"

pts = gpd.GeoDataFrame(
    la,
    geometry=gpd.points_from_xy(la["INTPTLON20"].astype(float), la["INTPTLAT20"].astype(float)),
    crs="EPSG:4326",
)
nc = gpd.read_file(nc_path)[["NAME", "geometry"]]
joined = gpd.sjoin(pts, nc, predicate="within", how="inner")
nc_pop = joined.groupby("NAME")["POP20"].sum().sort_values(ascending=False).rename("pop2020")

OUT.parent.mkdir(exist_ok=True)
nc_pop.to_csv(OUT)
print(f"Wrote {OUT}: {nc_pop.size} NCs, total {nc_pop.sum():,}")
