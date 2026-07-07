# MyLA311 Operational Model (2026 "Cases" system)

How a request moves through the current MyLA311 system, as far as the
evidence supports. Companion evidence:
[`notebooks/02_operational_model.ipynb`](../../notebooks/02_operational_model.ipynb).
Based on the 2026-07-06 snapshot (1.21M cases). Last reviewed: 2026-07-06.

## Evidence base — and its limits

- The Socrata metadata has official descriptions for `Owner`, `AssignTo`,
  `RequestSource`, `CreatedByUserOrganization`, `ServiceDate`, `ClosedDate`.
- **`Status`, `ResolutionCode`, `ReasonCode`, and `ActionTaken` have no
  official documentation anywhere we could find** — no data dictionary is
  attached to the dataset. Their semantics below are inferred from value
  distributions and cross-tabulations, corroborated with official City
  program documentation (LASAN LSD/CARE+, OCB graffiti program) where it
  exists. Inferences are marked *(inferred)*.
- **The dataset is a snapshot, not an event log.** Each case appears once in
  its current state. We never observe transitions, per-state timestamps, or
  reopenings. The lifecycle below is reconstructed, not watched.

## Lifecycle of a request

```
                         Citizen (or crew / hauler / council office)
                                          |
             +----------------------------+---------------------------+
             |                                                        |
      Agent channels                                          Self-service channels
  Call, Email, Chat, Voicemail,                            Web portal, Mobile App,
  Council's Office  (~50%)                                 recycLA, Driver Self Report (~50%)
             |                                                        |
   311 agent logs ActionTaken:                                        |
   - Information Provided / Status                                    |
     Provided / Transferred  ->  case type "Information-Only",        |
     created & closed within seconds (23% of ALL cases)               |
   - SR Created -------------------+----------------------------------+
                                   |
                            Case created [New]
                                   |
                     routed to Owner (department/bureau)
                     and AssignTo (yard, crew, or contractor)
                                   |
        +--------------------------+--------------------------------------+
        |                          |                                      |
  Work-order path           Report-only path                     Case-hygiene paths
        |                          |                                      |
 [Workorder Created]          [Reported]                       [Potential Duplicate]
        |                  report acknowledged                            |
 [In Progress]             ("C-Report has been               [Duplicate Confirm]
        |                  received"); feeds programs                     |
    [Closed]               (e.g. CARE+ scheduled                    [Cancelled]
  with department-         encampment cleanups), no                       |
  specific                 individual work order                 [Closed Ext-Referred]
  ResolutionCode                                                referred to external
                                                                agency (County, Caltrans…)
```

Every step above is evidenced: channel split and agent actions from
`RequestSource` × `ActionTaken`; instant Information-Only closure from
timestamps; states from `Status`; routing from `Owner`/`AssignTo`;
terminal codes from `Status` × `ResolutionCode`.

## Workflow states (`Status`, 9 values) *(inferred)*

| Status | Count | ClosedDate? | Meaning |
|---|---|---|---|
| `Closed` | 1,019,428 | always | Terminal. **Does not imply the problem was fixed** — see ResolutionCode |
| `Reported` | 65,068 | always | Terminal acknowledgment for report-only types (encampments, private property violations, sidewalk problems) |
| `Workorder Created` | 51,665 | never | Routed into a department work-order system; work pending |
| `Cancelled` | 42,755 | always | Terminal; incl. ~16.6K "Cancelled by Contractor" |
| `New` | 14,729 | never | Created, not yet routed/triaged |
| `In Progress` | 7,100 | never | Active work |
| `Closed Ext-Referred` | 5,914 | always | Closed by referral to an external agency (resolution `1003`) |
| `Potential Duplicate` | 2,576 | never | Flagged, awaiting review |
| `Duplicate Confirm` | 413 | never | Confirmed duplicate |

Note the `ClosedDate` quirk: `Reported` cases carry a `ClosedDate`, while
`Workorder Created` never does — `ClosedDate` marks *case-record* closure at
the 311 level, not completion of physical work.

## Key field semantics

### `ResolutionCode` (141 values, no docs) *(inferred)*

