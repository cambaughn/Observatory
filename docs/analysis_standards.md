# Observatory Analysis Standards

Shared methodology for every analysis notebook. Reference this document
instead of re-deriving these decisions. If an analysis deviates from a
standard, it must say so explicitly and say why.

Established 2026-07-06 from checkpoints 2–3 (see
[`myla311.md`](../shared/references/myla311.md) and
[`myla311_operational_model.md`](../shared/references/myla311_operational_model.md)).
This is a living document — amend it when evidence changes, and note the
change in [`observatory_findings.md`](observatory_findings.md).

---

## 1. Default inclusion/exclusion rules

Unless the research question demands otherwise, an *operational* analysis
(anything about maintenance work: volumes, response times, hotspots,
department performance) starts from:

| Rule | Rationale |
|---|---|
| **Exclude** `RequestType` in {`Information-Only`, `Feedback`, `Program Research`} | Intake artifacts (~24% of cases): call-center Q&A, not maintenance work |
| **Exclude** `Status` in {`Cancelled`, `Potential Duplicate`, `Duplicate Confirm`} | Not real serviced demand |
| **Exclude** resolution outcome class `duplicate` (see §5) even when Status is `Closed` | ~53K closed cases are coded as duplicates |
| **Keep** `Reported` cases for *demand* questions; **exclude** them for *performance* questions | They are real problems, but no individual work order exists, so "resolution time" is meaningless for them |
| **Keep** internal channels (`recycLA Service Provider`, `Driver Self Report*`) for workload questions; **exclude** for "resident demand" questions | They are city/franchise-originated, not resident reports |

