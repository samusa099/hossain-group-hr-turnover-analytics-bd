#!/usr/bin/env python3
"""Validate repository structure, analytics files and public-data safety controls."""
from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime
from enum import Enum
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


class FailureCategory(str, Enum):
    """Allow-listed diagnostic categories safe for CI logs."""

    REQUIRED_FILE = "required-file"
    JSON = "json"
    CSV = "csv"
    CSV_SCHEMA = "csv-schema"
    HR_DATA_POLICY = "hr-data-policy"
    EMPLOYEE_ID = "employee-id"
    EMPLOYEE_DATE = "employee-date"
    EMPLOYEE_STATUS = "employee-status"
    CSV_FORMULA = "csv-formula"
    NOTEBOOK = "notebook"
    NOTEBOOK_HYGIENE = "notebook-hygiene"
    CASE_MATERIALS = "case-materials"
    POWERBI = "powerbi"
    POWERBI_PATH = "powerbi-path"
    SECRET_PATTERN = "secret-pattern"
    RELEASE_METADATA = "release-metadata"


def fail(category: FailureCategory) -> bool:
    """Emit only an allow-listed failure category, never caller-controlled details."""
    print(f"FAIL [{category.value}]: project validation failed.")
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
            ok = fail(FailureCategory.REQUIRED_FILE) and ok
    return ok


def validate_json() -> bool:
    ok = True
    for path in ROOT.rglob("*.json"):
        if ".kaggle-build" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            ok = fail(FailureCategory.JSON) and ok
    return ok


def validate_csv_files() -> bool:
    ok = True
    for rel, expected in EXPECTED_HEADERS.items():
        path = ROOT / rel
        if not path.exists():
            ok = fail(FailureCategory.CSV) and ok
            continue
        try:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.reader(handle))
            if len(rows) < 2:
                ok = fail(FailureCategory.CSV) and ok
                continue
            if rows[0] != expected:
                ok = fail(FailureCategory.CSV_SCHEMA) and ok
        except Exception:
            ok = fail(FailureCategory.CSV) and ok
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
            ok = fail(FailureCategory.HR_DATA_POLICY) and ok

        for row_number, row in enumerate(reader, start=2):
            employee_id = (row.get("Employee_ID") or "").strip() or f"row {row_number}"
            if employee_id in seen_ids:
                ok = fail(FailureCategory.EMPLOYEE_ID) and ok
            seen_ids.add(employee_id)

            try:
                join_date = parse_iso_date(
                    (row.get("Join_Date") or "").strip(), "Join_Date", employee_id
                )
                exit_date = parse_iso_date(
                    (row.get("Exit_Date") or "").strip(), "Exit_Date", employee_id
                )
            except ValueError:
                ok = fail(FailureCategory.EMPLOYEE_DATE) and ok
                continue

            if not join_date:
                ok = fail(FailureCategory.EMPLOYEE_DATE) and ok
            if join_date and exit_date and exit_date < join_date:
                ok = fail(FailureCategory.EMPLOYEE_DATE) and ok

            status = (row.get("Status") or "").strip().lower()
            if status == "active" and exit_date:
                ok = fail(FailureCategory.EMPLOYEE_STATUS) and ok
            if status == "exited" and not exit_date:
                ok = fail(FailureCategory.EMPLOYEE_STATUS) and ok

            for column in FORMULA_CHECK_COLUMNS:
                value = (row.get(column) or "").strip()
                if value.startswith(FORMULA_PREFIXES):
                    ok = fail(FailureCategory.CSV_FORMULA) and ok
    return ok


def validate_notebook() -> bool:
    path = ROOT / "notebooks/Hossain_Group_Turnover_Analysis.ipynb"
    if not path.exists():
        return False
    try:
        notebook = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return fail(FailureCategory.NOTEBOOK)

    ok = True
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs"):
            ok = fail(FailureCategory.NOTEBOOK_HYGIENE) and ok
        if cell.get("execution_count") is not None:
            ok = fail(FailureCategory.NOTEBOOK_HYGIENE) and ok
    return ok


def validate_case_materials() -> bool:
    ok = True
    for rel in CASE_FILES:
        path = ROOT / rel
        if not path.is_file():
            ok = fail(FailureCategory.CASE_MATERIALS) and ok
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            ok = fail(FailureCategory.CASE_MATERIALS) and ok

    case_root = ROOT / "case-study"
    unexpected = [
        path.relative_to(case_root)
        for path in case_root.rglob("*")
        if path.is_file() and path.suffix.lower() != ".md"
    ]
    if unexpected:
        ok = fail(FailureCategory.CASE_MATERIALS) and ok
    return ok


def validate_powerbi_paths() -> bool:
    path = ROOT / "powerbi/Hossain_Group_Turnover.SemanticModel/model.bim"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8-sig")
    ok = True
    if "__PROJECT_ROOT__/data/processed/" not in text:
        ok = fail(FailureCategory.POWERBI) and ok

    unsafe_patterns = {
        "Linux or macOS user home": re.compile(r"(?:/home/|/Users/)[^/\s\"']+"),
        "temporary container path": re.compile(r"/mnt/data/"),
        "Windows user profile": re.compile(r"[A-Za-z]:\\\\Users\\\\|[A-Za-z]:/Users/"),
        "UNC network path": re.compile(r"\\\\\\\\[^\\\s]+\\\\[^\\\s]+"),
    }
    for pattern in unsafe_patterns.values():
        if pattern.search(text):
            ok = fail(FailureCategory.POWERBI_PATH) and ok
    return ok


def validate_secrets() -> bool:
    ok = True
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS.values():
            if pattern.search(text):
                ok = fail(FailureCategory.SECRET_PATTERN) and ok
    return ok


def validate_release_metadata() -> bool:
    version_path = ROOT / "VERSION"
    cff_path = ROOT / "CITATION.cff"
    release_version_path = ROOT / "release/RELEASE_VERSION"

    if not all(path.is_file() for path in (version_path, cff_path, release_version_path)):
        return fail(FailureCategory.RELEASE_METADATA)

    version = version_path.read_text(encoding="utf-8").strip()
    declared_tag = release_version_path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        return fail(FailureCategory.RELEASE_METADATA)
    if declared_tag != f"v{version}":
        return fail(FailureCategory.RELEASE_METADATA)

    cff_text = cff_path.read_text(encoding="utf-8")
    if not re.search(rf"^version:\s*{re.escape(version)}\s*$", cff_text, re.MULTILINE):
        return fail(FailureCategory.RELEASE_METADATA)

    notes = ROOT / f"RELEASE_NOTES_v{version}.md"
    manifest = ROOT / "release" / f"V{version}_RELEASE_MANIFEST.md"
    if not notes.is_file() or not notes.read_text(encoding="utf-8").strip():
        return fail(FailureCategory.RELEASE_METADATA)
    if not manifest.is_file() or not manifest.read_text(encoding="utf-8").strip():
        return fail(FailureCategory.RELEASE_METADATA)
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
