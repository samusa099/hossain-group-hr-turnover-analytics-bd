# Kaggle Publishing Configuration

This folder contains only the GitHub-to-Kaggle publishing configuration. The canonical project files remain in their normal repository locations.

## Source-of-truth model

```text
GitHub repository
        ↓
scripts/prepare_kaggle_dataset.py
        ↓
clean temporary Kaggle package
        ↓
GitHub Actions
        ↓
Kaggle Dataset version
```

The staging package is generated during CI and is not committed to the repository. This prevents duplicate CSV, JSON and notebook copies from becoming outdated.

## Published package

The Kaggle upload contains:

```text
dataset-metadata.json
README.md
DATA_PROVENANCE.md
DATASET_USAGE_GUIDE.md
CITATION.cff
raw.zip
processed.zip
metadata.zip
project.zip
```

Archive contents:

- `raw.zip` — employee-level synthetic source data;
- `processed.zip` — calculated HR analytics tables;
- `metadata.zip` — data dictionary JSON;
- `project.zip` — Kaggle-ready analysis notebook.

## Required GitHub configuration

| Type | Name | Value |
|---|---|---|
| Repository variable | `KAGGLE_USERNAME` | Your exact Kaggle username |
| Repository secret | `KAGGLE_API_TOKEN` | Token generated in Kaggle Settings → API |

See [`docs/KAGGLE_SYNC_NOOB_GUIDE.md`](../docs/KAGGLE_SYNC_NOOB_GUIDE.md) for exact setup and testing steps.
