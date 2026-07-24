#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "data/raw/employee_master.csv",
    "data/processed/company_monthly_turnover.csv",
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
]

def fail(msg):
    print("FAIL:", msg)
    return False

ok = True
for rel in REQUIRED:
    if not (ROOT / rel).exists():
        ok = fail(f"Missing {rel}") and ok

for path in ROOT.rglob("*.json"):
    try:
        json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        ok = fail(f"Invalid JSON {path.relative_to(ROOT)}: {exc}") and ok

for path in ROOT.rglob("*.csv"):
    try:
        with path.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        if len(rows) < 2:
            ok = fail(f"CSV has no data rows: {path.relative_to(ROOT)}") and ok
    except Exception as exc:
        ok = fail(f"Invalid CSV {path.relative_to(ROOT)}: {exc}") and ok

if ok:
    print("PASS: required files, JSON syntax, and CSV structure validated.")
    sys.exit(0)
sys.exit(1)
