# Repository Protection Baseline

This document records the recommended protection settings for the `main` branch, release tags and the automated safeguards committed to the repository.

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

## Protection enforced by the main ruleset

- require a pull request before merging;
- require all review conversations to be resolved;
- require the branch to be up to date before merging;
- require repository validation, dependency audit, notebook execution, CodeQL and dependency review;
- block force pushes;
- block branch deletion;
- require linear history.

For this solo-maintainer repository, required approvals remain `0`. Increase the value to `1` after adding a trusted reviewer.

## Importable release-tag ruleset

Use [`Protect_Release_Tags_Ruleset.json`](Protect_Release_Tags_Ruleset.json) to protect version tags that match `v*`, including tags such as `v1.2.0`.

### Tag import steps

1. Open **Settings → Rules → Rulesets**.
2. Select **New ruleset → Import a ruleset**.
3. Download and select `docs/Protect_Release_Tags_Ruleset.json`.
4. Confirm the ruleset name is **Protect release tags**.
5. Confirm the target is **Tags**, the pattern is `v*`, and enforcement is **Active**.
6. Click **Create**.

## Protection enforced by the tag ruleset

- allows new version tags to be created;
- prevents an existing `v*` tag from being moved to another commit;
- prevents an existing `v*` tag from being deleted;
- keeps published release references immutable and auditable.

The ruleset intentionally does not restrict tag creation. Create a release tag only after the target commit has passed the required pull-request checks. If a release tag is created incorrectly, temporarily disable the tag ruleset, correct the tag, and reactivate the ruleset.

## Important limitation

Repository rulesets are GitHub administrative settings. Committing either JSON file does not activate protection by itself; an administrator must import each file and click **Create** once in the repository settings.

## Power BI protection

The committed semantic model must contain only the portable `__PROJECT_ROOT__` token. The local launchers inject the working-copy path into the local model before Power BI Desktop opens. A `.pbix` file is a generated binary and remains excluded from normal source control.
