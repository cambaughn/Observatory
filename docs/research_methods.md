# Research Methods

Reusable methods and measurement strategies for the Observatory. Unlike
[analysis_standards.md](analysis_standards.md) (rules for handling the data
we have), this document is about **estimating what the data does not
contain**. Methods get added as investigations demand them.

---

# Estimating Reporting Coverage

**Core question: what percentage of real illegal dumping events are
represented by MyLA311 reports?**

## Why this matters

- **Every conclusion so far is conditioned on the observed fraction.**
  231.5K reports in six months (F13), 81% at recurring places (F17), the
  two-tier hotspot structure (F18) — all describe *reported* dumping. If
  coverage is high and uniform, these describe reality. If coverage is low
  or uneven, they describe reporting behavior wearing reality's clothes.
- **Report counts measure reported demand, not actual dumping.** We have
  seen this cut both ways already: re-reporting inflates counts at visible
  corners (duplicate pressure, F17), while industrial blocks with no
  residents may generate piles nobody files.
- **Coverage almost certainly varies** by neighborhood (reporting
  propensity, digital access — dumping is a web-first, 68% self-service
  category), by land use (residential eyes vs warehouse frontage), and by
  problem type (a couch blocking a sidewalk vs bags behind a fence). The
  Panorama City share/per-capita disagreement (notebook 06) is likely a
  coverage artifact in miniature.
- **Asymmetric conclusions at stake:** "Studio City has little dumping"
  (F19) is safe only if Studio City's coverage is comparable to Van Nuys'.
  Quiet ≠ clean is standards §6.1; this section is the plan for measuring
  *how* unequal the quiet actually is.

## Candidate estimation methods

### 1. Field sampling (visit sites, compare against active reports)

**Description.** Walk predefined street segments (chronic, typical, and
clean strata — the notebook 06 field program already provides this
stratification), record every visible dumping instance, then check each
against open/recent 311 reports at that location. Coverage ≈ share of
observed piles that have a matching report within some distance/time
window.

- **Strengths:** direct measurement; no new data dependencies; doubles as
  the already-planned field program (near-zero marginal cost for a first
  estimate); produces ground truth for validating the 20m place clustering.
- **Weaknesses:** small samples; one-shot visits can't distinguish
  "unreported" from "not yet reported" (a pile 2 hours old may get its
  report tomorrow); observer's own route choice biases the sample; matching
  a pile to a report is fuzzy (is this couch *that* couch?).
- **Effort:** low — a tally sheet added to the existing visit template and
  ~2 extra minutes per site; a defensible stratified version (random
  segments per stratum) is a few field days.
- **When:** **now** — fold a coverage tally into the first field visits.

### 2. Repeat observations (same sites over time)

**Description.** Revisit the Valley field targets (field program section B
was designed for revisits) on a cadence — say weekly — logging pile
presence, arrival, and disappearance. Against report timestamps, this
yields reporting *delay* (pile appears → report filed), *cleanup latency*
(report → gone), and *never-reported share* (piles that appear and vanish
with no report).

- **Strengths:** the only field method that separates coverage from
  timing; measures the full pile lifecycle including informal clearance
  (the F16 "race"); repeated visits build the personal calibration the
  project values.
- **Weaknesses:** labor-intensive and slow (weeks before estimates
  stabilize); a handful of sites, so generalization is weak; observation
  gaps miss short-lived piles (bounds, not exact rates).
- **Effort:** medium — the per-visit work is small but the commitment is
  recurring over 1–2 months.
- **When:** **now, at small scale** — it's already the plan for the Valley
  loop; add pile-level logging to the cadence.

### 3. Crew interviews (LASAN supervisors and field crews)

**Description.** Ask the people who drive the routes: "Of the dumping you
see in a day, how much already has a ticket?" Plus the adjacent policy
questions already tracked (RT-04, RT-05: do crews pick up off-ticket piles,
and is that logged anywhere?).

- **Strengths:** crews see the unreported denominator every day, across
  whole districts — no one else does; free calibration across
  neighborhoods ("Van Nuys vs Reseda?"); simultaneously answers the
  crew-policy questions that change how we read *all* counts.
