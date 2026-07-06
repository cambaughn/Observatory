# Weyland Observatory

A research and analysis environment for understanding how cities operate,
starting with Los Angeles civic maintenance — illegal dumping, graffiti,
311 requests, corridor health, and the like.

This is **not** a startup, product, or production application. It optimizes
for asking questions, iterating quickly, and staying reproducible. It
intentionally has no auth, no deployment, and no services.

See [docs/project_principles.md](docs/project_principles.md) for the guiding
principles and [docs/research_questions.md](docs/research_questions.md) for
the open question backlog.

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

- `analysis/` — reusable analyses, only once duplicated notebook logic
  naturally appears
- `data/raw/` — downloaded source datasets (gitignored; notebooks document
  how to re-fetch)
- `data/processed/` — cleaned/derived datasets (gitignored)
- `docs/` — project documentation
- `field-notes/` — observations from walking neighborhoods, corridors, and
  infrastructure
- `interviews/` — notes from conversations with BIDs, StreetsLA, contractors,
  residents, etc.
- `notebooks/` — exploratory analysis; the primary home for code. Prefer
  notebooks over reusable modules until duplication forces extraction.
- `scripts/` — small helper scripts as needed
