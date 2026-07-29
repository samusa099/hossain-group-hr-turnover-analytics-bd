# Submission Requirements

## Required submission path

Each participant must use exactly one submission directory:

```text
submissions/<github-username>/<submission-id>/
```

Example:

```text
submissions/rahim123/workforce-stability-review/
```

The submission ID must use lowercase letters, numbers and hyphens.

## Required files

### `README.md`

The submission README must identify:

- participant GitHub username;
- submission title;
- primary role;
- secondary role, if applicable;
- final decision owner;
- tools used;
- report filename;
- optional notebook or image files;
- data declaration.

Required declaration:

> **Data declaration: No real employee or confidential company data is included.**

### `report.pdf`

The report is the required management deliverable.

Recommended structure:

1. Executive position
2. Evidence reviewed
3. Findings
4. Competing explanations
5. Evidence and uncertainty classification
6. Policy, governance and legal considerations
7. Data limitations
8. Recommendations
9. 90-day and 180-day plan
10. Measurement framework
11. References

### Optional files

- one `.ipynb` analysis notebook;
- supporting `.png`, `.jpg` or `.jpeg` dashboard images;
- additional `.md` notes.

## Allowed file types

```text
.md
.pdf
.ipynb
.png
.jpg
.jpeg
```

## Prohibited files

Do not submit:

```text
.csv
.xlsx
.xls
.pbix
.zip
.7z
.exe
.bat
.ps1
.env
.json credential files
.pem
.key
kaggle.json
access_token
```

Do not copy the official dataset into the submission directory.

## Size limits

| File type | Maximum size |
|---|---:|
| PDF | 15 MB |
| Notebook | 5 MB |
| Each image | 3 MB |
| README or Markdown file | 256 KB |
| Entire submission | 25 MB |

## Notebook policy

An optional notebook must:

- be valid notebook JSON;
- use notebook format version 4;
- contain no secrets or credentials;
- contain no embedded dataset copy;
- contain no cell attachments;
- have cleared execution outputs before submission.

## Evidence restrictions

Participants may analyse only the existing synthetic project evidence.

Do not add or invent:

- salary records;
- attendance records;
- manager records;
- promotion records;
- performance ratings;
- grievance records;
- productivity figures;
- labour-market figures;
- recruitment or replacement costs;
- real employee or company information.

Use **Insufficient evidence to conclude** where appropriate.

## Pull-request rules

1. Fork the repository.
2. Create a branch named:

```text
submission/<github-username>/<selected-role>
```

3. Modify only your own submission directory.
4. Open one pull request for one submission.
5. Use the case-submission pull-request template.
6. Resolve automated policy failures before requesting review.
7. Do not modify official case, data, workflow, Power BI, notebook, documentation or governance files.

## Review outcome

A submission may be:

- accepted;
- accepted with observations;
- revision required;
- not eligible.

Maintainer feedback may be provided through pull-request comments, inline review and the published rubric.
