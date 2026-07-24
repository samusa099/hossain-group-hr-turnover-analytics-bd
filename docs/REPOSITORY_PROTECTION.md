# Repository Protection Baseline

This document records the recommended protection settings for the `main` branch and the automated safeguards committed to the repository.

## Automated controls included

| Control | Repository file |
|---|---|
| Project, schema, secret-pattern and path validation | `.github/workflows/security-and-validation.yml` |
| Python static security analysis | `.github/workflows/codeql.yml` |
| Pull-request dependency review | `.github/workflows/dependency-review.yml` |
| Dependency update automation | `.github/dependabot.yml` |
| Ownership of sensitive paths | `.github/CODEOWNERS` |
| Pull-request safety checklist | `.github/pull_request_template.md` |

## Recommended `main` ruleset

Enable these settings in **Settings → Rules → Rulesets**:

- require a pull request before merging;
- require the validation, CodeQL and dependency-review checks when applicable;
- require conversation resolution;
- block force pushes;
- block branch deletion;
- require linear history;
- require signed commits when practical;
- apply the ruleset to administrators, with an owner-only emergency bypass.

For a solo-maintainer repository, required approvals may remain `0`; increase to `1` when a trusted reviewer is available.

## Power BI protection

The committed semantic model must contain only the portable `__PROJECT_ROOT__` token. The local launchers inject the working-copy path into the local model before Power BI Desktop opens. A `.pbix` file is a generated binary and remains excluded from normal source control.
