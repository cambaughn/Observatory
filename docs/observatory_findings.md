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

### F13. Illegal dumping response is fast and complete — persistence, not response failure, is the phenomenon *(2026-07-06)*

Jan–Jun 2026: 231.5K dumping reports (28.8% of operational demand,
~1,279/day, steady). Outcomes are nearly binary: ~71% collected, ~26%
gone on arrival, closed fast (30% same-day, 92% ≤7 days). The ticket
queue works; the streets refill anyway.
Evidence: notebook 04.

### F14. Dumping is dominated by recurrence at specific points *(2026-07-06)*

Even with crude address-string matching, **70% of dumping reports occur
at addresses reported 2+ times within six months** (43K repeat
addresses); the top corner (4th St & New Hampshire Ave, Koreatown) was
reported 115 times (~every 37 hours). Geography is structured: South LA,
East Valley, Koreatown over-index even after controlling for overall 311
usage (CD6 1.32x, CD8 1.30x; CD12 0.58x). Caveat: repeat *reports* ≠
repeat *dumping events* (duplicate-linking gap).
Evidence: notebook 04.

### F15. Two service tracks clear dumping at different speeds *(2026-07-06)*

18% of dumping cases are owned by LSD (encampment division; CARE/CARE+
scheduled sweeps) and close in **median 1.0 day**; regular LASAN yard
dispatch takes **median 2.7 days**. Same 26% gone-on-arrival rate in
both. Performance/equity analyses must hold the track constant.
Evidence: notebook 04.

### F16. Gone-on-arrival correlates with slower response — a race with informal clearance *(2026-07-06)*

`QC-Item Not Out` dumping cases took longer to close (median 2.9d) than
collected ones (2.0d): consistent with scavengers/neighbors clearing
piles the city is slow to reach. Correlation only — confounded by
geography/workload; cleaner within-yard test pending (extends O3).
Evidence: notebook 04.

### F17. Illegal dumping is a place problem: report mass concentrates at recurring 20m locations *(2026-07-07)*

Using coordinate clustering (20m connected components; threshold validated
against the known top site): **81% of dumping reports occur at recurring
places**; 48% at places hit 5+ times in six months; ~300 places (25+
reports) carry ~10K reports; 19 places exceed 50. Recurrence decomposes
into **duplicate pressure** (21% of repeat-gaps <1 day — re-reports of a
standing pile) and **genuine refill cycles** (median gap ~10 days, 25% of
gaps >30 days). Dumping reports are ~100% geocoded (14 missing of 231.5K).
Evidence: notebook 05; field list in
`data/processed/dumping_field_candidates_nb05.csv`.

### F18. Hotspots are two-tier: an anchored chronic top over a churning middle *(2026-07-07)*

Top tier: 99% of 25+ report places are active in all three 2-month
periods; 78% sustain 5+ reports in every period; 83% active all six
months — the same corners absorb dozens of successful cleanups without
moving (removal does not touch the generating mechanism). Middle tier:
of ~7.5K places with 3+ reports in Jan–Feb, a third fall silent by
May–Jun; P1↔P3 count correlation ~0.16. Chronic sites bead along specific
arterials/alleys — sub-neighborhood structure invisible at CD resolution.
Interventions targeting last quarter's mid-tier list would systematically
miss.
Evidence: notebook 05.

### F19. Valley neighborhoods differ in dumping structure — and in failure mode *(2026-07-07)*

Calibration of seven SFV neighborhoods (NC-mapped): Van Nuys is the
Valley's dumping capital (46% of its own 311 demand = 1.6x citywide mix,
top intensity, 31 chronic sites); NoHo is the volume giant with the
highest encampment component (20% LSD); **Panorama City fails
differently** (Valley's slowest closes, 3.7d, and highest gone-on-arrival,
36%); Reseda is a corridor phenomenon (its top three places all on
Sherman Way 17800–17950); Encino hides 7 chronic pockets inside a clean
background (0.78x, fastest closes 1.8d); **Studio City is the clean
control** (0.59x, zero chronic 25+ places). Meanwhile recurring share
barely varies (75–89%) across a 0.59x–1.60x demand-mix range —
**recurrence is the universal structure of dumping, not a bad-neighborhood
trait**; neighborhoods differ in chronic-place count and intensity.
Evidence: notebook 06; field program in
`data/processed/field_program_nb06.csv`.

### F20. The citywide #1 dumping site went silent in mid-April *(2026-07-07)*

