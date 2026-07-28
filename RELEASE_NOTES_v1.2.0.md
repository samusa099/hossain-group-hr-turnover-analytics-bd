<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.2.0-7B61FF" alt="Release v1.2.0">
  <img src="https://img.shields.io/badge/Security-Hardened-1E8E5A" alt="Security hardened">
  <img src="https://img.shields.io/badge/Power%20BI-PBIP%20Source-F2C811" alt="Power BI PBIP source">
  <img src="https://img.shields.io/badge/Compatibility-No%20Data%20Schema%20Change-2EA44F" alt="No data schema change">
</p>

# v1.2.0 — Security Hardening & Power BI Delivery

> A stable portfolio release focused on repository protection, deterministic Power BI sources, and safe `.pbix` distribution.

| Release detail | Value |
|---|---|
| **Release date** | 24 July 2026 |
| **Primary scope** | Security, CI, code protection, Power BI delivery |
| **Employee schema** | Unchanged |
| **Turnover formulas** | Unchanged |
| **Dashboard KPIs** | Unchanged |

## ✨ Highlights

- resolved the tracked local-path exposure case in [issue #1](https://github.com/samusa099/hossain-group-hr-turnover-analytics-bd/issues/1);
- replaced committed absolute Power BI paths with the portable `__PROJECT_ROOT__` token;
- added deterministic model generation and stronger repository validation;
- introduced GitHub Actions validation, CodeQL, dependency review, Dependabot, and CODEOWNERS;
- documented a safe workflow for creating and distributing an upload-ready `.pbix` file.

## 🔐 Security hardening

The release adds validation for CSV schemas, employee IDs, dates, notebook outputs, secret patterns, unsafe paths, and generated Power BI content.

No active credential leak, production secret, or real confidential employee dataset was identified during the targeted review.

## 📊 Power BI delivery

| File type | Purpose | Git policy |
|---|---|---|
| `.pbip` project | Reviewable Power BI source | Stored in the repository |
| `.pbix` file | Generated portfolio-delivery binary | Upload as a Release asset; do not commit |

Repository source:

```text
powerbi/Hossain_Group_Turnover.pbip
powerbi/Hossain_Group_Turnover.Report/
powerbi/Hossain_Group_Turnover.SemanticModel/
```

The committed semantic model uses:

```text
__PROJECT_ROOT__/data/processed/...
```

### Create the `.pbix`

1. Run `scripts\run_project.bat` or `.\scripts\run_project.ps1` on Windows.
2. Wait for Power BI Desktop to open the `.pbip` project.
3. Select **Refresh** and verify the visuals and measures.
4. Select **File → Save As**.
5. Save as `Hossain_Group_HR_Turnover_Analytics_v1.2.0.pbix`.
6. Upload the validated file as a GitHub Release asset or through another controlled distribution channel.

## 🛡️ Repository protection

This release includes:

- project and data validation;
- Python dependency auditing;
- notebook execution on Python 3.11 and 3.12;
- CodeQL analysis;
- pull-request dependency review;
- grouped Dependabot updates;
- import-ready branch and tag protection rulesets.

GitHub rulesets remain administrative settings and must be activated once through **Settings → Rules → Rulesets**.

## 🔄 Upgrade

```bash
git pull origin main
python -m pip install -r requirements.txt
python scripts/generate_powerbi_project.py
python scripts/validate_project.py
```

For local Power BI refresh, use the Windows launcher so the repository path is injected only at runtime.

## ✅ Compatibility

- Existing Excel workflow remains supported.
- Existing Kaggle notebook workflow remains supported.
- Existing Looker Studio workflow remains supported.
- No employee-data schema, turnover-formula, or dashboard-KPI migration is required.
