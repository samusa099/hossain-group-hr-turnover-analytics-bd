# Changelog

All notable changes to **Hossain Group HR Turnover Analytics BD** are documented here.

The project follows a simple portfolio-release convention based on meaningful improvements to data, calculations, documentation, automation, dashboard assets or repository security.

## [Unreleased]

### Security

- Pinned GitHub Actions to immutable commit SHAs
- Disabled persisted checkout credentials in every workflow
- Upgraded checkout, setup-python, CodeQL and dependency-review actions
- Added strict Python dependency auditing
- Expanded the importable `main` ruleset with dependency and notebook checks

### Changed

- Consolidated Dependabot updates into grouped GitHub Actions and analytics-stack pull requests
- Replaced loose Python lower bounds with tested direct-version pins
- Removed unused `openpyxl` from the runtime dependency set
- Split repository validation, dependency audit and notebook execution into independent CI jobs
- Required deterministic generated Power BI and processed-data outputs

### Added

- Bounded source requirements in `requirements.in`
- Headless notebook execution on Python 3.11 and 3.12
- `scripts/execute_notebook_smoke.py`

### Planned

- Voluntary versus involuntary turnover analysis
- New-hire turnover and tenure-band reporting
- Regrettable turnover indicator
- Replacement-cost estimation
- Department retention action tracker
- Extended Power BI dashboard pages

## [1.2.0] - 2026-07-24

### Security

- Removed absolute local filesystem paths from the committed Power BI semantic model
- Added portable `__PROJECT_ROOT__` Power BI source paths
- Added deterministic semantic-model lineage identifiers
- Added secret-pattern, PII-field, notebook-output and unsafe-path validation
- Added CodeQL, dependency review and automated project validation workflows
- Added Dependabot, CODEOWNERS and a security-focused pull-request template
- Expanded `.gitignore` protection for secrets, local environments and binary outputs
- Resolved and closed security issue #1

### Added

- `RELEASE_NOTES_v1.2.0.md`
- `VERSION`
- `docs/REPOSITORY_PROTECTION.md`
- Safe local-path injection through the Windows Power BI launchers
- Power BI `.pbip` and `.pbix` distribution guidance

### Changed

- Power BI Project files remain the source-controlled repository format
- Generated `.pbix` files remain excluded from normal Git commits
- Project validation now checks schemas, duplicate employee IDs, dates, formula-injection prefixes and release version

## [1.1.0] - 2026-07-24

### Added

- Professional GitHub cover and portfolio-style README
- Mermaid analytics workflow
- Mermaid repository structure diagram
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `SUPPORT.md`
- Expanded governance and documentation references

### Changed

- Cover image display width set to 65%
- Repository documentation reorganised for faster navigation
- Project positioning clarified for Bangladesh HR analytics use

## [1.0.0] - 2026-07-24

### Added

- Synthetic employee master dataset
- Formula-driven Excel turnover calculator
- Excel management dashboard
- Monthly company turnover summary
- Department turnover summary
- Exit-reason summary
- Power BI Project source files
- Power BI semantic model and measures
- Python generation and validation scripts
- Kaggle-ready notebook and metadata
- Looker Studio-ready CSV
- Project documentation and data dictionary

### Validation

- Required-file validation passed
- JSON syntax validation passed
- CSV structure validation passed
- Excel formula error scan returned no identified formula errors
- ZIP archive integrity validation passed
