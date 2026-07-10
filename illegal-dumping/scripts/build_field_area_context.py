"""Precompute area context around each field-program site.

For every site in data/processed/field_program_nb06.csv, export all
report-stacks (exact-coordinate aggregations of dumping reports) within
350m, plus per-site diagnostics of how "address-stacked" the site itself
is. Lets notebook 07 show the surrounding micro-area without loading the
full 384MB dataset.

Outputs:
  data/processed/field_area_stacks.csv   (site_id, lat, lon, n_reports)
  data/processed/field_site_diagnostics.csv

Usage (from illegal-dumping/): python scripts/build_field_area_context.py
"""

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent  # illegal-dumping/
SHARED = ROOT.parent / "shared" / "datasets"

raw = pd.read_csv(SHARED / "raw/myla311_cases_2026.csv", low_memory=False)
INTAKE = {"Information-Only", "Feedback", "Program Research"}
DEAD = {"Cancelled", "Potential Duplicate", "Duplicate Confirm"}
op = raw[~raw["RequestType"].isin(INTAKE) & ~raw["Status"].isin(DEAD)]
op = op[~op["ResolutionCode"].fillna("").str.startswith(("DUP-", "B-Duplicated", "CDR-"))].copy()
op["created"] = pd.to_datetime(op["CreatedDate"], format="mixed")
op = op[op["created"] < "2026-07-01"]
il = op[op["RequestType"] == "Illegal Dumping Item Pickup"].dropna(subset=["Latitude", "Longitude"])
il = il[il["Latitude"].between(33.60, 34.40) & il["Longitude"].between(-118.75, -118.10)].copy()

# aggregate to exact-coordinate stacks (address-geocoded reports pile up here)
il["lat_r"], il["lon_r"] = il["Latitude"].round(6), il["Longitude"].round(6)
stacks = (il.groupby(["lat_r", "lon_r"])
          .agg(n_reports=("CaseNumber", "size"),
               self_service=("RequestSource", lambda s: (s == "Self Service").mean()))
          .reset_index())
sg = gpd.GeoDataFrame(stacks, geometry=gpd.points_from_xy(stacks["lon_r"], stacks["lat_r"]),
                      crs="EPSG:4326").to_crs("EPSG:32611")
SX, SY = sg.geometry.x.values, sg.geometry.y.values

program = pd.read_csv(ROOT / "data/processed/field_program_nb06.csv")
program["site_id"] = [f"A{i+1}" for i in range(10)] + [f"B{i+1}" for i in range(9)]
pg = gpd.GeoDataFrame(program, geometry=gpd.points_from_xy(program["lon"], program["lat"]),
                      crs="EPSG:4326").to_crs("EPSG:32611")

area_rows, diag_rows = [], []
for _, site in pg.iterrows():
    d = np.hypot(SX - site.geometry.x, SY - site.geometry.y)
    near = sg[d <= 350].copy()
    near["site_id"] = site["site_id"]
    area_rows.append(near[["site_id", "lat_r", "lon_r", "n_reports"]])

    inner = sg[d <= 20]
    ring = sg[(d > 20) & (d <= 250)]
    diag_rows.append({
        "site_id": site["site_id"],
        "address": site["address"],
        "site_reports": int(inner["n_reports"].sum()),
        "site_distinct_coords": len(inner),
        "site_modal_stack": int(inner["n_reports"].max()) if len(inner) else 0,
        "site_self_service_pct": round(
            float((inner["self_service"] * inner["n_reports"]).sum()
                  / max(inner["n_reports"].sum(), 1)) * 100),
        "ring250_reports": int(ring["n_reports"].sum()),
        "ring250_stacks": len(ring),
        "site_share_of_area": round(
            float(inner["n_reports"].sum()
                  / max(inner["n_reports"].sum() + ring["n_reports"].sum(), 1)) * 100),
    })

pd.concat(area_rows).rename(columns={"lat_r": "lat", "lon_r": "lon"}).to_csv(
    ROOT / "data/processed/field_area_stacks.csv", index=False)
pd.DataFrame(diag_rows).to_csv(ROOT / "data/processed/field_site_diagnostics.csv", index=False)
print("wrote field_area_stacks.csv and field_site_diagnostics.csv")
print(pd.DataFrame(diag_rows).to_string(index=False))
