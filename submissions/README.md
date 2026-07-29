# Participant Submissions

This folder is the only repository area available for external case-study submissions.

## Required path

```text
submissions/<github-username>/<submission-id>/
```

Example:

```text
submissions/rahim123/workforce-stability-review/
```

## Required files

```text
README.md
report.pdf
```

Optional files:

```text
analysis.ipynb
supporting-dashboard.png
additional-notes.md
```

## Contribution process

1. Fork the repository.
2. Create a branch named `submission/<github-username>/<selected-role>`.
3. Add files only inside your own submission directory.
4. Open a pull request to `main`.
5. Select the case-submission pull-request template.
6. Wait for the automated submission-scope check.
7. Resolve policy failures before requesting maintainer review.

## Automatic protection

External pull requests are rejected when they:

- modify files outside the participant’s own submission path;
- add blocked file types;
- exceed file-size limits;
- include dataset copies;
- include notebook outputs or invalid notebook JSON;
- include secrets, tokens or private keys;
- omit the required README or PDF report.

## Important limitation

A GitHub ruleset cannot provide folder-level write permission by itself. Protection is implemented through:

- fork-based contributions;
- pull requests;
- automated path validation;
- CODEOWNERS review;
- protected `main` branch settings.

## Official requirements

Read:

- [`../case-study/SUBMISSION_REQUIREMENTS.md`](../case-study/SUBMISSION_REQUIREMENTS.md)
- [`../case-study/RUBRIC.md`](../case-study/RUBRIC.md)
- [`SUBMISSION_TEMPLATE.md`](SUBMISSION_TEMPLATE.md)

Do not add real employee or confidential company information.