4th St & New Hampshire Ave (Koreatown, 100% LSD-serviced): 115 reports
Jan 1–Apr 17 (~one per 1.5 days), then **zero for the rest of the period**.
**Explained (2026-07-07): the encampment at the corner's vacant lot was
resolved in late April.** `Homeless Encampment` reports within 150m
collapsed from ~100/month (Jan–Apr) to 4/month (May–Jun) simultaneously;
dumping in the surrounding 30–300m ring continued unchanged (~80/month) —
so no reporting collapse and no next-door migration. External context:
this corner was already citywide #1 in Apr–Dec 2025 (206 reports, LAist),
with a documented tent cluster on the vacant SE-corner lot; CD10 was
actively working the corridor (city moved to acquire the 4th & Kingsley
lot for a pocket park on 2026-04-02). Which intervention did it — CARE+/
Inside Safe op, lot fencing, or media pressure — and whether the street
is clean or merely unreported: field visit + CD10/LSD interview. The
program's best natural experiment on what makes a chronic site stop.
Evidence: notebook 06 (postscript); laist.com coverage.

### F21. Top "places" are largely address-stacks; the micro-area is the real unit *(2026-07-08)*

Forensic check of the field-program sites: 6 of 9 Valley sites (and
several citywide ones) have **100% of reports at one exact coordinate
with one address string, 91–100% self-service** — web reports geocoded to
a named parcel, not GPS readings at a curb. Meanwhile every site sits in
a hot micro-area: the pin accounts for only **~4–40% (typically 10–17%)
of dumping reports within 250m** (e.g., Delano St: 58 at the pin, 433
more at 130 nearby spots). Implications: (a) the 20m place ranking is
biased toward addresses reporters *name* — confirmed and quantified
version of notebook 05's geocode-bin caveat on F17; (b) field
investigation must cover the block, not the address (notebook 07 now
shows all surrounding report-stacks per stop); (c) single-stack sites
may reflect a chronic *reporter* as much as a chronic *pile* (RT-11).
Counter-examples that look like genuine physical clusters: 14102 Delano
(7 coords, 8 address variants, 55% phone), 17900 Sherman Way (7 coords).
Evidence: scripts/build_field_area_context.py output;
data/processed/field_site_diagnostics.csv.

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

### O11. Crew-level cleanup policy (interview: LASAN yards, LSD/CARE+ leads)

Not answerable from case data: (a) if a crew sees additional dumped items
near a work order, do they collect them? (b) what share of cleanup is
proactive/patrol vs ticket-driven, and did anything replace CleanStat's
proactive street scoring? (c) how do crews decide what to take on scene
(size/hazard limits, private-property line, e-waste/white-goods handling)?

### O12. What routes a dumping case to LSD vs a regular yard?

Encampment proximity? Dispatcher judgment? Keyword? Determines what the
two-track speed gap (F15) actually measures.

### O13. Are repeat reports one long-lived pile or many dumping events?

The duplicate-linking gap means 115 reports at one corner could be
anywhere from a few piles to 115. Inter-report timing vs closure timing
may partially separate these; field observation can settle it.

### O14. What distinguishes anchored chronic sites from the churning middle tier?

Land use, alley access, encampment proximity, lighting, enforcement
history? Needs parcel/land-use data joins and the field program (notebook
05's six-visit plan across three site archetypes).

### O15. Is middle-tier churn migration, resolution, or reporting fatigue?

Reporting fatigue is invisible in case data; field checks of gone-quiet
places can distinguish "cleaned up" from "gave up reporting."

---

## Amendment log

- 2026-07-06 — Document created with F1–F8, O1–O7 (from checkpoints 1–3).
- 2026-07-06 — Notebook 03 (demand survey): added F9–F12, O8–O10; standards
  §5 outcome table extended (13 codes), data-quality register gained batch-
  import warning (§8.9).
- 2026-07-06 — Notebook 04 (illegal dumping case study): added F13–F16,
  O11–O13. Project focus confirmed: illegal dumping is the primary object
  of study; scheduled Item Pickups serve as context/control.
- 2026-07-07 — Notebook 05 (recurrence & hotspot structure): added F17–F18,
  O14–O15; first field-visit target list produced (20 ranked sites, six-visit
  program); council district boundaries added to data/raw (download script
  extended).
- 2026-07-08 — Address-stack forensics (user-prompted sanity check): added
  F21, RT-11; notebook 07 stop maps now show 350m area context; F17's
  geocode-bin caveat upgraded from suspicion to quantified finding.
- 2026-07-07 — Notebook 06 (SFV neighborhood calibration): added F19–F20;
  full field program produced (10 citywide + 9 Valley targets in
  data/processed/field_program_nb06.csv + 5 clean comparison corridors).
- 2026-07-08 — Per-capita denominators upgraded from the city's 2010-by-NC
  file to 2020 Census blocks aggregated into certified NC boundaries
  (scripts/build_nc_population_2020.py; validated against official county
  total). Neighborhood rates shifted <3%; no conclusions changed.
