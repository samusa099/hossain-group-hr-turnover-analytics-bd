# Dataset Provenance and Citation

## Sources

This dataset is fully synthetic and was created specifically for an HR analytics portfolio project. It does not originate from any real company, employee database, government record or confidential HR system.

The structure follows common HRIS and workforce analytics fields, including employee ID, department, designation, location, employment type, joining date, exit date, exit reason and employment status. Bangladesh-based names, locations and organisational context are used only to make the dataset realistic for learning and demonstration.

## Collection methodology

Employee records were programmatically generated using Python for the period from **1 January 2025 to 30 June 2026**.

The synthetic records were created using predefined business rules for departments, job roles, locations, employment types, joining dates, exit dates, employee status and exit reasons. No real employee information or personally identifiable data was collected.

After generation, the data was validated for required columns, date consistency, duplicate employee IDs, missing values, unsafe spreadsheet content and structural accuracy. The dataset was then transformed into processed HR analytics tables for headcount, hires, exits, turnover rates, departmental comparison, monthly trends and risk classification.

The final outputs were prepared for Excel, Power BI, Python, Kaggle and Looker Studio use.

## Coverage

- **Start date:** 1 January 2025
- **End date:** 30 June 2026
- **Geospatial coverage:** Bangladesh
- **Records:** 762 synthetic employee records

## Recommended citation

> Musa. (2026). *Hossain Group HR Turnover Analytics BD* (Version 1.2.0) [Synthetic dataset and analytics project]. GitHub. https://github.com/samusa099/hossain-group-hr-turnover-analytics-bd

## BibTeX

```bibtex
@dataset{musa2026hossain,
  author    = {Musa},
  title     = {Hossain Group HR Turnover Analytics BD},
  year      = {2026},
  version   = {1.2.0},
  publisher = {GitHub},
  url       = {https://github.com/samusa099/hossain-group-hr-turnover-analytics-bd},
  note      = {Synthetic Bangladesh-focused HR turnover dataset and analytics project}
}
```

## Licensing

- **Project code:** MIT License
- **Synthetic dataset:** CC0-1.0

## Citation file

Machine-readable citation metadata is available in the repository root as [`CITATION.cff`](../CITATION.cff).
