#!/usr/bin/env python3
"""Validate repository structure, analytics files and public-data safety controls."""
from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CASE_FILES = [
    "case-study/README.md",
    "case-study/CASE_NARRATIVE.md",
    "case-study/MANAGEMENT_CONTEXT.md",
    "case-study/EXECUTIVE_MANDATE.md",
    "case-study/ROLE_TRACKS.md",
    "case-study/SUBMISSION_REQUIREMENTS.md",
    "case-study/POLICY_AND_LEGAL_RESEARCH.md",
    "case-study/RUBRIC.md",
    "case-study/variants/managing-director.md",
    "case-study/variants/hr-business-partner.md",
    "case-study/variants/people-analytics.md",
    "case-study/variants/operations-finance.md",
    "case-study/variants/policy-governance.md",
]

REQUIRED = [
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/pull_request_template.md",
    ".github/PULL_REQUEST_TEMPLATE/case-submission.md",
    ".github/scripts/case_submission_policy.py",
    ".github/workflows/codeql.yml",
    ".github/workflows/dependency-review.yml",
    ".github/workflows/security-and-validation.yml",
    ".github/workflows/portfolio-security.yml",
    ".github/workflows/validate-case-submission.yml",
    ".github/workflows/sync-kaggle.yml",
    ".github/workflows/publish-release.yml",
    ".gitignore",
    "README.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "RELEASE_NOTES_v1.3.0.md",
    "VERSION",
    "CITATION.cff",
    "release/RELEASE_VERSION",
    "release/V1.3.0_RELEASE_MANIFEST.md",
    "docs/CASE_SUBMISSION_PROTECTION.md",
    "docs/CASE_STUDY_PUBLISHING_GUIDE.md",
    "docs/Protect_Case_Submission_Ruleset.json",
    "submissions/README.md",
    "submissions/SUBMISSION_TEMPLATE.md",
    "scripts/prepare_kaggle_dataset.py",
    "kaggle/dataset/README.md",
    "data/raw/employee_master.csv",
    "data/metadata/data_dictionary.json",
    "data/processed/company_monthly_turnover.csv",
    "data/processed/department_monthly_turnover.csv",
    "data/processed/department_turnover_summary.csv",
    "data/processed/exit_reason_summary.csv",
    "data/processed/dashboard_kpis.csv",
    "excel/Hossain_Group_Employee_Turnover_Calculator.xlsx",
    "notebooks/Hossain_Group_Turnover_Analysis.ipynb",
    "powerbi/Hossain_Group_Turnover.pbip",
    "powerbi/Hossain_Group_Turnover.Report/definition.pbir",
    "powerbi/Hossain_Group_Turnover.Report/definition/version.json",
    "powerbi/Hossain_Group_Turnover.Report/definition/report.json",
    "powerbi/Hossain_Group_Turnover.SemanticModel/definition.pbism",
    "powerbi/Hossain_Group_Turnover.SemanticModel/model.bim",
    *CASE_FILES,
]

EXPECTED_HEADERS = {
    "data/raw/employee_master.csv": [
        "Employee_ID", "Employee_Name", "Gender", "Department", "Designation",
        "Location", "Employment_Type", "Join_Date", "Exit_Date", "Exit_Reason", "Status",
    ],
    "data/processed/company_monthly_turnover.csv": [
        "MonthStart", "MonthLabel", "Year", "OpeningHeadcount", "Hires", "Exits",
        "ClosingHeadcount", "AverageHeadcount", "TurnoverRate",
        "AnnualizedTurnoverRate", "RiskLevel",
    ],
    "data/processed/department_monthly_turnover.csv": [
        "MonthStart", "MonthLabel", "Year", "Department", "OpeningHeadcount", "Hires",
        "Exits", "ClosingHeadcount", "AverageHeadcount", "TurnoverRate",
        "AnnualizedTurnoverRate", "RiskLevel",
    ],
    "data/processed/department_turnover_summary.csv": [
        "Department", "AverageHeadcount", "Exits", "TurnoverRate",
        "AnnualizedTurnoverRate", "RiskLevel",
    ],
    "data/processed/exit_reason_summary.csv": ["ExitReason", "Exits", "SharePct"],
    "data/processed/dashboard_kpis.csv": [
        "PeriodStart", "PeriodEnd", "OpeningHeadcount", "ClosingHeadcount",
        "AverageHeadcount", "TotalHires", "TotalExits", "TurnoverRate",
        "AnnualizedTurnoverRate", "ActiveEmployees", "RiskLevel",
    ],
    "looker_studio/hossain_group_looker_studio.csv": [
        "MonthStart", "MonthLabel", "Year", "Department", "OpeningHeadcount", "Hires",
        "Exits", "ClosingHeadcount", "AverageHeadcount", "TurnoverRate",
        "AnnualizedTurnoverRate", "RiskLevel",
    ],
}

