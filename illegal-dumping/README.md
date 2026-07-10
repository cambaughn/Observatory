# Illegal Dumping

Where does illegal dumping concentrate in Los Angeles, why does it recur at
specific places, and what actually makes a chronic site stop?

The Observatory's first research domain. Core results so far: dumping is a
**place problem** (81% of reports at recurring 20m locations, two-tier
hotspot structure), response is fast — persistence, not response failure,
is the phenomenon — and a site-anatomy hypothesis (bin-staging corners +
semi-private geometry at multifamily frontage) is under active field
testing. Findings F13–F21 in
[docs/observatory_findings.md](../docs/observatory_findings.md).

## Where things live

- [questions.md](questions.md) — open research questions for this domain
- [roadmap.md](roadmap.md) — the research tracker: one row per tracked
  question (RT-numbers), with status and next action; **start here** to see
  what's active
- [sources.md](sources.md) — datasets, documents, and external references
  this domain draws on
- `docs/` — domain documents ([field_program.md](docs/field_program.md) is
  the phone-friendly field guide)
- `analysis/` — reusable analysis code, only once duplicated notebook logic
  naturally appears
- `data/raw/`, `data/processed/` — domain-derived datasets (gitignored;
  notebooks document how to regenerate). Cross-domain source data (the
  MyLA311 extract, boundaries, census) lives in `../shared/datasets/`.
- `field-notes/` — site observations (`maps/` holds the field-day HTML maps)
- `interviews/` — stakeholder conversation notes
- `notebooks/` — the primary home for analysis. Numbered 04–07: this domain
  grew out of the general MyLA311 investigation, whose notebooks 00–03 now
  live in `../shared/notebooks/`.
- `scripts/` — helpers (`build_field_maps.py`, `build_field_area_context.py`);
  run them from this directory

## Conventions

Analyses follow [docs/analysis_standards.md](../docs/analysis_standards.md)
(filters, outcome classes, stated assumptions) and the workflow in
[docs/project_principles.md](../docs/project_principles.md). Field visits
and interviews start from the templates in `../shared/templates/`.