- **Weaknesses:** impressions, not measurements — recall bias, incentive
  to describe the system favorably; "fraction with a ticket" conflates
  coverage with response speed; needs access.
- **Effort:** low per interview; the bottleneck is getting the meetings.
- **When:** **now** — already scheduled intent in the tracker (RT-04/05/06);
  add the coverage question to those interview guides.

### 4. Proactive-route comparison (if data becomes available)

**Description.** LSD/CARE+ runs scheduled sweeps regardless of tickets
(F15). If per-sweep collection records exist (tonnage, item counts, or
stop logs), compare what sweeps collect against what tickets predicted in
the same segments: sweeps sample reality independently of reporting.
CleanStat's historical proactive street-cleanliness scores are the same
idea if archives survive.

- **Strengths:** large-scale, city-generated ground truth; covers exactly
  the low-reporting areas where field sampling is weakest; retrospective —
  no waiting.
- **Weaknesses:** the data may not exist, may not be shareable, and sweep
  routes are themselves non-random (they target known encampment areas);
  matching sweep records to 311 geography could be painful.
- **Effort:** unknown until asked — the ask itself is one interview
  question (piggybacks on RT-05/RT-06 and the ITA meeting, O5).
- **When:** **later** — ask about data existence now, analyze only if it
  materializes.

### 5. Independent audits (volunteer surveys, photo audits, existing datasets)

**Description.** Compare 311 against independently collected observations:
neighborhood-council or BID cleanliness surveys (Wilshire Center BID
operates inside our Koreatown hotspot zone and appears in the data as an
`Owner`), volunteer photo walks, academic street audits, or any structured
dataset someone else already maintains.

- **Strengths:** independence from both 311 and from us; BIDs in
  particular walk their districts daily and often keep logs; some datasets
  may already exist (zero collection cost).
- **Weaknesses:** coverage of *their* territory only (BIDs are commercial
  corridors — a biased slice); varying methodology and quality; access
  depends on relationships.
- **Effort:** low to discover (add one question to the BID interview),
  medium to reconcile formats if data exists.
- **When:** **only if surfaced** — ask during the Wilshire Center BID
  interview; pursue only if something usable exists.

### 6. Future computer vision (discussion only — no implementation proposed)

**Description.** Continuous or wide-area imagery could estimate coverage
without human walking: dashcam footage from repeated drives of sample
corridors, historical Street View imagery as a sparse time-lapse of known
sites, or (institutionally) city fleet cameras — sanitation trucks already
traverse every street weekly. Detection of curbside bulk items from
imagery is a solved-enough vision problem; the estimate would be
(items detected) vs (items reported) per segment per time window.

- **Strengths:** scales past every labor limit above; repeatable and
  neighborhood-comparable; the trucks-as-sensors idea measures exactly the
  right denominator (every street, weekly).
- **Weaknesses:** privacy and policy questions (faces, plates, people at
  encampments); historical imagery is temporally sparse; a real pipeline is
  an engineering project — squarely against the stay-lightweight principle
  for now; city fleet cameras are an institutional ask far beyond our
  current relationships.
- **Effort:** high (any automated version); trivial only in the degenerate
  manual form ("look at Street View captures of the top 20 sites"), which
  is worth doing and is really method 5.
- **When:** **only if needed** — revisit after field methods produce a
  first estimate; the Street View manual check can happen anytime as a
  cheap supplement.

## What would convince us that reporting coverage is approximately…

