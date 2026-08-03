#!/usr/bin/env python3
"""Validate repository data safety and GitHub Actions dependency invariants."""

from __future__ import annotations

import csv
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(".").resolve()
WORKFLOWS = Path(".github/workflows")
DEPENDABOT = Path(".github/dependabot.yml")
FULL_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
ACTION_REF = re.compile(
    r"^\s*(?:-\s*)?uses:\s*([^\s@]+)@([^\s#]+)",
    re.MULTILINE,
)
CODEQL_REF = re.compile(
    r"^\s*(?:-\s*)?uses:\s*github/codeql-action/([^@\s]+)@([^\s#]+)",
    re.MULTILINE,
)

BLOCKED_NAMES = {
    ".env",
    "credentials.json",
    "id_dsa",
    "id_ed25519",
    "id_rsa",
    "kaggle.json",
    "service-account.json",
}
BLOCKED_BINARY_SUFFIXES = {
    ".apk",
    ".com",
    ".dll",
    ".dmg",
    ".exe",
    ".iso",
    ".jar",
    ".msi",
    ".scr",
}
UNSAFE_NOTEBOOK_TOKENS = (
    "curl | sh",
    "wget | sh",
    "rm -rf /",
    "subprocess.popen",
    "os.system(",
)

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def workflow_paths() -> list[Path]:
    return sorted(WORKFLOWS.glob("*.y*ml"))


def validate_paths_and_files() -> None:
    for path in Path(".").rglob("*"):
        if ".git" in path.parts:
            continue

        if path.is_symlink():
            try:
                path.resolve(strict=True).relative_to(ROOT)
            except Exception:
                fail(f"Unsafe symlink: {path}")
            continue

        if not path.is_file():
            continue

        try:
            path.resolve().relative_to(ROOT)
        except ValueError:
            fail(f"Path escapes repository: {path}")

        if path.name.lower() in BLOCKED_NAMES:
            fail(f"Blocked credential or private file: {path}")
        if path.suffix.lower() in BLOCKED_BINARY_SUFFIXES:
            fail(f"Blocked binary file: {path}")

    for path in Path(".").rglob("*.xlsx"):
        if ".git" in path.parts:
            continue
        try:
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                if "[Content_Types].xml" not in names or "xl/workbook.xml" not in names:
                    fail(f"Invalid XLSX: {path}")
                for member in names:
                    if member.startswith(("/", "\\")) or ".." in Path(member).parts:
                        fail(f"XLSX path traversal: {path}:{member}")
                    if archive.getinfo(member).file_size > 200_000_000:
                        fail(f"Oversized XLSX member: {path}:{member}")
        except Exception as exc:
            fail(f"Unreadable XLSX {path}: {type(exc).__name__}")

    for path in Path(".").rglob("*.ipynb"):
        if ".git" in path.parts:
            continue
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"Invalid notebook {path}: {type(exc).__name__}")
            continue
        for index, cell in enumerate(notebook.get("cells", [])):
            if not isinstance(cell, dict) or cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", [])).lower()
            if any(token in source for token in UNSAFE_NOTEBOOK_TOKENS):
                fail(f"Unsafe notebook command: {path} cell {index}")

    for path in Path(".").rglob("*.csv"):
        if ".git" in path.parts:
            continue
        try:
            with path.open(encoding="utf-8-sig", newline="", errors="replace") as handle:
                for row_number, row in enumerate(csv.reader(handle), 1):
                    for column_number, value in enumerate(row, 1):
                        if value.lstrip().startswith(("=", "+", "@", "\t", "\r")):
                            fail(
                                "CSV formula injection risk: "
                                f"{path}:{row_number}:{column_number}"
                            )
        except OSError as exc:
            fail(f"Unreadable CSV {path}: {type(exc).__name__}")


def validate_actions() -> None:
    repository_codeql_refs: dict[Path, set[str]] = {}

    for workflow in workflow_paths():
        text = workflow.read_text(encoding="utf-8")

        for action, ref in ACTION_REF.findall(text):
            if action.startswith("docker://"):
                continue
            if not FULL_SHA.fullmatch(ref):
                fail(f"Non-immutable action reference in {workflow}: {action}@{ref}")

        codeql_entries = CODEQL_REF.findall(text)
        if not codeql_entries:
            continue

        refs = {ref.lower() for _, ref in codeql_entries}
        repository_codeql_refs[workflow] = refs
        if len(refs) != 1:
            details = ", ".join(f"{component}@{ref}" for component, ref in codeql_entries)
            fail(f"CodeQL component mismatch in {workflow}: {details}")

    all_codeql_refs = {
        ref
        for refs in repository_codeql_refs.values()
        for ref in refs
    }
    if len(all_codeql_refs) > 1:
        details = ", ".join(
            f"{workflow}={','.join(sorted(refs))}"
            for workflow, refs in sorted(
                repository_codeql_refs.items(), key=lambda item: str(item[0])
            )
        )
        fail(f"Repository-wide CodeQL SHA drift: {details}")


def validate_dependabot_grouping() -> None:
    if not DEPENDABOT.exists():
        fail("Missing .github/dependabot.yml")
        return

    text = DEPENDABOT.read_text(encoding="utf-8")
    if not re.search(
        r"package-ecosystem:\s*[\"']?github-actions[\"']?",
        text,
    ):
        fail("Dependabot does not configure the github-actions ecosystem")

    if not re.search(r"^\s*codeql-version-suite:\s*$", text, re.MULTILINE):
        fail("Missing Dependabot codeql-version-suite group")
    if not re.search(r"^\s*codeql-security-suite:\s*$", text, re.MULTILINE):
        fail("Missing Dependabot codeql-security-suite group")
    if not re.search(
        r"^\s*applies-to:\s*[\"']?version-updates[\"']?\s*$",
        text,
        re.MULTILINE,
    ):
        fail("CodeQL version-update grouping is not explicit")
    if not re.search(
        r"^\s*applies-to:\s*[\"']?security-updates[\"']?\s*$",
        text,
        re.MULTILINE,
    ):
        fail("CodeQL security-update grouping is not explicit")
    if text.count("github/codeql-action/*") < 2:
        fail("CodeQL wildcard must be present in both version and security groups")


def main() -> int:
    validate_paths_and_files()
    validate_actions()
    validate_dependabot_grouping()

    if errors:
        for message in errors:
            print(f"::error::{message}")
        print(f"FAILED: {len(errors)} repository policy violation(s).")
        return 1

    print("PASS: repository data and GitHub Actions dependency policy validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
