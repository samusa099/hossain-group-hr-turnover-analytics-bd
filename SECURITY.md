# Security and Data Privacy Policy

## Supported Scope

This repository is a portfolio and learning project. Security support applies to the current default branch and the latest published project files.

## Reporting a Security or Privacy Issue

Please do not create a public issue for vulnerabilities involving credentials, malicious code execution, sensitive employee data, or privacy exposure.

Report privately through the repository owner's GitHub profile contact method and include:

- a clear description of the issue;
- affected file or component;
- reproduction steps;
- expected impact;
- suggested remediation, when available.

Please allow reasonable time for investigation before public disclosure.

## Sensitive HR Data

This public repository must never contain:

- real employee names linked to employment records;
- national identification numbers;
- personal addresses or phone numbers;
- payroll bank details;
- medical or disability information;
- disciplinary records;
- authentication credentials;
- confidential company information.

All included employee records are synthetic. Anyone adapting this project for organisational use must apply appropriate access control, anonymisation, retention, encryption, and internal approval procedures.

## Secrets and Credentials

Do not commit:

- API keys;
- passwords;
- tokens;
- database connection strings;
- cloud credentials;
- local environment secrets.

Use environment variables or an excluded local configuration file instead.

## Dependency and File Safety

Before running scripts:

1. review the source code;
2. use a virtual environment;
3. install dependencies from `requirements.txt`;
4. keep Python, Power BI Desktop, and spreadsheet software updated;
5. scan downloaded archives when working outside GitHub.

## Power BI and Local Paths

The Power BI generator writes local file paths into the semantic-model source. Do not commit paths containing private usernames, confidential network locations, or credentials. Run the generator only in a trusted local environment.

## Disclosure Response

Confirmed issues may result in documentation updates, code changes, file removal, credential rotation, or a new release entry in `CHANGELOG.md`.
