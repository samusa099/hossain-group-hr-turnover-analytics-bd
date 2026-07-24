<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.2.0-0A66C2" alt="Release v1.2.0">
  <img src="https://img.shields.io/badge/Security-Hardened-1E8E5A" alt="Security hardened">
  <img src="https://img.shields.io/badge/Power%20BI-PBIP%20Source-F2C811" alt="Power BI PBIP source">
</p>

# 🔐 Release Notes — v1.2.0

**Release date:** 24 July 2026  
**Theme:** Repository security, code protection and safe Power BI distribution

---

## ✅ Security case resolved

This release resolves the tracked local-path exposure and repository-protection case documented in [issue #1](https://github.com/samusa099/hossain-group-hr-turnover-analytics-bd/issues/1).

### Remediation completed

- replaced committed absolute Power BI source paths with `__PROJECT_ROOT__`;
- made Power BI lineage identifiers deterministic to prevent unnecessary model churn;
- configured the Windows launchers to inject the real local repository path only at runtime;
- expanded validation for CSV schemas, employee IDs, dates, notebook outputs, secret patterns and unsafe paths;
- added GitHub Actions validation, CodeQL and dependency review;
- added Dependabot, CODEOWNERS and a security-focused pull-request template;
- expanded `.gitignore` coverage for secrets, virtual environments, local files and binaries.

No active credential leak, production secret or real confidential employee dataset was identified during the targeted review.

---

## 📊 Power BI file upload and distribution

### Repository source of truth

The GitHub repository stores the source-control-friendly Power BI Project files:

```text
powerbi/Hossain_Group_Turnover.pbip
powerbi/Hossain_Group_Turnover.Report/
powerbi/Hossain_Group_Turnover.SemanticModel/
```

The committed `model.bim` uses the safe placeholder:

```text
__PROJECT_ROOT__/data/processed/...
```

This prevents private usernames, temporary container paths and confidential network locations from being published.

### Create the local Power BI file

On Windows, run one of these launchers:

```bat
scripts\run_project.bat
```

```powershell
.\scripts\run_project.ps1
```

The launcher:

1. sets the current repository as the local Power BI data root;
2. regenerates processed datasets and the local semantic model;
3. opens `Hossain_Group_Turnover.pbip` in Power BI Desktop.

After Power BI Desktop opens:

1. select **Refresh**;
2. confirm the visuals and measures;
3. select **File → Save As**;
4. save an upload-ready `.pbix` file locally.

### Why `.pbix` is not committed

`.pbix` is a generated binary file and is intentionally excluded through `.gitignore` because it is not suitable for readable source review or normal Git version control.

Use the `.pbip` project for GitHub collaboration. When a `.pbix` copy is required for portfolio delivery, upload it manually as a GitHub Release asset, Google Drive file or other controlled distribution file after validating that it contains no confidential data or private local paths.

---

## 🛡️ Code-protection baseline

The repository now includes:

- automated project validation on pushes and pull requests;
- scheduled and pull-request CodeQL analysis;
- dependency review for pull requests;
- weekly Dependabot checks for Python and GitHub Actions;
- explicit ownership for security-sensitive paths;
- documented recommended `main` branch rules.

Repository-level branch rules must still be enabled by the repository owner in GitHub Settings because those administrative settings are not stored as ordinary repository files.

---

## 🔄 Upgrade instructions

```bash
git pull origin main
python -m pip install -r requirements.txt
python scripts/generate_powerbi_project.py
python scripts/validate_project.py
```

For local Power BI refresh, use the Windows launcher rather than running the generator directly.

---

## 📌 Compatibility

- No employee-data schema change
- No turnover-formula change
- No dashboard KPI change
- Existing Excel, Kaggle and Looker Studio workflows remain supported
