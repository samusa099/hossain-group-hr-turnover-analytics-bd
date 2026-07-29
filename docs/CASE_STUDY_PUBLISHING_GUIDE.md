# Case Study Publishing Guide

## Purpose

This guide publishes the Hossain Group role-based workforce stability case without changing the employee-data source of truth, duplicating analytical files or exposing participant submissions in the Kaggle dataset package.

## Publication layers

| Layer | Published content | Excluded content |
|---|---|---|
| GitHub repository | Official case, source evidence, project files, validation, governance and controlled submission area | Secrets, generated `.pbix`, real employee data |
| GitHub Release | Versioned release notes, manifest and immutable source snapshot | Participant work unless separately reviewed and merged |
| Kaggle Dataset | Approved dataset, processed tables, metadata, notebook, usage documentation and official case materials | `.github/`, rulesets, submissions, Power BI binaries and credentials |

## Pre-publication checklist

### 1. Verify the official case

Confirm that the following files exist:

```text
case-study/README.md
case-study/CASE_NARRATIVE.md
case-study/MANAGEMENT_CONTEXT.md
case-study/EXECUTIVE_MANDATE.md
case-study/ROLE_TRACKS.md
case-study/SUBMISSION_REQUIREMENTS.md
case-study/POLICY_AND_LEGAL_RESEARCH.md
case-study/RUBRIC.md
case-study/variants/managing-director.md
case-study/variants/hr-business-partner.md
case-study/variants/people-analytics.md
case-study/variants/operations-finance.md
case-study/variants/policy-governance.md
```

The public case must not contain a model answer, solved department diagnosis, difficulty percentage, mandatory dashboard answer, completed root-cause tree or pre-calculated financial benefit.

### 2. Verify the evidence boundary

Quantitative findings must remain grounded in the existing project evidence:

```text
data/raw/employee_master.csv
data/processed/
data/metadata/data_dictionary.json
excel/
powerbi/
notebooks/
looker_studio/
```

Do not add another employee dataset for the case.

### 3. Validate controlled submissions

The accepted external path is:

```text
submissions/<github-username>/<submission-id>/
```

Each participant pull request must contain:

```text
README.md
report.pdf
```

Optional cleared analysis:

```text
analysis.ipynb
*.png
```

Run or confirm the required check:

```text
Validate participant submission scope
```

### 4. Import the ruleset

Repository administrator path:

```text
Settings
→ Rules
→ Rulesets
→ New ruleset
→ Import a ruleset
```

Import:

```text
docs/Protect_Case_Submission_Ruleset.json
```

Before activating, confirm that the repository has an eligible reviewer for the required CODEOWNERS approval. A solo maintainer should add a trusted collaborator or deliberately adjust the approval requirement before activation; otherwise the maintainer's own pull requests may become unmergeable.

### 5. Configure Kaggle publication

Under **Settings → Secrets and variables → Actions**, configure:

```text
Repository variable: KAGGLE_USERNAME
Repository secret: KAGGLE_API_TOKEN
```

The Kaggle workflow validates the canonical project, builds the clean package and either creates the dataset or publishes a new version.

Expected public package:

```text
raw.zip
processed.zip
metadata.zip
project.zip
case-study.zip
README.md
DATA_PROVENANCE.md
DATASET_USAGE_GUIDE.md
CITATION.cff
```

### 6. Verify release metadata

For this release:

```text
VERSION                         = 1.3.0
CITATION.cff version            = 1.3.0
release/RELEASE_VERSION         = v1.3.0
RELEASE_NOTES_v1.3.0.md         = present
release/V1.3.0_RELEASE_MANIFEST.md = present
```

### 7. Merge the protected release pull request

Required outcomes before merge:

- project validation passes;
- Python dependency audit passes;
- notebook execution passes;
- CodeQL and dependency review pass;
- portfolio security checks pass;
- Kaggle package preview passes;
- case-submission policy passes;
- all review conversations are resolved.

## Automated publication after merge

### GitHub Release

`.github/workflows/publish-release.yml` validates release consistency and creates `v1.3.0` on the exact merge commit. The workflow is idempotent and does not create a duplicate release when the declared version already exists.

### Kaggle Dataset

`.github/workflows/sync-kaggle.yml` runs when approved case or package files change. Pull requests create a package-preview artifact only. A push to `main` publishes only when the Kaggle repository variable and secret are configured.

## Post-publication verification

Confirm:

- the GitHub Release tag points to the intended main-branch commit;
- the release notes render correctly;
- Kaggle contains `case-study.zip` and the approved evidence archives;
- no `submissions/`, `.github/`, ruleset, `.pbix`, credential or private-key file appears in Kaggle;
- the case landing page links work;
- participant pull requests trigger the scope-validation check;
- repository rules remain active and do not accidentally block all maintainer work.

## Rollback

When a publication problem is found:

1. do not rewrite or force-push protected history;
2. fix the source through a new branch and pull request;
3. publish a corrected patch release or Kaggle dataset version;
4. document the correction in `CHANGELOG.md` and release notes;
5. revoke and rotate any credential immediately if exposure is suspected.
