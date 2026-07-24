<p align="center">
  <img src="https://img.shields.io/badge/Security-Responsible%20Disclosure-0A66C2" alt="Responsible Disclosure">
  <img src="https://img.shields.io/badge/HR%20Data-Synthetic-1E8E5A" alt="Synthetic HR Data">
  <img src="https://img.shields.io/badge/Controls-CodeQL%20%7C%20CI-625BEB" alt="Automated Controls">
</p>

<h1 align="center">🔐 Security & HR Data Privacy</h1>

<p align="center">
  <strong>Responsible disclosure, automated validation and privacy-first workforce analytics.</strong>
</p>

---

## 🧭 Core policy

| Area | Requirement |
|---|---|
| 🛡️ Security reports | Report sensitive issues privately |
| 👥 HR data | Only synthetic records belong in this public repository |
| 🔑 Secrets | Never commit passwords, tokens, keys or credentials |
| 📊 Power BI | Commit only portable source paths; never publish private local paths |
| 💻 Local use | Review scripts and dependencies before running them |

> This is a public portfolio project, not a production HR information system.

---

## 🤖 Automated controls

| Control | Purpose |
|---|---|
| Project validation | Checks required files, schemas, dates, duplicate IDs and notebook hygiene |
| Secret-pattern scanning | Detects common credential and private-key patterns in text files |
| Power BI path validation | Blocks user-home, container and network paths in committed `model.bim` |
| CodeQL | Performs Python static security analysis |
| Dependency review | Blocks vulnerable dependency changes at moderate severity or above |
| Dependabot | Checks Python and GitHub Actions dependencies weekly |
| CODEOWNERS | Assigns repository-owner review to sensitive files and folders |

The recommended GitHub ruleset is documented in [`docs/REPOSITORY_PROTECTION.md`](docs/REPOSITORY_PROTECTION.md).

---

## 🚨 Reporting an issue

Do **not** open a public issue for exposed credentials, real employee data, malicious code, confidential company information or reproducible privacy leaks.

Use the repository owner's private GitHub profile contact method and include:

```text
Issue type:
Affected file:
Commit or version:
Description:
Reproduction steps:
Potential impact:
Suggested fix, if known:
```

```mermaid
flowchart LR
    A[Issue found] --> B{Sensitive?}
    B -->|Yes| C[Report privately]
    B -->|No| D[Open a normal issue]
    C --> E[Assess and fix]
    E --> F[Validate and publish safely]
```

---

## 👥 Prohibited HR data

This repository must not contain:

- real employee identities linked to employment records;
- national ID, passport or tax numbers;
- personal addresses, phone numbers or private emails;
- payroll, bank, medical, disability or biometric information;
- disciplinary or grievance records;
- confidential company information;
- production credentials or internal system details.

All employee records included in this project are synthetic.

---

## 🔑 Secrets and local safety

Never commit:

```text
API keys
Passwords
Tokens
Connection strings
Cloud credentials
Private certificates
.env files
```

Use environment variables and review staged changes before pushing:

```bash
git status
git diff --cached
```

---

## 📈 Power BI path safety

The committed semantic model must use:

```text
__PROJECT_ROOT__/data/processed/...
```

The Windows launchers inject the actual repository path only into the local working copy before Power BI Desktop opens.

Do not commit:

- private usernames;
- internal server addresses;
- confidential network paths;
- employee or customer names;
- embedded credentials;
- generated `.pbix` binaries.

---

## ✅ Pre-push checklist

- [ ] No real employee or confidential company data
- [ ] No passwords, tokens or connection strings
- [ ] No private Power BI or notebook paths
- [ ] Committed `model.bim` uses `__PROJECT_ROOT__`
- [ ] CSV, JSON and Excel outputs reviewed
- [ ] `python scripts/validate_project.py` passes
- [ ] Public documentation states that the data is synthetic

---

## 🧾 Resolved security cases

| Case | Resolution | Release |
|---|---|---|
| [#1 — committed local Power BI paths and missing repository safeguards](https://github.com/samusa099/hossain-group-hr-turnover-analytics-bd/issues/1) | Absolute paths removed; validation, CodeQL, dependency review and ownership controls added | [`v1.2.0`](RELEASE_NOTES_v1.2.0.md) |

---

## 📚 Related documents

- [`README.md`](README.md)
- [`RELEASE_NOTES_v1.2.0.md`](RELEASE_NOTES_v1.2.0.md)
- [`docs/REPOSITORY_PROTECTION.md`](docs/REPOSITORY_PROTECTION.md)
- [`DATASET_USAGE_GUIDE.md`](DATASET_USAGE_GUIDE.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [`SUPPORT.md`](SUPPORT.md)

---

<p align="center">
  <strong>Protect people data before analysing people data.</strong> 🛡️
</p>