PROHIBITED_HR_HEADERS = {
    "nid", "national_id", "nationalid", "passport", "tax_id", "tin",
    "bank_account", "bankaccount", "routing_number", "medical", "disability",
    "biometric", "fingerprint", "personal_email", "private_email", "phone_number",
    "mobile_number", "home_address",
}

SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub classic token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}

TEXT_SUFFIXES = {
    ".py", ".ps1", ".bat", ".json", ".yml", ".yaml", ".toml", ".ini",
    ".cfg", ".txt", ".csv", ".bim", ".pbir", ".pbism", ".md", ".cff",
}

FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")
FORMULA_CHECK_COLUMNS = {
    "Employee_ID", "Employee_Name", "Gender", "Department", "Designation",
    "Location", "Employment_Type", "Exit_Reason", "Status",
}


def fail(message: str) -> bool:
    print(f"FAIL: {message}")
    return False


def parse_iso_date(value: str, field: str, employee_id: str):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{employee_id}: invalid {field} '{value}'") from exc


def iter_text_files():
    ignored_parts = {
        ".git", ".venv", "venv", "__pycache__", ".ipynb_checkpoints", ".kaggle-build"
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ignored_parts.intersection(path.parts):
            continue
        yield path


def validate_required() -> bool:
    ok = True
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            ok = fail(f"Missing required file: {rel}") and ok
    return ok


def validate_json() -> bool:
    ok = True
    for path in ROOT.rglob("*.json"):
        if ".kaggle-build" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            ok = fail(f"Invalid JSON {path.relative_to(ROOT)}: {exc}") and ok
    return ok


def validate_csv_files() -> bool:
    ok = True
    for rel, expected in EXPECTED_HEADERS.items():
        path = ROOT / rel
        if not path.exists():
            ok = fail(f"Missing CSV: {rel}") and ok
            continue
        try:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.reader(handle))
            if len(rows) < 2:
                ok = fail(f"CSV has no data rows: {rel}") and ok
                continue
            if rows[0] != expected:
                ok = fail(f"Unexpected CSV headers in {rel}: {rows[0]}") and ok
        except Exception as exc:
            ok = fail(f"Invalid CSV {rel}: {exc}") and ok
    return ok


def validate_employee_data() -> bool:
    path = ROOT / "data/raw/employee_master.csv"
    if not path.exists():
        return False

    ok = True
    seen_ids: set[str] = set()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        prohibited = sorted(
            PROHIBITED_HR_HEADERS.intersection({header.lower() for header in headers})
        )
        if prohibited:
            ok = fail(f"Prohibited public HR fields detected: {', '.join(prohibited)}") and ok

        for row_number, row in enumerate(reader, start=2):
            employee_id = (row.get("Employee_ID") or "").strip() or f"row {row_number}"
            if employee_id in seen_ids:
                ok = fail(f"Duplicate Employee_ID: {employee_id}") and ok
            seen_ids.add(employee_id)

            try:
                join_date = parse_iso_date(
                    (row.get("Join_Date") or "").strip(), "Join_Date", employee_id
                )
                exit_date = parse_iso_date(
                    (row.get("Exit_Date") or "").strip(), "Exit_Date", employee_id
                )
            except ValueError as exc:
                ok = fail(str(exc)) and ok
                continue

            if not join_date:
                ok = fail(f"{employee_id}: Join_Date is required") and ok
            if join_date and exit_date and exit_date < join_date:
                ok = fail(f"{employee_id}: Exit_Date is before Join_Date") and ok

            status = (row.get("Status") or "").strip().lower()
            if status == "active" and exit_date:
                ok = fail(f"{employee_id}: Active employee has an Exit_Date") and ok
            if status == "exited" and not exit_date:
                ok = fail(f"{employee_id}: Exited employee has no Exit_Date") and ok

            for column in FORMULA_CHECK_COLUMNS:
                value = (row.get(column) or "").strip()
                if value.startswith(FORMULA_PREFIXES):
                    ok = fail(
                        f"Potential spreadsheet formula injection in {employee_id} column {column}"
                    ) and ok
    return ok


