# Weyland Observatory

A research and analysis environment for understanding how cities operate,
starting with Los Angeles civic maintenance — illegal dumping, graffiti,
311 requests, corridor health, and the like.

This is **not** a startup, product, or production application. It optimizes
for asking questions, iterating quickly, and staying reproducible. It
intentionally has no auth, no deployment, and no services.

See [docs/project_principles.md](docs/project_principles.md) for the guiding
principles and [docs/research_questions.md](docs/research_questions.md) for
the cross-domain question backlog.

## Workflow

Question → Data → Analysis → Visualization → Hypothesis →
Field Investigation → Stakeholder Conversation → New Question.

## Setup

```
conda activate weyland-observatory
jupyter notebook
```

The `weyland-observatory` conda environment holds all dependencies for this
project, kept separate from anything else on this machine.

## Structure

The repository is organized around **research domains**. Each domain is a
self-contained workspace; everything cross-domain lives in `docs/` (how we
work) and `shared/` (what we work with). The domain list stays flat: topics
are promoted to domains — and domains grouped under parent directories —
only per the rules in
[docs/project_principles.md](docs/project_principles.md) ("How the
repository grows").

- `docs/` — Observatory-wide documentation:
  [project_principles.md](docs/project_principles.md),
  [analysis_standards.md](docs/analysis_standards.md),
  [research_methods.md](docs/research_methods.md),
  [observatory_findings.md](docs/observatory_findings.md) (the global
  findings ledger — F-numbers are unique across all domains),
  [research_questions.md](docs/research_questions.md) (cross-domain backlog)
- `shared/` — cross-domain infrastructure, currently mostly the MyLA311
  dataset platform:
  - `shared/datasets/raw/` — downloaded source datasets (gitignored;
    scripts and dataset docs record how to re-fetch)
  - `shared/datasets/processed/` — cross-domain derived datasets (gitignored)
  - `shared/references/` — dataset documentation (MyLA311 schema and
    operational model)
  - `shared/scripts/` — data acquisition/build scripts
  - `shared/notebooks/` — notebooks 00–03: environment check and the
    general MyLA311 investigation every domain builds on
  - `shared/templates/` — field-visit and interview templates
- `illegal-dumping/` — the first research domain
  ([README](illegal-dumping/README.md))
- `homelessness/` — the next research domain (scaffolded, not yet started)

### Inside a research domain

Every domain follows the same layout:

| Path | Purpose |
|---|---|
| `README.md` | What the domain studies, state of play, where things live |
| `questions.md` | Open research questions |
| `roadmap.md` | The research tracker: tracked questions, status, next action |
| `sources.md` | Datasets, documents, people, and external references |
| `docs/` | Domain documents (field guides, write-ups) |
| `analysis/` | Reusable analysis code, extracted only when duplication forces it |
| `data/raw/`, `data/processed/` | Domain-specific datasets (gitignored; regenerable) |
| `field-notes/` | Observations from walking neighborhoods and sites |
| `interviews/` | Notes from stakeholder conversations |
| `notebooks/` | Exploratory analysis; the primary home for code |
| `scripts/` | Small helper scripts, run from the domain directory |
