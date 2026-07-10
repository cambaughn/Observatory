"""Generate standalone HTML field maps into field-notes/maps/.

Inputs: data/processed/field_program_nb06.csv (site coordinates + stats,
produced by notebook 06). No analysis here - presentation only.

Usage (from illegal-dumping/): python scripts/build_field_maps.py
"""

from pathlib import Path

import folium
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "field-notes" / "maps"
OUT.mkdir(exist_ok=True)

program = pd.read_csv(ROOT / "data" / "processed" / "field_program_nb06.csv")
A = program[program["section"] == "A_citywide"].reset_index(drop=True)
B = program[program["section"] == "B_valley"].reset_index(drop=True)

# Valley visit order (field guide section B / itinerary), keyed by street number
ROUTE_ORDER = ["17808", "17900", "5130", "14102", "9404", "13036", "5767", "4176", "14359"]


def gmaps(lat, lon):
    return f"https://www.google.com/maps/search/?api=1&query={lat:.6f},{lon:.6f}"


def popup(r):
    return folium.Popup(
        f"<b>{r['address']}</b><br>{r['neighborhood']}<br>"
        f"reports: {r['reports']} | median gap: {r['median_gap_days']} d<br>"
        f"<i>{r['why_interesting']}</i><br>"
        f"<a href='{gmaps(r['lat'], r['lon'])}' target='_blank'>Open in Google Maps</a>",
        max_width=300,
    )


# --- 1. Valley field route: numbered stops connected in visit order ---
routed = pd.concat(
    [B[B["address"].str.startswith(num)] for num in ROUTE_ORDER]
).reset_index(drop=True)
assert len(routed) == len(B), "route order must cover every Valley site"

m = folium.Map(location=[34.19, -118.44], zoom_start=12, tiles="cartodbpositron")
folium.PolyLine(routed[["lat", "lon"]].values.tolist(),
                color="royalblue", weight=3, opacity=0.6, dash_array="6").add_to(m)
for i, r in routed.iterrows():
    folium.CircleMarker([r["lat"], r["lon"]], radius=13, color="royalblue",
                        fill=True, fill_color="white", fill_opacity=1,
                        popup=popup(r)).add_to(m)
    folium.map.Marker(
        [r["lat"], r["lon"]],
        icon=folium.DivIcon(html=f"<div style='font-size:11px;font-weight:bold;"
                                 f"color:royalblue;text-align:center;width:26px;"
                                 f"margin-left:-13px;margin-top:-7px'>{i + 1}</div>"),
    ).add_to(m)
m.save(OUT / "valley_route.html")

# --- 2. Koreatown investigation area: the paired New Hampshire sites ---
pair = A[A["address"].str.contains("NEW HAMPSHIRE")].reset_index(drop=True)
assert len(pair) == 2
quiet = pair[pair["why_interesting"].str.contains("QUIET")].iloc[0]
active = pair[~pair["why_interesting"].str.contains("QUIET")].iloc[0]

m = folium.Map(location=[(quiet["lat"] + active["lat"]) / 2,
                         (quiet["lon"] + active["lon"]) / 2],
               zoom_start=16, tiles="cartodbpositron")
for r, color, label in [(quiet, "gray", "WENT QUIET Apr 17 — what changed here?"),
                        (active, "crimson", "still active — the control")]:
    folium.CircleMarker([r["lat"], r["lon"]], radius=12, color=color, weight=3,
                        fill=True, fill_opacity=0.7, popup=popup(r),
                        tooltip=f"{r['address']} — {label}").add_to(m)
# the rings used in the migration analysis (nb06 postscript): 300m and 800m
for radius, dash in [(300, None), (800, "8")]:
    folium.Circle([quiet["lat"], quiet["lon"]], radius=radius, color="#888",
                  weight=1.5, fill=False, dash_array=dash,
                  tooltip=f"{radius}m ring (migration check: dumping stayed flat here)").add_to(m)
m.save(OUT / "koreatown.html")

# --- 3. Citywide planning map: all top 10 sites ---
m = folium.Map(location=[34.04, -118.32], zoom_start=11, tiles="cartodbpositron")
for _, r in A.iterrows():
    folium.CircleMarker([r["lat"], r["lon"]], radius=9, color="crimson", weight=2,
                        fill=True, fill_opacity=0.85, popup=popup(r),
                        tooltip=r["address"]).add_to(m)
m.save(OUT / "citywide.html")

print("wrote:", *[p.name for p in sorted(OUT.glob("*.html"))])