Department-specific closure vocabularies, distinguishable by prefix style.
Functional families:

- **Work performed:** `AR-Request Completed` (386K), `RC-Contractor
  Serviced`, `SARH`/`SARC` (StreetsLA Small Asphalt Repair, hot/cold mix),
  `PFR-Palm Fronds Removed`, `LR-Limb Removed`, `TR-Tree Removed`,
  `BR-Barricades removed`, `WC-Work Completed`
- **Crew responded, no service possible/needed:** `QC-Item Not Out`
  (**118K — the third most common outcome in the entire system**),
  `NCPP-Not at Curb / On Private Property`, `ASG-Already Serviced`,
  `UTM-Unable to Make`
- **Administrative closure:** `C-Closed` (325K), `1004-Closed`,
  `RF-Receive and File`, `NAT-No Action Taken`, `GI-General Information`
- **Acknowledgment:** `C-Report has been received` (59K, pairs with
  `Reported`)
- **Duplicates / cancellations:** `DUP-*`, `B-Duplicated Request`, `CDR-*`,
  `RCAN-Cancelled by Contractor`, `1005-Cancelled`
- **Referral:** `1003-Referral to External Department`
- **Dockless-mobility set:** `VM-Vehicle moved…`, `VMRB-…rebalancing`,
  `OPUVM-Operator picked up vehicle…`

**This field answers Checkpoint 2's biggest question: closure outcome IS
distinguishable.** Any resolution-quality analysis must group these codes
into outcome classes first.

### `ReasonCode` (97 values, 91% empty, no docs) *(inferred)*

Optional per-department workflow annotation: inspection outcomes
(`I-Inspected`), scheduling steps (`SARS-…SAR scheduled`), failure causes
(`0200-Blocked in By Vehicle/Object`), case hygiene (`0999-Wrong SR Type`,
`1000-Change Internal Department`). Too sparse and inconsistent to serve as
a primary analysis field; useful qualitatively.

### `ActionTaken` (10 values, no docs) *(inferred, high confidence)*

The 311 **agent's** action at intake. Populated for ~100% of
agent-handled-channel cases (Call, Email, Chat, Voicemail, Council's
Office) and ~0% of self-service cases. Values: `SR Created`,
`Information Provided`, `Transferred`, `Status Provided`,
`Unable to Assist`, `Escalate to Supervisor`, etc. Reveals the call
center's own workload: of ~600K calls, only ~336K resulted in an SR;
~205K were answered with information, ~43K transferred.

### `Owner` (96 values, officially "department assigned")

Primary routing target. Top owners and their domains:

| Owner | Cases | Who / what |
|---|---|---|
| `LASAN` | 618K | LA Sanitation & Environment — collections, dumping, dead animals |
| `ITA` | 165K | Information Technology Agency (runs the 311 center) — owns `Information-Only` |
| `OCB - Normal Cases` (+ Special) | 75K | Office of Community Beautification (Board of Public Works) — graffiti, via contracted CBOs |
| `LSD` / `LASAN - LSD` | 99K | LASAN Livability Services Division — homeless encampments (CARE/CARE+ program) — **same unit, two labels** |
| `RAP - Construction` | 46K | Recreation & Parks — but owns mostly *graffiti* cases (unexplained, see below) |
| `BSS - SMD` / `IED` / `UFD` / `UTA` | 86K | StreetsLA (Bureau of Street Services): Street Maintenance, Investigation & Enforcement, Urban Forestry divisions |
| `BSL` | 25K | Bureau of Street Lighting |
| `recycLA` | 25K | Commercial waste franchise program |
| `LADOT - *` | 40K+ | Transportation: district ops, dockless mobility, parking, signals |
| `LAAS` | 4K | Animal Services |

Caveats: duplicate labels (`LSD` vs `LASAN - LSD`, `Sanitation` vs
`LASAN`), individual staff names, and a literal `TEST XX` (5 cases).
Requires a normalization map before department-level analysis.

### `AssignTo` (49 values, officially "specific group assigned")

The execution level below `Owner`. Two populations:

