# Support Guide

## Before Requesting Support

Please review the following resources first:

- `README.md` for the complete project overview and quick start;
- `docs/POWER_BI_SETUP.md` for Power BI setup;
- `docs/METRIC_DEFINITIONS.md` for turnover formulas;
- `looker_studio/LOOKER_STUDIO_SETUP.md` for Looker Studio configuration;
- `docs/VALIDATION_REPORT.md` for validation scope and limitations.

Run the validator before reporting a problem:

```bash
python scripts/validate_project.py
```

## Supported Topics

Support requests may cover:

- Excel calculator formulas;
- project folder structure;
- Python generation and validation scripts;
- Power BI Project setup;
- processed CSV outputs;
- Kaggle notebook usage;
- Looker Studio field configuration;
- data dictionary interpretation.

## Creating a Useful Issue

Include:

1. a concise issue title;
2. the affected file or workflow;
3. operating system and software version;
4. exact steps to reproduce;
5. the full error message;
6. expected and actual behaviour;
7. screenshots with confidential information removed;
8. validator output.

## Example

```text
Title: Power BI refresh cannot locate processed CSV
Environment: Windows 11, Power BI Desktop current release, Python 3.11
Command: scripts\run_project.bat
Expected: PBIP opens and refreshes processed tables
Actual: File.Contents path error
Validation: PASS
```

## Not Supported

This repository does not provide:

- legal, tax, or regulatory advice;
- production HRIS implementation support;
- guarantees for organisation-specific turnover benchmarks;
- recovery of corrupted proprietary Power BI files;
- support for publishing real confidential employee data.

## Data Privacy Reminder

Never attach real employee records, payroll details, medical information, identification documents, credentials, or internal company files to a public issue.

## Response Expectations

This is an independently maintained portfolio project. Responses are best-effort and may depend on the clarity, reproducibility, and scope of the request.
