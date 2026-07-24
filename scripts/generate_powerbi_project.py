#!/usr/bin/env python3
"""Recalculate turnover outputs and rebuild the Power BI PBIP project.

No third-party Python packages are required.

Security note:
The committed semantic model uses the portable ``__PROJECT_ROOT__`` token.
The local launcher sets ``HOSSAIN_GROUP_DATA_ROOT`` so Power BI receives a
machine-specific path only in the local working copy.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import uuid
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "employee_master.csv"
PROCESSED = ROOT / "data" / "processed"
POWERBI = ROOT / "powerbi"
START = date(2025, 1, 1)
END = date(2026, 6, 30)
POWERBI_ROOT_ENV = "HOSSAIN_GROUP_DATA_ROOT"
PORTABLE_ROOT = "__PROJECT_ROOT__"
LINEAGE_NAMESPACE = uuid.UUID("279f5fae-7a3b-4f6d-bf35-6f4df5571b99")


def parse_date(value: str):
    value = (value or "").strip()
    return datetime.strptime(value, "%Y-%m-%d").date() if value else None


def end_of_month(d: date) -> date:
    nxt = date(d.year + (d.month == 12), 1 if d.month == 12 else d.month + 1, 1)
    return nxt - timedelta(days=1)


def month_range(start: date, end: date):
    d = date(start.year, start.month, 1)
    while d <= end:
        yield d
        d = date(d.year + (d.month == 12), 1 if d.month == 12 else d.month + 1, 1)


def active_on(e, d):
    return e["Join_Date"] <= d and (e["Exit_Date"] is None or e["Exit_Date"] >= d)


def active_end(e, d):
    return e["Join_Date"] <= d and (e["Exit_Date"] is None or e["Exit_Date"] > d)


def risk(rate):
    p = rate * 100
    if p < 5:
        return "Low Risk"
    if p < 10:
        return "Moderate Risk"
    if p < 15:
        return "High Risk"
    if p < 20:
        return "Very High Risk"
    return "Critical Risk"


def read_employees():
    if not RAW.exists():
        raise FileNotFoundError(f"Missing source file: {RAW}")
    rows = []
    with RAW.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            r["Join_Date"] = parse_date(r["Join_Date"])
            r["Exit_Date"] = parse_date(r.get("Exit_Date", ""))
            rows.append(r)
    return rows


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows generated for {path.name}")
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def calculate(employees):
    months = list(month_range(START, END))
    company = []
    dept_monthly = []
    depts = sorted({e["Department"] for e in employees})

    for ms in months:
        me = end_of_month(ms)
        opening = sum(active_on(e, ms) for e in employees)
        closing = sum(active_end(e, me) for e in employees)
        hires = sum(ms <= e["Join_Date"] <= me for e in employees)
        exits = sum(bool(e["Exit_Date"] and ms <= e["Exit_Date"] <= me) for e in employees)
        avg = (opening + closing) / 2
        rate = exits / avg if avg else 0
        company.append({
            "MonthStart": ms.isoformat(), "MonthLabel": ms.strftime("%b %Y"), "Year": ms.year,
            "OpeningHeadcount": opening, "Hires": hires, "Exits": exits,
            "ClosingHeadcount": closing, "AverageHeadcount": round(avg, 2),
            "TurnoverRate": round(rate, 6), "AnnualizedTurnoverRate": round(rate * 12, 6),
            "RiskLevel": risk(rate),
        })
        for dept in depts:
            subset = [e for e in employees if e["Department"] == dept]
            o = sum(active_on(e, ms) for e in subset)
            c = sum(active_end(e, me) for e in subset)
            h = sum(ms <= e["Join_Date"] <= me for e in subset)
            x = sum(bool(e["Exit_Date"] and ms <= e["Exit_Date"] <= me) for e in subset)
            a = (o + c) / 2
            r = x / a if a else 0
            dept_monthly.append({
                "MonthStart": ms.isoformat(), "MonthLabel": ms.strftime("%b %Y"), "Year": ms.year,
                "Department": dept, "OpeningHeadcount": o, "Hires": h, "Exits": x,
                "ClosingHeadcount": c, "AverageHeadcount": round(a, 2),
                "TurnoverRate": round(r, 6), "AnnualizedTurnoverRate": round(r * 12, 6),
                "RiskLevel": risk(r),
            })

    dept_summary = []
    for dept in depts:
        rows = [r for r in dept_monthly if r["Department"] == dept]
        avg = sum(r["AverageHeadcount"] for r in rows) / len(rows)
        exits = sum(r["Exits"] for r in rows)
        period_rate = exits / avg if avg else 0
        annual = period_rate * 12 / len(months)
        dept_summary.append({
            "Department": dept, "AverageHeadcount": round(avg, 2), "Exits": exits,
            "TurnoverRate": round(period_rate, 6), "AnnualizedTurnoverRate": round(annual, 6),
            "RiskLevel": risk(annual),
        })
    dept_summary.sort(key=lambda r: r["TurnoverRate"], reverse=True)

    reasons = Counter(
        e.get("Exit_Reason", "") for e in employees
        if e["Exit_Date"] and START <= e["Exit_Date"] <= END
    )
    total_exits = sum(reasons.values())
    reason_summary = [
        {"ExitReason": reason, "Exits": count, "SharePct": round(count / total_exits, 6)}
        for reason, count in reasons.most_common() if reason
    ]

    opening = sum(active_on(e, START) for e in employees)
    closing = sum(active_end(e, END) for e in employees)
    avg = sum(r["AverageHeadcount"] for r in company) / len(company)
    hires = sum(START <= e["Join_Date"] <= END for e in employees)
    period_rate = total_exits / avg if avg else 0
    annual = period_rate * 12 / len(months)
    kpi = [{
        "PeriodStart": START.isoformat(), "PeriodEnd": END.isoformat(),
        "OpeningHeadcount": opening, "ClosingHeadcount": closing,
        "AverageHeadcount": round(avg, 2), "TotalHires": hires, "TotalExits": total_exits,
        "TurnoverRate": round(period_rate, 6), "AnnualizedTurnoverRate": round(annual, 6),
        "ActiveEmployees": closing, "RiskLevel": risk(annual),
    }]
    return company, dept_monthly, dept_summary, reason_summary, kpi


def json_write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def lineage(*parts: str):
    return str(uuid.uuid5(LINEAGE_NAMESPACE, "::".join(parts)))


def powerbi_source_path(csv_path: Path) -> str:
    relative = csv_path.relative_to(ROOT).as_posix()
    configured_root = os.environ.get(POWERBI_ROOT_ENV, "").strip()
    if configured_root:
        source = str((Path(configured_root).expanduser().resolve() / Path(relative)).resolve())
    else:
        source = f"{PORTABLE_ROOT}/{relative}"
    return source.replace("\\", "\\\\")


def make_m(csv_path, columns):
    p = powerbi_source_path(csv_path)
    transform = ", ".join(f'{{"{n}", {t}}}' for n, t in columns)
    return [
        "let",
        f'    Source = Csv.Document(File.Contents("{p}"),[Delimiter=",", Columns={len(columns)}, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
        '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        f'    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{{transform}}})',
        "in",
        '    #"Changed Type"'
    ]


def table(name, file, cols, measures):
    columns = []
    for cname, dtype, mtype, fmt in cols:
        c = {
            "name": cname,
            "dataType": dtype,
            "sourceColumn": cname,
            "lineageTag": lineage("column", name, cname),
            "summarizeBy": "none",
        }
        if fmt:
            c["formatString"] = fmt
        columns.append(c)
    return {
        "name": name,
        "lineageTag": lineage("table", name),
        "columns": columns,
        "measures": [
            {
                **{
                    "name": m[0],
                    "expression": m[1],
                    "lineageTag": lineage("measure", name, m[0]),
                },
                **({"formatString": m[2]} if m[2] else {}),
            }
            for m in measures
        ],
        "partitions": [{
            "name": name,
            "mode": "import",
            "source": {
                "type": "m",
                "expression": make_m(file, [(c[0], c[2]) for c in cols]),
            },
        }],
    }


def rebuild_model():
    model_dir = POWERBI / "Hossain_Group_Turnover.SemanticModel"
    tables = [
        table("DashboardKPIs", PROCESSED / "dashboard_kpis.csv", [
            ("PeriodStart", "dateTime", "type date", "yyyy-mm-dd"),
            ("PeriodEnd", "dateTime", "type date", "yyyy-mm-dd"),
            ("OpeningHeadcount", "int64", "Int64.Type", "0"),
            ("ClosingHeadcount", "int64", "Int64.Type", "0"),
            ("AverageHeadcount", "double", "type number", "0.00"),
            ("TotalHires", "int64", "Int64.Type", "0"),
            ("TotalExits", "int64", "Int64.Type", "0"),
            ("TurnoverRate", "double", "type number", "0.00%"),
            ("AnnualizedTurnoverRate", "double", "type number", "0.00%"),
            ("ActiveEmployees", "int64", "Int64.Type", "0"),
            ("RiskLevel", "string", "type text", None),
        ], [
            ("Active Employees", "MAX('DashboardKPIs'[ActiveEmployees])", "0"),
            ("Total Exits", "MAX('DashboardKPIs'[TotalExits])", "0"),
            ("Total Hires", "MAX('DashboardKPIs'[TotalHires])", "0"),
            ("Period Turnover Rate", "MAX('DashboardKPIs'[TurnoverRate])", "0.00%"),
            ("Annualized Turnover Rate", "MAX('DashboardKPIs'[AnnualizedTurnoverRate])", "0.00%"),
        ]),
        table("CompanyMonthly", PROCESSED / "company_monthly_turnover.csv", [
            ("MonthStart", "dateTime", "type date", "mmm yyyy"),
            ("MonthLabel", "string", "type text", None),
            ("Year", "int64", "Int64.Type", "0"),
            ("OpeningHeadcount", "int64", "Int64.Type", "0"),
            ("Hires", "int64", "Int64.Type", "0"),
            ("Exits", "int64", "Int64.Type", "0"),
            ("ClosingHeadcount", "int64", "Int64.Type", "0"),
            ("AverageHeadcount", "double", "type number", "0.00"),
            ("TurnoverRate", "double", "type number", "0.00%"),
            ("AnnualizedTurnoverRate", "double", "type number", "0.00%"),
            ("RiskLevel", "string", "type text", None),
        ], [
            ("Monthly Turnover Rate", "MAX('CompanyMonthly'[TurnoverRate])", "0.00%"),
            ("Monthly Exits", "SUM('CompanyMonthly'[Exits])", "0"),
            ("Monthly Hires", "SUM('CompanyMonthly'[Hires])", "0"),
        ]),
        table("DepartmentSummary", PROCESSED / "department_turnover_summary.csv", [
            ("Department", "string", "type text", None),
            ("AverageHeadcount", "double", "type number", "0.00"),
            ("Exits", "int64", "Int64.Type", "0"),
            ("TurnoverRate", "double", "type number", "0.00%"),
            ("AnnualizedTurnoverRate", "double", "type number", "0.00%"),
            ("RiskLevel", "string", "type text", None),
        ], [
            ("Department Turnover Rate", "MAX('DepartmentSummary'[TurnoverRate])", "0.00%"),
            ("Department Exits", "SUM('DepartmentSummary'[Exits])", "0"),
        ]),
        table("ExitReasonSummary", PROCESSED / "exit_reason_summary.csv", [
            ("ExitReason", "string", "type text", None),
            ("Exits", "int64", "Int64.Type", "0"),
            ("SharePct", "double", "type number", "0.00%"),
        ], [
            ("Exit Count", "SUM('ExitReasonSummary'[Exits])", "0"),
        ]),
    ]
    json_write(model_dir / "model.bim", {
        "name": "Hossain Group Turnover Semantic Model",
        "compatibilityLevel": 1600,
        "model": {
            "culture": "en-US",
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "en-US",
            "tables": tables,
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True,
            },
            "annotations": [{
                "name": "PBI_QueryOrder",
                "value": '["DashboardKPIs","CompanyMonthly","DepartmentSummary","ExitReasonSummary"]',
            }],
        },
    })


def main():
    employees = read_employees()
    company, dept_monthly, dept_summary, reasons, kpi = calculate(employees)
    write_csv(PROCESSED / "company_monthly_turnover.csv", company)
    write_csv(PROCESSED / "department_monthly_turnover.csv", dept_monthly)
    write_csv(PROCESSED / "department_turnover_summary.csv", dept_summary)
    write_csv(PROCESSED / "exit_reason_summary.csv", reasons)
    write_csv(PROCESSED / "dashboard_kpis.csv", kpi)
    write_csv(ROOT / "looker_studio" / "hossain_group_looker_studio.csv", dept_monthly)
    rebuild_model()
    print("Success: processed data and Power BI semantic model regenerated.")
    if os.environ.get(POWERBI_ROOT_ENV):
        print("Power BI source paths were prepared for this local repository.")
    else:
        print(f"Power BI source paths use the safe {PORTABLE_ROOT} placeholder.")
        print("For local Power BI refresh, use run_project.bat or run_project.ps1.")
    print("Open:", POWERBI / "Hossain_Group_Turnover.pbip")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
