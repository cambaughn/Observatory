# Sources — Illegal Dumping

Datasets, documents, and external references this domain draws on.

## Data

- **MyLA311 service request cases (2026 "Cases" system)** — the primary
  dataset. Documentation: [shared/references/myla311.md](../shared/references/myla311.md)
  and [shared/references/myla311_operational_model.md](../shared/references/myla311_operational_model.md).
  Re-fetch: `python shared/scripts/download_myla311.py 2026`. File:
  `shared/datasets/raw/myla311_cases_2026.csv`.
- **LA neighborhood council boundaries** and **council district boundaries**
  (GeoJSON, LA Open Data / geohub) — `shared/datasets/raw/`, fetched via
  `python shared/scripts/download_myla311.py boundaries`.
- **2020 Census block population**, aggregated to neighborhood councils —
  `shared/datasets/processed/nc_population_2020.csv`, built by
  `shared/scripts/build_nc_population_2020.py`.
- **Domain-derived datasets** (`data/processed/`, gitignored): field
  candidate sites (notebook 05), field program sites (notebook 06), area
  stacks + site diagnostics (`scripts/build_field_area_context.py`).

## Institutional / web references

- LASAN Livability Services Division (CARE/CARE+):
  sanitation.lacity.gov/livability — report-only encampment workflow (F6, F15)
- LA Office of Community Beautification: laocb.org — graffiti/cleanup
  contractor network (F5)
- LAist, ["Mind the mess: Koreatown leads LA in illegal dumping reports"](https://laist.com/news/mind-the-mess-koreatown-leads-la-in-illegal-dumping-reports)
  — independent confirmation of the #1 site; reporter outreach tracked as RT-10
- LAist, ["LA to acquire vacant lot for Koreatown pocket park"](https://laist.com/news/la-to-acquire-vacant-lot-koreatown-new-pocket-park-plan)
  — CD10 corridor activity relevant to the 4th & New Hampshire case (F20, RT-02)

## People / access (prospective)

- LASAN yard supervisors (East Valley / West Valley) — crew policy questions
  (RT-04, RT-05)
- CD10 field deputy; LSD/CARE+ lead — 4th & New Hampshire intervention (RT-02)
- Wilshire Center BID — independent cleanliness observations (research
  methods, method 5)
- ITA — data dictionary, reporter-level dedup, internal chronic-site lists
  (O5, RT-06, RT-11)
