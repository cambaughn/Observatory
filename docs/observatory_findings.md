# Observatory Findings

Living document of confirmed findings and open questions. Newest additions
at the bottom of each section. Every finding cites its evidence (notebook
or document). A finding gets an entry only once it's confirmed, not while
it's a hunch.

---

## Confirmed findings

### F1. LA replaced its 311 platform in late 2025 *(2026-07-06)*

The old "Service Request Data" era (2015–2025, ~12 request types) ends
Nov 3, 2025; a Salesforce-based "Cases" era begins (62 request types, new
schema). Historical continuity is broken at the migration boundary; no
cross-era comparison without explicit mapping.
Evidence: [`datasets/myla311.md`](datasets/myla311.md).

### F2. ~24% of 311 cases are intake artifacts, not maintenance requests *(2026-07-06)*

`Information-Only` alone is ~280K of 1.21M cases (23%), created and closed
within 60 seconds — call-center Q&A logged as cases. Of ~600K phone calls,
only ~336K produced a service request. 311 is as much an information
hotline as a work-order intake.
Evidence: notebooks 01, 02.

### F3. "Closed" does not mean "fixed" — and the data can tell the difference *(2026-07-06)*

The undocumented 141-value `ResolutionCode` field separates real outcomes:
work performed vs. crew-found-nothing vs. administrative closure vs.
duplicate/cancelled. 32% of closures are bare `C-Closed` (outcome unknown).
Standardized into seven outcome classes in
[`analysis_standards.md` §5](analysis_standards.md).
Evidence: notebook 02, [`datasets/myla311_operational_model.md`](datasets/myla311_operational_model.md).

### F4. Enormous dispatched-but-wasted capacity: `QC-Item Not Out` *(2026-07-06)*

The third most common outcome in the entire system (118K cases in ~6
months): a collection crew responds to an item-pickup/dumping case and the
item isn't there. Potentially a major efficiency lever; mechanism unknown
(late crews? premature reports? item scavenged?).
Evidence: notebook 02.

### F5. Street maintenance is substantially executed by named contractors *(2026-07-06)*

`AssignTo` exposes the execution layer: graffiti removal runs through
OCB-contracted nonprofits (CCAC, KYCC, Northeast Graffiti Busters,
Hollywood Beautification Team, LA Corps, CRCD…, with a public 72-hour
removal goal); dockless scooter cases go to Lime; recycLA franchise
haulers file and cancel their own missed-collection cases.
Evidence: notebook 02; laocb.org.

### F6. Report-only case types never get individual work orders *(2026-07-06)*

Homeless encampments (~53K), private property violations, sidewalk
problems terminate in status `Reported` ("report has been received") and
feed scheduled programs (LASAN LSD's CARE/CARE+ regional deployments)
rather than per-case dispatch. Their `ClosedDate` marks record
acknowledgment, not service.
Evidence: notebook 02; sanitation.lacity.gov/livability.

### F7. Our focus areas are the system's biggest workload *(2026-07-06)*

Item pickups (~246K) + illegal dumping (~243K) + graffiti (~121K) dominate
operational volume — together roughly two-thirds of non-intake cases.
Evidence: notebook 01.

### F8. `Service Not Complete` is a missed-trash-collection workflow *(2026-07-06)*

Not a general recurrence signal: owned by LASAN/recycLA, a quarter filed
by the haulers themselves, resolutions are completed/cancelled-by-
contractor. Recurrence analysis must be built spatially instead.
Evidence: notebook 02.

### F9. Operational demand is object-removal-dominated and extremely concentrated *(2026-07-06)*

Jan–Jun 2026, standard operational filter (~804K cases, ~4,400/day,
~1.6M/yr pace): `Item Pickups` (29.1%) + `Illegal Dumping Item Pickup`
(28.8%) = **58% of all demand**; top 5 categories = 78%; the 40 smallest
categories = 5%. Pavement, sidewalks, lighting are single digits each.
LASAN and its divisions receive ~72% of demand; its six collection-yard
districts are the city's largest workgroups.
Evidence: notebook 03.

### F10. The "front door" depends on the filter: website carries service demand, phone carries questions *(2026-07-06)*

Raw cases: phone ~50%. Operational demand: **website 62%, phone 36%** —
calls disproportionately produce Information-Only entries. Channel claims
about 311 flip sign depending on this filter. ~17% of terminal operational
cases still resolve `no_service_needed` (F4 sized on filtered data).
Evidence: notebook 03.

### F11. Council-district demand is nearly flat; neighborhood-scale demand is not *(2026-07-06)*

Raw case volume varies only **1.5x across the 15 council districts**
(43K–64K), but **27x across the 99 Neighborhood Councils** (Wilshire
Center-Koreatown 22.6K → Hermon 835), pre-normalization. The interesting
variation lives below district scale. Weekly rhythm: weekdays ≈ 2x
Saturday; Sunday runs 25% above Saturday.
Evidence: notebook 03.

### F12. At least one batch import masquerades as demand *(2026-07-06)*

2026-03-25, 11am hour: 8,201 cases created, 7,585 of them `Streetlight
Repair Services`, mostly labeled `Mobile App` — a bulk load (likely a BSL
backlog transfer), not organic reporting. Inflates H1 streetlight volume
~30%, supplies most of the year's app-channel volume (partially explains
O4), and warns that category time series need spike checks (standards §8.9).
Evidence: notebook 03.