def validate_notebook() -> bool:
    path = ROOT / "notebooks/Hossain_Group_Turnover_Analysis.ipynb"
    if not path.exists():
        return False
    try:
        notebook = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return fail(f"Invalid notebook JSON: {exc}")

    ok = True
    for index, cell in enumerate(notebook.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs"):
            ok = fail(f"Notebook code cell {index} contains committed output") and ok
        if cell.get("execution_count") is not None:
            ok = fail(f"Notebook code cell {index} contains an execution count") and ok
    return ok


def validate_case_materials() -> bool:
    ok = True
    for rel in CASE_FILES:
        path = ROOT / rel
        if not path.is_file():
            ok = fail(f"Missing official case file: {rel}") and ok
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            ok = fail(f"Official case file is empty: {rel}") and ok

    case_root = ROOT / "case-study"
    unexpected = [
        path.relative_to(case_root)
        for path in case_root.rglob("*")
        if path.is_file() and path.suffix.lower() != ".md"
    ]
    if unexpected:
        ok = fail(
            "Unexpected non-Markdown file in official case materials: "
            + ", ".join(str(path) for path in unexpected)
        ) and ok
    return ok


def validate_powerbi_paths() -> bool:
    path = ROOT / "powerbi/Hossain_Group_Turnover.SemanticModel/model.bim"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8-sig")
    ok = True
    if "__PROJECT_ROOT__/data/processed/" not in text:
        ok = fail("Power BI model does not use the portable __PROJECT_ROOT__ token") and ok

    unsafe_patterns = {
        "Linux or macOS user home": re.compile(r"(?:/home/|/Users/)[^/\s\"']+"),
        "temporary container path": re.compile(r"/mnt/data/"),
        "Windows user profile": re.compile(r"[A-Za-z]:\\\\Users\\\\|[A-Za-z]:/Users/"),
        "UNC network path": re.compile(r"\\\\\\\\[^\\\s]+\\\\[^\\\s]+"),
    }
    for label, pattern in unsafe_patterns.items():
        if pattern.search(text):
            ok = fail(f"Unsafe Power BI source path detected: {label}") and ok
    return ok


def validate_secrets() -> bool:
    ok = True
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                ok = fail(f"Potential {label} in {path.relative_to(ROOT)}") and ok
    return ok


def validate_release_metadata() -> bool:
    version_path = ROOT / "VERSION"
    cff_path = ROOT / "CITATION.cff"
    release_version_path = ROOT / "release/RELEASE_VERSION"

    if not all(path.is_file() for path in (version_path, cff_path, release_version_path)):
        return fail("Release metadata files are incomplete")

    version = version_path.read_text(encoding="utf-8").strip()
    declared_tag = release_version_path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        return fail(f"VERSION must use X.Y.Z format, found '{version}'")
    if declared_tag != f"v{version}":
        return fail(
            f"release/RELEASE_VERSION must equal v{version}, found '{declared_tag}'"
        )

    cff_text = cff_path.read_text(encoding="utf-8")
    if not re.search(rf"^version:\s*{re.escape(version)}\s*$", cff_text, re.MULTILINE):
        return fail(f"CITATION.cff does not declare version {version}")

    notes = ROOT / f"RELEASE_NOTES_v{version}.md"
    manifest = ROOT / "release" / f"V{version}_RELEASE_MANIFEST.md"
    if not notes.is_file() or not notes.read_text(encoding="utf-8").strip():
        return fail(f"Missing or empty release notes: {notes.relative_to(ROOT)}")
    if not manifest.is_file() or not manifest.read_text(encoding="utf-8").strip():
        return fail(f"Missing or empty release manifest: {manifest.relative_to(ROOT)}")
    return True


def main() -> int:
    checks = [
        validate_required,
        validate_json,
        validate_csv_files,
        validate_employee_data,
        validate_notebook,
        validate_case_materials,
        validate_powerbi_paths,
        validate_secrets,
        validate_release_metadata,
    ]
    ok = True
    for check in checks:
        ok = check() and ok

    if ok:
        print(
            "PASS: repository structure, case materials, JSON, CSV schemas, employee dates, "
            "notebook hygiene, Power BI paths, secret patterns and release metadata validated."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
