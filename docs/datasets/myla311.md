# Dataset Reference: MyLA311

Long-term reference for the City of LA 311 service request data.
Last reviewed: 2026-07-06.

## Source

- **Publisher:** City of Los Angeles, Information Technology Agency (ITA)
- **Portal:** [data.lacity.org](https://data.lacity.org) (Socrata platform)
- **Primary dataset (current):** [MyLA311 Cases 2026](https://data.lacity.org/City-Infrastructure-Service-Requests/MyLA311-Cases-2026/2cy6-i7zn) — dataset id `2cy6-i7zn`
- **Update cadence:** daily (data observed running up to within hours of download time)
- **License:** Creative Commons CC0 1.0 (public domain — no usage restrictions)

## The 2025 system migration (important)

LA replaced its 311 platform with a Salesforce-based system in late 2025.
This split the data into two eras:

| Era | Datasets | Naming | Notes |
|---|---|---|---|
| 2015 – Nov 2025 | one per year (`MyLA311 Service Request Data <year>`) | ~12 request types | 2025 dataset **ends Nov 3, 2025** (~423K rows) |
| Mar 2025 – present | `MyLA311 Cases March 2025 to December 2025` (`73a2-6ar5`), `MyLA311 Cases 2026` (`2cy6-i7zn`) | 62 request types, new column names | the Mar–Dec 2025 dataset overlaps the old system during phased rollout |

Consequences:

- **Cross-era trend analysis requires schema + category mapping.** The 62 new
  request types do not map 1:1 onto the ~12 old ones.
- Late-2025 coverage is awkward: the old dataset stops Nov 3; the transition
  dataset overlaps Mar–Nov. Deduplication across the two is an open question.
- Case volume jumped: ~423K rows in 10 months of old-system 2025 vs ~1.21M rows
  in 6 months of 2026. Unclear how much is real volume vs the new system
  logging more record types (e.g. `Information-Only`). Do not naively compare.

## Download method

Reproducible via [`scripts/download_myla311.py`](../../scripts/download_myla311.py):

```
python scripts/download_myla311.py            # 2026 (current)
python scripts/download_myla311.py 2024       # any historical year
```

Uses Socrata's full-CSV export endpoint
(`https://data.lacity.org/api/views/<id>/rows.csv?accessType=DOWNLOAD`) —
no API key, no pagination. The same data is also queryable via the SODA API
(`/resource/<id>.json` with SQL-ish `$select`/`$where` params), useful later
if we want incremental refresh instead of full re-download.

Files land in `data/raw/` (gitignored). 2026 file: `myla311_cases_2026.csv`,
~384 MB, 1,209,648 rows at download time.

## Schema summary (2026 "Cases" era)

34 columns. Full column-by-column commentary lives in
[`notebooks/01_acquire_and_understand_data.ipynb`](../../notebooks/01_acquire_and_understand_data.ipynb).

- **Identity/lifecycle:** `CaseNumber`, `CreatedDate`, `UpdatedDate`,
  `ClosedDate`, `ServiceDate`, `DateServiceRendered`, `Status`, `ActionTaken`,
  `ReasonCode`, `ResolutionCode`
- **What/who:** `RequestType` (62 values), `RequestSource`,
  `CreatedByUserOrganization`, `Anonymous`, `Owner`, `AssignTo`
- **Where:** `Address` + components, `ZipCode`, `Latitude`/`Longitude`,
  `Location`, `TBMPage`/`TBMColumn`/`TBMRow` (legacy Thomas Guide refs),
  `APC` (7), `CD`/`CDMember` (15 + a `0` bucket), `NC`/`NCName` (99),
  `PolicePrecinct`

Note: the CSV export uses friendly headers (`RequestType`); the SODA API
returns raw Salesforce field names (`type`, `department_name__c`,
`locator_council_district`). Same data, two naming schemes.

## Important caveats

1. **Coordinates contain junk.** ~5% missing, and non-missing values include
   impossible points (lat −38 to +56, lon −158 to +174). Must bound-filter to
   the LA area before any mapping.
2. **`Owner` is messy.** 96 distinct values with duplicates
   (`LASAN LSD` / `LASAN - LSD`), individual staff names, and a literal
   `TEST XX`. Needs normalization before department-level analysis.
3. **`Information-Only` is ~23% of all cases** — questions, not maintenance
   requests. Every operational analysis needs an explicit include/exclude
   decision.
4. **`Closed` ≠ fixed.** Status describes case handling, not real-world
   outcomes. `ResolutionCode` vocabulary not yet studied.
5. **Near-empty fields:** `Location` (100%), `DateServiceRendered` (99.5%),
   `ServiceDate` (98%), `ReasonCode` (91%).
6. **`CD=0`** appears alongside districts 1–15 — likely "couldn't assign."
7. **Cancelled (~43K) and duplicate-flagged (~3K) cases** are present and
   need filtering decisions.
8. **Reporting bias is structural.** This data measures *reports*, not
   *problems*. Neighborhoods differ in propensity to report and in channel
   (`RequestSource`). Quiet ≠ clean.

## First impressions

Rich, current, and permissively licensed — a strong backbone dataset. Our
focus areas (illegal dumping ~243K, item pickups ~246K, graffiti ~121K)
happen to be the system's largest operational workloads. Data quality issues
are real but all look manageable with explicit cleaning rules.

## Questions raised while exploring the schema

- What operationally distinguishes `Item Pickups` from
  `Illegal Dumping Item Pickup`?
- What exactly triggers a `Service Not Complete` case? (Possible ready-made
  recurrence signal — ~66K of them.)
- What is the `ResolutionCode` vocabulary, and does it distinguish
  "fixed" from "closed without action"?
- Are `Information-Only` calls geographically skewed (a proxy for who relies
  on 311)?
- How should the 62 new categories be mapped to old ones for pre-2026 trends?
- How do we deduplicate the Mar–Dec 2025 transition dataset against the
  old-system 2025 dataset?
