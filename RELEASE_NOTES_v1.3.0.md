<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.3.0-7B61FF" alt="Release v1.3.0">
  <img src="https://img.shields.io/badge/Case-Role--Based%20Simulation-625BEB" alt="Role-based simulation">
  <img src="https://img.shields.io/badge/Submissions-Protected-1E8E5A" alt="Protected submissions">
  <img src="https://img.shields.io/badge/Data%20Schema-Unchanged-2EA44F" alt="Data schema unchanged">
</p>

# v1.3.0 — Role-Based Workforce Stability Case

> A publication-ready release that turns the existing synthetic HR analytics project into a controlled, evidence-led management simulation without duplicating the source dataset.

| Release detail | Value |
|---|---|
| **Release date** | 29 July 2026 |
| **Primary scope** | Case design, role tracks, governance, protected submissions and publication automation |
| **Employee schema** | Unchanged |
| **Turnover formulas** | Unchanged |
| **Dashboard KPIs** | Unchanged |
| **GitHub source of truth** | Preserved |
| **Kaggle package** | Expanded with approved official case materials |

## ✨ Release highlights

- introduces a narrative-led workforce stability and governance review;
- supports Managing Director, HR Business Partner, People Analytics, Operations and Finance, Policy and Governance, and hybrid participation tracks;
- requires participants to distinguish verified evidence, plausible but unverified explanation, allegation, legal-research need and evidence limitation;
- requires a management-ready PDF report and permits an optional cleared notebook;
- creates a controlled contribution path under `submissions/<github-username>/<submission-id>/`;
- adds automated submission-scope validation without executing untrusted participant code;
- adds an import-ready branch ruleset for protected case submissions;
- publishes approved case-study Markdown files in the clean Kaggle dataset package;
- adds a guarded, idempotent GitHub Release publisher.

## 🧭 Case objective

Participants must prepare a defensible management position that separates:

1. what the current evidence supports;
2. what remains uncertain;
3. what additional records or official research are required;
4. which actions management can approve now;
5. which actions should wait for further investigation;
6. who owns the 90-day and 180-day response.

The public case does not disclose a model answer, a solved root-cause tree, a required dashboard layout, a difficulty percentage or pre-calculated financial benefit.

## 👥 Role tracks

| Track | Primary emphasis |
|---|---|
| Managing Director | Enterprise risk, accountability and intervention approval |
| HR Business Partner | Department diagnosis, employee relations and action design |
| People Analytics | Data quality, metric validation, segmentation and analytical limits |
| Operations and Finance | Workforce continuity, replacement pressure and resource prioritisation |
| Policy and Governance | Policy consistency, auditability, legal alignment and control design |
| Hybrid | Two connected perspectives with one declared primary decision-maker |

## 🔒 Controlled submissions

External participants use:

```text
submission/<github-username>/<selected-role>
```

and may modify only:

```text
submissions/<github-username>/<submission-id>/
```

Required submission files:

```text
README.md
report.pdf
```

Optional files:

```text
analysis.ipynb
supporting-dashboard.png
```

The policy gate checks path scope, author ownership, one-submission-per-pull-request, required files, allowed extensions, file sizes, PDF signature, notebook JSON and output policy, secret patterns and the synthetic-data declaration.

## 🇧🇩 Legal and policy research boundary

No unverified labour-law conclusion is embedded in the dataset or case narrative. Participants must verify current legal or regulatory issues from official sources applicable on the submission date and explain:

- relevance to the case;
- whether the existing dataset can assess the issue;
- which additional evidence is required;
- which policy, approval, documentation or reporting control management should introduce.

## 📦 Publication structure

GitHub remains the complete source of truth. Kaggle receives only the approved publication package:

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

Participant submissions, repository administration files, workflow files, secrets and Power BI binaries are not copied into the Kaggle dataset package.

## 🛡️ Repository protection

This release includes:

- `Validate participant submission scope`;
- CODEOWNERS coverage for official case and submission paths;
- import-ready case-submission branch ruleset;
- existing project validation and notebook execution;
- CodeQL and dependency review;
- Gitleaks, dependency audit and portfolio file-policy checks;
- immutable GitHub Action references and least-privilege permissions.

## 🚀 Publication sequence

1. Merge the release pull request after all required checks pass.
2. The GitHub Release workflow validates version consistency and publishes `v1.3.0` idempotently.
3. The Kaggle workflow builds and validates the clean package.
4. When `KAGGLE_USERNAME` and `KAGGLE_API_TOKEN` are configured, the workflow creates or versions the public Kaggle dataset.
5. Import `docs/Protect_Case_Submission_Ruleset.json` under repository rules and confirm required checks.

## ✅ Compatibility

- Existing Excel workflow remains supported.
- Existing Power BI PBIP workflow remains supported.
- Existing Python analysis and validation remain supported.
- Existing Looker Studio workflow remains supported.
- Existing employee records and calculated tables remain unchanged.
- No migration of formulas, schemas or dashboard measures is required.
