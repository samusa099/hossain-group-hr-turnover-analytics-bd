# Case Submission Protection

## Protection model

GitHub does not provide folder-level write permission for individual external contributors inside one repository. This project therefore uses a controlled contribution model:

```text
Fork
→ submission branch
→ pull request
→ automated scope validation
→ CODEOWNERS review
→ protected main branch
```

External contributors do not receive direct write access to the main repository.

## Automated control

Workflow:

```text
.github/workflows/validate-case-submission.yml
```

Required check name:

```text
Validate participant submission scope
```

The workflow runs from the trusted base repository through `pull_request_target`. It does not check out or execute untrusted participant code.

For external contributors, it validates:

- branch naming;
- participant-specific path scope;
- one submission directory per pull request;
- required `README.md` and `report.pdf`;
- allowed extensions;
- file-size limits;
- PDF signature;
- notebook JSON and output policy;
- secret and private-key patterns;
- required data declaration.

Trusted owner, member and collaborator pull requests may modify normal project paths. A trusted pull request that uses a `submission/` branch is still validated as a participant submission.

## CODEOWNERS

The official case and submission directories require review from:

```text
@samusa099
```

Protected paths:

```text
/case-study/
/submissions/
/.github/
/scripts/
/data/metadata/
/powerbi/
```

## Required branch rules

The `main` branch ruleset should require:

- pull requests before merging;
- review conversation resolution;
- linear history;
- branch deletion protection;
- force-push protection;
- CODEOWNERS review when a reviewer is available;
- required check: `Validate participant submission scope`;
- existing security, validation, CodeQL and dependency-review checks.

## Import package

The importable ruleset JSON is distributed outside the repository tree in a ZIP package. It is not committed to the project source.

Repository administrators must import it manually under:

```text
Settings
→ Rules
→ Rulesets
→ New ruleset
→ Import a ruleset
```

Confirm:

```text
Name: Protect main and case submissions
Target: Default branch
Enforcement: Active
```

## Maintainer review

Automated validation establishes eligibility; it does not establish analytical quality.

The maintainer may:

- request changes;
- provide inline feedback;
- assess the submission against `case-study/RUBRIC.md`;
- accept the submission;
- close a submission that remains outside policy.