---

## Open questions

### O1. Why does `RAP - Construction` own ~45K graffiti-removal cases?

Rec & Parks as second-largest graffiti owner after OCB is unexplained.
Routing rule (parks facilities?) or artifact? *(Ask OCB/RAP.)*

### O2. What formally distinguishes `Item Pickups` from `Illegal Dumping Item Pickup`?

Both LASAN item collection with shared outcome codes. Presumed scheduled
bulky pickup vs. dumped material in public right-of-way; no official
definition found. Affects how we define "illegal dumping" in every
analysis. *(Ask LASAN; check MyLA311 service catalog.)*

### O3. What drives 118K `QC-Item Not Out` outcomes? (see F4)

Resident behavior, scavenging, response latency, or address errors? Data
alone may narrow it (e.g., does it correlate with response delay?); field
observation could settle it.

### O4. Where did mobile app traffic go?

`Mobile App` is 0.3% of 2026 cases — implausibly low. Folded into
`Self Service`? Affects channel-equity analyses. *(Ask ITA.)*

### O5. Does an official data dictionary exist for the new system?

`Status`, `ResolutionCode`, `ReasonCode`, `ActionTaken` are publicly
undocumented; our semantics are inferred. *(Ask ITA — highest-value
single question on the list.)*

### O6. How should the two 2025 datasets be deduplicated?

Old-system 2025 (ends Nov 3) overlaps the transition "Cases Mar–Dec 2025"
dataset. Blocks any 2025 analysis. *(Deferred until we need 2025 data.)*

### O7. Is real case volume up after the migration?

~423K old-system cases in 10 months of 2025 vs 1.21M new-system cases in
6 months of 2026 — but the new system logs intake artifacts as cases.
Unclear how much is real demand growth vs. accounting change.

---

### O8. Is the Sunday demand uptick a bulky-item scheduling effect?

Sunday runs 25% above Saturday. Hypothesis: residents set out items ahead
of the collection week. Testable in the item-collection case study.

### O9. Does channel mix (phone vs web) vary by neighborhood?

If some communities depend on the phone, channel-based friction is an
equity issue, and channel mix confounds geographic comparisons. Testable
now with existing data.

### O10. Do crew-discovered cases (`Driver Self Reported`) cluster where resident reporting is low?

If yes, they're a partial ground-truth wedge into reporting bias (the
quiet-≠-clean problem). Testable now.

---

## Amendment log

- 2026-07-06 — Document created with F1–F8, O1–O7 (from checkpoints 1–3).
- 2026-07-06 — Notebook 03 (demand survey): added F9–F12, O8–O10; standards
  §5 outcome table extended (13 codes), data-quality register gained batch-
  import warning (§8.9).
