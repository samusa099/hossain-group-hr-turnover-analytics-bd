## Purpose

Describe the HR, analytics, documentation or security reason for this change.

## Changes

- 

## Validation

- [ ] `python scripts/generate_powerbi_project.py`
- [ ] `python scripts/validate_project.py`
- [ ] No real employee or confidential company data is included
- [ ] No passwords, tokens, private local paths or connection strings are included
- [ ] Power BI, Excel, notebook and processed-data outputs were reviewed where affected
- [ ] Documentation and `CHANGELOG.md` were updated where required

## Power BI files

- [ ] The source-controlled `.pbip` project remains the repository source of truth
- [ ] No `.pbix` binary was committed
- [ ] Committed `model.bim` uses the `__PROJECT_ROOT__` placeholder

## Screenshots or evidence

Add dashboard screenshots, validation output or other supporting evidence when relevant.
