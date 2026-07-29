# Changelog

All notable changes to **Hossain Group HR Turnover Analytics BD** are documented here.

The project follows a simple portfolio-release convention based on meaningful improvements to data, calculations, documentation, automation, dashboard assets or repository security.

## [Unreleased]

### Planned

- Voluntary versus involuntary turnover analysis
- New-hire turnover and tenure-band reporting
- Regrettable turnover indicator
- Replacement-cost estimation
- Department retention action tracker
- Extended Power BI dashboard pages

## [1.3.0] - 2026-07-29

### Added

- Role-based workforce stability and governance case study
- Managing Director, HR Business Partner, People Analytics, Operations and Finance, Policy and Governance, and hybrid role tracks
- Executive mandate, management context, submission requirements, legal-research guidance and assessment rubric
- Controlled participant submission area under `submissions/<github-username>/<submission-id>/`
- Dedicated pull-request template and CODEOWNERS coverage for official case and submission paths
- Automated `Validate participant submission scope` policy gate
- Import-ready `docs/Protect_Case_Submission_Ruleset.json`
- Case-study files in the clean Kaggle publication package
- Release manifest and automated GitHub Release publisher

### Security

- Participant pull requests are validated without checking out or executing untrusted contribution code
- External submissions are restricted by branch, path, extension, file-size, notebook, PDF and secret-scanning controls
- Existing portfolio security hardening remains active, including CodeQL, Gitleaks, dependency audit, path containment, XLSX validation and CSV formula-injection checks

### Changed

- Project scope expanded from a turnover-calculation portfolio into a controlled management simulation
- GitHub remains the source of truth while Kaggle receives only approved case, evidence, metadata, documentation and notebook files
- Release and citation metadata updated to version 1.3.0

### Compatibility

- No employee-data schema change
- No turnover-formula change
- No dashboard-KPI change
- Existing Excel, Power BI, Python, Kaggle and Looker Studio workflows remain supported

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
