# Weyland Atlas

A research and analysis environment for understanding how Los Angeles operates
from a civic maintenance perspective — potholes, sidewalks, trees, street
sweeping, 311 requests, and the like.

This is **not** a production app. It optimizes for asking questions, iterating
quickly, and staying reproducible. It intentionally has no auth, no
deployment, and no services.

## Workflow

Question → Acquire public data → Analyze → Visualize → Develop hypotheses →
Field investigation → Interview stakeholders → repeat.

## Setup

```
conda activate weyland-atlas
jupyter notebook
```

The `weyland-atlas` conda environment holds all dependencies for this project,
kept separate from anything else on this machine.

## Structure

- `notebooks/` — Jupyter notebooks, one per question/investigation
- `data/` — downloaded/raw data (gitignored — not checked into git; notebooks
  should document how to re-fetch it)
- `scripts/` — small reusable helpers, once patterns emerge from notebooks