- **LASAN service-yard districts:** `NC` (North Central), `EV` (East
  Valley), `WV` (West Valley), `WLA`, `SLA` (South LA), `HB` (Harbor) —
  ~560K cases *(district decoding inferred from official LASAN yard
  geography; not yet verified per-case)*
- **Contractors and programs:** graffiti CBOs contracted by OCB — `CCAC`
  (Central City Action Committee), `KYCC` (Koreatown Youth & Community
  Center), `NEGB` (Northeast Graffiti Busters), `HBT` (Hollywood
  Beautification Team), `LA Corps`, `CRCD`, `GAPBH`, `WVA`, `PGS`, `NDFY`
  — plus `Lime` for dockless scooters.

**A large share of LA's visible street maintenance is executed by
nonprofit contractors, and this field names them.** OCB's published goal
is graffiti removal within 72 hours of report.

### `RequestType` (62 values, officially documented as the case type)

Functional families (share of all cases):

- **Sanitation collections (45%):** Item Pickups, Illegal Dumping Item
  Pickup, Dead Animal Removal, Service Not Complete
- **Intake artifacts (24%):** Information-Only, Feedback, Program Research
- **Cleanliness/livability (15%):** Graffiti Removal, Homeless Encampment
- **Streets & trees (8%):** pavement, sidewalks, tree emergencies/trims,
  street sweeping
- **Transportation (3%):** dockless mobility, parking, signals, signs
- **Lighting (2%):** streetlight repair variants
- Small tails: animals, parks, water/flooding, misc.

`Service Not Complete` is now understood: a **missed-collection follow-up
workflow** owned by LASAN/recycLA (a quarter filed by the haulers
themselves) — not a general "problem came back" signal.

`Item Pickups` vs `Illegal Dumping Item Pickup` remains partially open:
both are LASAN item collection; the volumes and the shared `QC-Item Not
Out` outcome suggest scheduled bulky-item pickup vs. dumped-material
report, but no official definition found yet.

### `RequestSource` (18 values, officially documented)

Call 49.6%, Self Service (web portal) 47.9%, then a long tail. Notable:
`recycLA Service Provider` and `Driver Self Report`/`Driver Self Reported`
(two spellings of the same thing) are *internal/franchise* channels —
"requests" not originating from residents. `Mobile App` is only 3.7K
(0.3%), suspiciously low given the old system's app volume; app traffic
may be folded into `Self Service`.

## Where the data is clear

- The status vocabulary is small and its terminal/live split is unambiguous.
- Routing is legible end-to-end: RequestType → Owner → AssignTo, down to
  named contractor.
- Resolution codes genuinely distinguish "work done" from "nothing there"
  from "administrative close."
- Intake channel and agent-vs-self-service behavior are cleanly separable.

## Where the data is ambiguous

- `ClosedDate` on `Reported` cases: closure of the *record*, not of any
  real-world condition.
- `Owner` needs normalization (duplicate labels, staff names, `TEST XX`).
- `RAP - Construction` owning ~45K graffiti-removal cases — routing rule or
  data artifact? Unknown.
- `CreatedByUserOrganization` is `Self Service` for 97% of cases *including
  call-center-created ones*, contradicting its official description.
- `ReasonCode` mixes several unrelated vocabularies.
- `Item Pickups` vs `Illegal Dumping Item Pickup` boundary undefined.

## Questions we still cannot answer from this dataset

1. **State history.** When did a case enter each state? How long did it sit
   in `Workorder Created`? Snapshot data cannot say.
2. **Reopenings.** If a resident re-reports the same issue, it's a new
   CaseNumber; the system does not link them.
3. **Physical outcomes.** Whether the street is actually clean/fixed —
   `DateServiceRendered` is 99.5% empty.
4. **Department SLAs.** Internal targets aren't in the data (only OCB's
   72-hour graffiti goal is public).
5. **What the 62 request types formally mean** — the "full list" the
   metadata points to (MyLA311.lacity.gov) is a service catalog, not a data
   dictionary.

Good stakeholder-interview questions, all five — especially for ITA (data
dictionary?), LASAN (yard codes, SNC workflow), and OCB (contractor SLAs).