Every notebook states its filters in its first section, even when they are
exactly these defaults ("Standard operational filter, per
`analysis_standards.md` §1").

### Reference implementation

Copy-paste this into notebooks (per project principles we copy, not import,
until duplication becomes painful — when it does, this becomes the first
candidate for the domain's `analysis/`):

```python
INTAKE_ARTIFACTS = {"Information-Only", "Feedback", "Program Research"}
DEAD_STATUSES = {"Cancelled", "Potential Duplicate", "Duplicate Confirm"}

def standard_operational_filter(df):
    """Standard filter per docs/analysis_standards.md §1."""
    out = df[~df["RequestType"].isin(INTAKE_ARTIFACTS)]
    out = out[~out["Status"].isin(DEAD_STATUSES)]
    return out
```

## 2. Information-Only cases

Excluded from operational analyses (above), but **not garbage** — they are
~280K observations of who relies on the 311 phone line for information.
Acceptable uses: channel-mix analysis, neighborhood reporting-behavior
analysis, call-center workload. Never mix them into request volumes or
resolution-time statistics.

## 3. Duplicates

- Drop `Potential Duplicate` / `Duplicate Confirm` statuses and
  duplicate-coded resolutions (`DUP-*`, `B-Duplicated Request`, `CDR-*`) by
  default.
- **Known limitation:** the system does not link duplicates to their
  original case, and independent re-reports of the same physical problem get
  fresh CaseNumbers. Therefore *case counts overstate unique problems*, and
  spatial clustering of "distinct" cases partly measures re-reporting. Any
  hotspot/recurrence analysis must say whether it counts *reports* or
  attempts to deduplicate into *problems* (and how).

## 4. Cancelled requests

Excluded by default. Two subgroups worth remembering:

- `RCAN-Cancelled by Contractor` (~16.6K, mostly recycLA `Service Not
  Complete` cases) — cancellation initiated by the service provider, an
  interesting subject in its own right.
- `0999-Wrong SR Type` reasons — intake misclassification, a data-quality
  signal.

Cancellation *rates* (by type, area, channel) are a legitimate analysis
target; cancelled cases just don't belong in service-delivery metrics.

## 5. ResolutionCode → outcome classes

141 raw codes collapse into seven analysis classes. Classify by exact code;
the listed codes cover >99% of non-null values. Anything unmatched →
`unclassified`, and the notebook must print its unclassified codes so we
can extend this table.

| Class | Meaning | Codes (principal) |
|---|---|---|
| `work_performed` | City/contractor did physical work | `AR-Request Completed`, `RC-Contractor Serviced`, `RC-Request Completed`, `COM-Request Completed`, `WC-Work Completed`, `SARH-*`, `SARC-*`, `PFR-*`, `LR-*`, `TR-*`, `BR-*`, `RSP-*`, `IWO-*`, `MNT-*`, `VM-*`, `VMRB-*`, `OPUVM-*`, `BF-*`, `R-Repaired`, `TSC-Trimmed for Clearance`, `AD-Request Completed` |
| `no_service_needed` | Crew responded; nothing to do | `QC-Item Not Out`, `NCPP-*`, `ASG-Already Serviced`, `UTM-Unable to Make`, `NAT-No Action Taken`, `VNL-Vehicle Not at Location`, `NAR-No Action Required`, `BINS-Bin Empty-No Service`, `ASAT-Appears Safe at This Time` |
| `administrative_close` | Record closed without evidence of field work | `C-Closed`, `1004-Closed`, `RF-Receive and File`, `GI-General Information`, `IP-Information Provided`, `AAA-Assisted and Advised`, `IO-Information Only`, `CL-CL - Closed` |
| `acknowledged` | Report received; feeds programs, no work order | `C-Report has been received`, `C-Report has been referred out.` |
| `referred` | Sent to external agency | `1003-Referral to External Department` |
| `duplicate` | Duplicate of another case | `DUP-*`, `B-Duplicated Request`, `CDR-*` |
| `cancelled` | Cancelled | `RCAN-*`, `1005-Cancelled`, `CANC-*`, `CG-Cancelled`, `RBI-Reschedule for Bulky Items`, `RWG-Reschedule for White Goods`, `REW-Reschedule for E-Waste`, `CCAN-Cancelled by Customer` |

*Amended 2026-07-06 (notebook 03): 13 codes added via the unclassified-codes
rule; residual unclassified now ~0.5% of terminal cases.*

Notes:
- "Success-rate" style metrics compare `work_performed` against
  `no_service_needed` + `administrative_close`, never just "Closed".
- `administrative_close` is the honest name for `C-Closed` (325K cases,
  32% of closures): we *do not know* what happened. Do not count it as
  work done.
- This mapping is our construction (the field is undocumented). It is a
  standard, not a truth — revisit after any stakeholder conversation with
  ITA/LASAN.

## 6. Assumptions every analysis must state

1. **Reports ≠ problems.** The data measures reporting behavior as much as
   street conditions. Quiet ≠ clean; loud ≠ dirty. (Neighborhood-level
   comparisons especially.)
2. **Closed ≠ fixed.** Use outcome classes (§5).
3. **Snapshot censoring.** We see current state only. Open cases have no
   resolution time yet, so *recent periods look artificially fast/clean* —
   restrict duration analyses to cases created long enough ago to have had
   a fair chance to close, and say what cutoff was used.
4. **One case ≠ one problem** (§3).
5. **Single-era scope.** 2026-system data only; no comparisons across the
   late-2025 migration without explicit category/schema mapping.
6. **Geocoding trust bounds.** Coordinates only within lat 33.60–34.40,
   lon −118.75 to −118.10; ~5% missing + junk outside bounds get dropped —
   state the row loss.

## 7. Common pitfalls

- **Counting `Information-Only` in demand** → inflates everything ~24%.
- **Averaging resolution time across request types** — a graffiti wipe and
  a tree removal have different clocks; always segment by type.
- **Mean durations on skewed data** — report medians (plus p90 if spread
  matters).
- **Treating `Reported` ClosedDate as service completion** — it is record
  acknowledgment, not work (encampment reports feed scheduled CARE+
  deployments).
- **Trusting `Owner` raw strings** — normalize first (duplicate labels:
  `LSD` = `LASAN - LSD`, `Sanitation` = `LASAN`; staff names; `TEST XX`).
- **`CD = 0`** is "unassigned", not a 16th district.
- **Channel mix confounds geography** — self-service vs call shares differ
  by area; any equity comparison should check `RequestSource` composition.
- **`ServiceDate`, `DateServiceRendered`, `Location` are near-empty** — do
  not build on them.

## 8. Known data quality issues (running list)

From [`myla311.md`](../shared/references/myla311.md) and
[`myla311_operational_model.md`](../shared/references/myla311_operational_model.md):

1. ~5% missing coordinates; junk values outside plausible bounds.
2. `Owner`: 96 values needing normalization; test records present.
3. `RequestSource`: `Driver Self Report` vs `Driver Self Reported` (same
   channel, two spellings).
4. `CreatedByUserOrganization` contradicts its official description (97%
   "Self Service" including call-created cases) — do not use without
   further investigation.
5. Near-dead columns: `Location` (100% empty), `DateServiceRendered`
   (99.5%), `ServiceDate` (98%), `ReasonCode` (91%).
6. `Mobile App` channel implausibly small (0.3%) — app traffic may be
   labeled `Self Service`; treat the two as one "self-service" channel.
7. No official data dictionary for `Status`, `ResolutionCode`,
   `ReasonCode`, `ActionTaken` — our semantics are inferred.
8. 2025 old-system dataset ends Nov 3, 2025; transition dataset overlaps
   Mar–Dec 2025; deduplication between them unresolved.
9. **Batch imports masquerade as demand.** 2026-03-25, 11am: 8,201 cases in
   one hour, 7,585 of them `Streetlight Repair Services` labeled
   `Mobile App` — inflates H1 streetlight volume ~30% and accounts for most
   of the app channel. Check category time series for single-hour spikes
   before interpreting trends (notebook 03).

## 9. Notebook conventions

- One question per notebook, stated in the first cell, numbered
  sequentially (`03_…`, `04_…`).
- Each domain numbers its notebooks independently, starting at `01_…`.
  Cross-domain citations name the domain ("dumping notebook 06").
  *Grandfathered exception:* illegal dumping keeps 04–07 — those numbers
  are load-bearing in the findings ledger, tracker, and derived filenames
  (`field_program_nb06.csv`); do not renumber them.
- State filters (§1), assumptions (§6), and any cutoffs up front.
- Raw data is never modified; derived datasets go to the domain's `data/processed/`
  with the producing notebook named in the filename or a README line.
- Deterministic sampling (`random_state=…`) so reruns match.
- End with: findings (→ promote durable ones to
  [`observatory_findings.md`](observatory_findings.md)) and new questions
  (→ the domain's `questions.md`, or [`research_questions.md`](research_questions.md) for cross-domain questions).
