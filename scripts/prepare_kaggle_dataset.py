#!/usr/bin/env python3
"""Build and validate the Kaggle dataset upload package.

The GitHub repository remains the source of truth. This script copies only the
approved dataset, metadata, documentation and notebook files into a temporary
Kaggle staging directory. It never copies GitHub administration files, secrets,
Power BI binaries or unrelated development files.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from pathlib import Path

DATASET_SLUG = "hossain-group-hr-turnover-analytics-bd"
DATASET_TITLE = "Hossain Group HR Turnover Analytics BD"
EXPECTED_EMPLOYEE_ROWS = 762

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / ".kaggle-build" / "dataset"


def copy_file(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"Required source file is missing: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_csv_directory(source: Path, destination: Path) -> list[Path]:
    csv_files = sorted(source.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {source}")

    copied: list[Path] = []
    for csv_file in csv_files:
        target = destination / csv_file.name
        copy_file(csv_file, target)
        copied.append(target)
    return copied


def write_metadata(output: Path, username: str) -> Path:
    metadata = {
        "title": DATASET_TITLE,
        "id": f"{username}/{DATASET_SLUG}",
        "licenses": [{"name": "CC0-1.0"}],
    }
    metadata_path = output / "dataset-metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return metadata_path


def validate_employee_csv(path: Path) -> None:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if len(rows) != EXPECTED_EMPLOYEE_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_EMPLOYEE_ROWS} employee rows, found {len(rows)}"
        )

    required_columns = {
        "Employee_ID",
        "Employee_Name",
        "Department",
        "Designation",
        "Location",
        "Employment_Type",
        "Join_Date",
        "Exit_Date",
        "Exit_Reason",
        "Status",
    }
    missing_columns = required_columns.difference(reader.fieldnames or [])
    if missing_columns:
        raise ValueError(
            "Employee CSV is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )


def validate_package(output: Path, username: str) -> None:
    expected_files = [
        output / "dataset-metadata.json",
        output / "README.md",
        output / "DATA_PROVENANCE.md",
        output / "DATASET_USAGE_GUIDE.md",
        output / "CITATION.cff",
        output / "raw" / "employee_master.csv",
        output / "metadata" / "data_dictionary.json",
        output / "project" / "Hossain_Group_Turnover_Analysis.ipynb",
    ]

    missing = [str(path.relative_to(output)) for path in expected_files if not path.is_file()]
    if missing:
        raise FileNotFoundError("Kaggle package is missing: " + ", ".join(missing))

    metadata = json.loads(
        (output / "dataset-metadata.json").read_text(encoding="utf-8")
    )
    expected_id = f"{username}/{DATASET_SLUG}"
    if metadata.get("id") != expected_id:
        raise ValueError(
            f"Dataset metadata id must be {expected_id!r}, found {metadata.get('id')!r}"
        )

    json.loads(
        (output / "metadata" / "data_dictionary.json").read_text(encoding="utf-8-sig")
    )
    json.loads(
        (output / "project" / "Hossain_Group_Turnover_Analysis.ipynb").read_text(
            encoding="utf-8-sig"
        )
    )
    validate_employee_csv(output / "raw" / "employee_master.csv")

    prohibited_names = {
        ".env",
        "kaggle.json",
        "access_token",
        "id_rsa",
        "id_ed25519",
    }
    prohibited_suffixes = {".pbix", ".pem", ".pfx", ".key"}

    for path in output.rglob("*"):
        if not path.is_file():
            continue
        if path.name in prohibited_names or path.suffix.lower() in prohibited_suffixes:
            raise ValueError(f"Prohibited file found in Kaggle package: {path}")

    processed_files = sorted((output / "processed").glob("*.csv"))
    if not processed_files:
        raise ValueError("The processed Kaggle archive contains no CSV files")


def build_package(output: Path, username: str) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    write_metadata(output, username)

    copy_file(REPOSITORY_ROOT / "README.md", output / "README.md")
    copy_file(
        REPOSITORY_ROOT / "DATA_PROVENANCE.md",
        output / "DATA_PROVENANCE.md",
    )
    copy_file(
        REPOSITORY_ROOT / "DATASET_USAGE_GUIDE.md",
        output / "DATASET_USAGE_GUIDE.md",
    )
    copy_file(REPOSITORY_ROOT / "CITATION.cff", output / "CITATION.cff")

    copy_file(
        REPOSITORY_ROOT / "data" / "raw" / "employee_master.csv",
        output / "raw" / "employee_master.csv",
    )
    copy_csv_directory(
        REPOSITORY_ROOT / "data" / "processed",
        output / "processed",
    )
    copy_file(
        REPOSITORY_ROOT / "data" / "metadata" / "data_dictionary.json",
        output / "metadata" / "data_dictionary.json",
    )
    copy_file(
        REPOSITORY_ROOT
        / "notebooks"
        / "Hossain_Group_Turnover_Analysis.ipynb",
        output / "project" / "Hossain_Group_Turnover_Analysis.ipynb",
    )

    validate_package(output, username)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the clean GitHub-to-Kaggle dataset package."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Staging directory to recreate.",
    )
    parser.add_argument(
        "--username",
        default=os.environ.get("KAGGLE_USERNAME", "dry-run-user"),
        help="Kaggle username used in dataset-metadata.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    username = args.username.strip()
    if not username:
        raise ValueError("Kaggle username cannot be empty")

    output = args.output.resolve()
    build_package(output, username)

    files = sorted(
        str(path.relative_to(output))
        for path in output.rglob("*")
        if path.is_file()
    )
    print(f"PASS: Kaggle package prepared at {output}")
    print(f"Dataset id: {username}/{DATASET_SLUG}")
    print(f"Files prepared: {len(files)}")
    for file_name in files:
        print(f"- {file_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