**…10%?** Field walks find ~10 visible piles for every one with a matching
report, consistently across strata; crews laugh at the question ("we see
it everywhere, tickets are the tip"); repeat observation shows most piles
appearing and disappearing (scavenged/absorbed) with no report ever filed;
sweep records (method 4) collect an order of magnitude more than tickets
predicted. *Implication if true:* our maps show where reporters live, not
where dumping happens; place-level findings survive only at heavily
reported corners; neighborhood comparisons are mostly meaningless.

**…50%?** Roughly every other observed pile has a report; crews estimate
"about half, depends on the block"; repeat visits show most piles reported
eventually but with long delays, and a large minority cleared informally
first; coverage differs sharply by stratum (high on residential corners,
low in industrial/alley segments). *Implication if true:* citywide totals
are undercounts but structure (recurrence, two-tier hotspots) likely
holds; neighborhood comparisons need stratum-level correction factors.

**…90%?** Nearly every pile encountered already has a ticket (or gets one
within a day or two); crews report rarely encountering unticketed dumping
outside encampment zones; repeat observation shows short report delays;
independent audits (BID logs) track 311 closely in shared territory.
*Implication if true:* 311 is a trustworthy census of visible street
dumping; our findings can be read as statements about reality with modest
caveats.

**…nearly complete?** All of the 90% evidence, plus: the *misses* have an
identifiable, bounded cause (e.g., only fenced private lots and freeway
embankments — jurisdictionally excluded anyway); multiple independent
methods (field, crews, audits) converge within a few points; and coverage
is uniform across neighborhoods (the Studio City / Van Nuys contrast
survives a coverage audit). Near-completeness is a strong claim: we should
require convergence of at least three methods before making it.

Honest prior, stated so future evidence can move it: given the 68%
self-service channel mix, visible-from-sidewalk bias, and crew-discovered
reports being a rounding error (~1%), we'd guess coverage is *moderate and
uneven* — well above 10% at residential curbs, plausibly far below 50% in
industrial and alley segments. The methods above exist to replace that
guess with a number.

---

# Distinguishing Observation, Hypothesis, and Conclusion

The project's working philosophy: **keep separate what we saw, what we can
show, what we suspect, what we're asking, and what we're prepared to
claim.** Blurring these is how civic data analysis goes wrong — a
correlation becomes a headline, a hypothesis becomes a policy
recommendation. Our vocabulary:

- **Observation** — a fact about the *data* (or the street), stated with
  its scope. "X appears in the dataset" — nothing more.
- **Evidence** — observations assembled to bear on a specific claim,
  including the checks that could have falsified it.
- **Hypothesis** — a proposed mechanism that would explain the evidence;
  explicitly labeled, with what would confirm or kill it.
- **Research question** — the tracker-worthy form of a hypothesis: what to
  ask, whom/what to ask it of (data, field, interview — per the project
  principles, every question has a next evidence source).
- **Conclusion** — a claim we are prepared to defend and build on;
  requires evidence from more than one angle, gets an F-number in
  [observatory_findings.md](observatory_findings.md), and remains
  revisable (findings carry dates, and the amendment log records changes).

## Worked example from the illegal dumping investigation

The 4th St & New Hampshire Ave case (F20) traversed all five levels:

- **Observation:** dumping reports at the citywide #1 site stop after
  April 17, 2026 — 115 reports Jan 1–Apr 17, zero afterward (notebook 06).
- **Hypotheses (competing, all initially live):** (a) an encampment at the
  corner was resolved; (b) reporting collapsed (fatigue, or the main
  reporter left); (c) demand migrated to nearby corners; (d) a data
  artifact (geocoding change).
- **Evidence:** `Homeless Encampment` reports within 150m collapsed
  ~100/month → 4/month in the same weeks (supports a); dumping in the
  30–300m ring stayed flat at ~80/month (kills b — neighbors kept
  reporting everything else — and kills c — no migration signal); the
  corner's documented vacant-lot tent cluster and CD10's April activity on
  the same corridor (news coverage) corroborate a; coordinates for
  surrounding reports unchanged (no sign of d).
- **Conclusion (bounded):** the encampment at the corner was resolved in
  late April and the site's report generation stopped — *recorded as F20*.
  Note what is **not** concluded: which intervention did it, and whether
  the street is physically clean. Those remain **research questions**
  (RT-02, RT-03: interview CD10/LSD; visit the site), because case data
  cannot answer them.

The practical rule: notebooks end by sorting their outputs into these
bins — findings (F-numbers) for conclusions, tracker rows (RT-numbers)
for questions, and hypotheses stay labeled as hypotheses in both places
until evidence moves them.
