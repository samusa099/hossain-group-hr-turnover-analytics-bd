# Power BI Setup

## Prerequisites

- Windows
- Microsoft Power BI Desktop
- Python 3 available as `python` or `py`

## One-Click Setup

Run `scripts/run_project.bat`.

The process will:

1. Read `data/raw/employee_master.csv`.
2. Recalculate company, department, and exit-reason summaries.
3. Rebuild the Power BI semantic model and report source files.
4. Insert the correct local absolute paths into the Power Query M partitions.
5. Open `powerbi/Hossain_Group_Turnover.pbip`.

## First Open

1. Enable the Power BI Project save option in Power BI Desktop if prompted.
2. Open the `.pbip`.
3. Select **Refresh** to load CSV data.
4. Review the Executive Overview and Monthly Detail pages.
5. Use **File → Save As** to create a `.pbix` file.

## Important Limitation

Microsoft does not support programmatic conversion between `.pbix` and `.pbip`. The script creates and updates the source-control-friendly `.pbip` project. Power BI Desktop must perform the final `.pbix` Save As operation.

## Troubleshooting

- Keep the extracted project in a short local path, for example `C:\HR-Projects\HossainTurnover`.
- Do not move individual files after running the generator; move the entire project folder.
- If data paths change, run the script again.
- If the report opens without data, select Refresh.
- If Power BI Desktop is old, update it before opening the PBIP project.
