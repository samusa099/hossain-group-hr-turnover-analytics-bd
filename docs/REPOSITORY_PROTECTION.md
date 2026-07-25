# Repository Protection Baseline

This document records the recommended protection settings for the `main` branch and the automated safeguards committed to the repository.

## Automated controls included

| Control | Repository file |
|---|---|
| Project, schema, secret-pattern and path validation | `.github/workflows/security-and-validation.yml` |
| Pinned-dependency vulnerability audit | `.github/workflows/security-and-validation.yml` |
| Python 3.11 and 3.12 notebook execution | `.github/workflows/security-and-validation.yml` |
| Python static security analysis | `.github/workflows/codeql.yml` |
| Pull-request dependency review | `.github/workflows/dependency-review.yml` |
| Grouped dependency update automation | `.github/dependabot.yml` |
| Ownership of sensitive paths | `.github/CODEOWNERS` |
| Pull-request safety checklist | `.github/pull_request_template.md` |

The controls are exercised through pull requests before protected changes are merged into `main`.

## Importable `main` ruleset

Use [`Protect_Main_Branch_Ruleset.json`](Protect_Main_Branch_Ruleset.json) to configure the repository protection without entering every rule manually.

### Import steps

1. Open **Settings → Rules → Rulesets**.
2. Select **New ruleset → Import a ruleset**.
3. Download and select `docs/Protect_Main_Branch_Ruleset.json`.
4. Confirm the ruleset name is **Protect main branch**.
5. Confirm the target is the **default branch** and enforcement is **Active**.
6. Review the required checks and click **Create**.

The imported ruleset requires these successful pull-request checks:

- `Validate data, code and Power BI sources`
- `Audit Python dependencies`
- `Execute analytics notebook (3.11)`
- `Execute analytics notebook (3.12)`
- `Analyze Python`
- `Review dependency changes`

## Protection enforced by the ruleset

- require a pull request before merging;
- require all review conversations to be resolved;
- require the branch to be up to date before merging;
- require repository validation, dependency audit, notebook execution, CodeQL and dependency review;
- block force pushes;
- block branch deletion;
- require linear history.

For this solo-maintainer repository, required approvals remain `0`. Increase the value to `1` after adding a trusted reviewer.

## Important limitation

Repository rulesets are GitHub administrative settings. Committing the JSON file does not activate protection by itself; an administrator must import the file and click **Create** once in the repository settings.

## Power BI protection

The committed semantic model must contain only the portable `__PROJECT_ROOT__` token. The local launchers inject the working-copy path into the local model before Power BI Desktop opens. A `.pbix` file is a generated binary and remains excluded from normal source control.
