# Hossain Group Employee Turnover Analytics

A portfolio-ready HR analytics project for **Hossain Group**, designed for an **HR Business Executive** to calculate, monitor, and communicate employee turnover using Excel, Power BI, Python, Kaggle, GitHub, and Looker Studio.

## Project Snapshot

- Company: Hossain Group
- Analysis period: 01 Jan 2025 to 30 Jun 2026
- Records: 762 synthetic employee records
- Opening headcount: 520
- Closing headcount: 592
- Total exits: 170
- Period turnover: 31.11%
- Annualized turnover: 20.74%
- Current risk: Critical Risk

> The dataset is synthetic and created for learning, portfolio, Kaggle, and dashboard practice. It does not contain real employee information.

## Folder Structure

```text
data/raw/                 Employee-level source data
data/processed/           Power BI and Looker Studio-ready summaries
data/metadata/            Data dictionary
excel/                    Formula-driven Excel calculator and dashboard
notebooks/                Kaggle-ready analysis notebook
scripts/                  One-click Power BI project generator and validator
powerbi/                  PBIP report + semantic model source files
looker_studio/            Flat file and setup guide
docs/                     Project description and metric definitions
```

## Quick Start

### Excel

Open `excel/Hossain_Group_Employee_Turnover_Calculator.xlsx`.

1. Replace or extend the rows in `Employee_Data`.
2. Select dates and filters in `Turnover_Calculator`.
3. Review `Dashboard`, `Monthly_Summary`, `Department_Summary`, and `Exit_Reason_Summary`.

### Power BI — one-click Windows workflow

Run:

```bat
scripts\run_project.bat
```

The script recalculates the processed CSV files, rebuilds the Power BI Project source, and opens:

```text
powerbi/Hossain_Group_Turnover.pbip
```

In Power BI Desktop, select **Refresh**. To create a binary `.pbix`, use **File → Save As → Power BI Desktop file (.pbix)**.

### Kaggle

Upload the files from the Kaggle ZIP package or use `notebooks/Hossain_Group_Turnover_Analysis.ipynb`.

### Looker Studio

Upload `looker_studio/hossain_group_looker_studio.csv` as a file data source.

## Turnover Formula

```text
Turnover Rate = Employees Exited / Average Headcount
Average Headcount = (Opening Headcount + Closing Headcount) / 2
Annualized Turnover = Period Turnover × 12 / Number of Months
```

## Risk Bands

| Annualized Turnover | Risk |
|---:|---|
| Below 5% | Low |
| 5% to below 10% | Moderate |
| 10% to below 15% | High |
| 15% to below 20% | Very High |
| 20% or more | Critical |

## Power BI Format Note

This repository uses Microsoft’s source-control-friendly **Power BI Project (`.pbip`)** format. Microsoft documents that PBIP contains separate report and semantic-model folders and can be opened directly in Power BI Desktop. Programmatic PBIX-to-PBIP or PBIP-to-PBIX conversion is not supported; use Power BI Desktop’s **Save As** command for the final `.pbix`.

Official references:

- https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
- https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
- https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset

## License

MIT for project code. Synthetic data is released under CC0-1.0 for portfolio and learning use.
