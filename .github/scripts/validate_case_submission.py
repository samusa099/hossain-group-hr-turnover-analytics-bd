#!/usr/bin/env python3
"""Validate external case-study pull requests without executing contributor code."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import PurePosixPath

TOKEN = os.environ["GH_TOKEN"]
REPOSITORY = os.environ["REPOSITORY"]
PR_NUMBER = int(os.environ["PR_NUMBER"])
AUTHOR = os.environ["PR_AUTHOR"].lower()
ASSOCIATION = os.environ["AUTHOR_ASSOCIATION"].upper()
HEAD_REPOSITORY = os.environ["HEAD_REPOSITORY"]
HEAD_SHA = os.environ["HEAD_SHA"]
HEAD_REF = os.environ["HEAD_REF"]

TRUSTED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
SUBMISSION_BRANCH = re.compile(
    rf"^submission/{re.escape(AUTHOR)}/[a-z0-9][a-z0-9-]{{1,63}}$"
)
SUBMISSION_ID = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")
ALLOWED_SUFFIXES = {".md", ".pdf", ".ipynb", ".png", ".jpg", ".jpeg"}
BLOCKED_NAMES = {
    ".env",
    "kaggle.json",
    "access_token",
    "id_rsa",
    "id_ed25519",
}
SIZE_LIMITS = {
    ".pdf": 15 * 1024 * 1024,
    ".ipynb": 5 * 1024 * 1024,
    ".png": 3 * 1024 * 1024,
    ".jpg": 3 * 1024 * 1024,
    ".jpeg": 3 * 1024 * 1024,
    ".md": 256 * 1024,
}
TOTAL_LIMIT = 25 * 1024 * 1024
SECRET_PATTERNS = {
    "Kaggle API token": re.compile(r"KGAT_[A-Za-z0-9_-]{20,}"),
    "GitHub personal access token": re.compile(
        r"(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"
    ),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}
REQUIRED_DECLARATION = (
    "Data declaration: No real employee or confidential company data is included."
)

errors: list[str] = []


def api_json(path: str) -> object:
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "hossain-group-case-submission-validator",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_raw(repository: str, sha: str, path: str) -> bytes:
    encoded_path = "/".join(
        urllib.parse.quote(part, safe="") for part in path.split("/")
    )
    request = urllib.request.Request(
        f"https://raw.githubusercontent.com/{repository}/{sha}/{encoded_path}",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "User-Agent": "hossain-group-case-submission-validator",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def add_error(message: str, path: str | None = None) -> None:
    errors.append(message)
    if path:
        print(f"::error file={path}::{message}")
    else:
        print(f"::error::{message}")


def human_size(size: int) -> str:
    if size < 1024 * 1024:
        return f"{size // 1024} KB"
    return f"{size // (1024 * 1024)} MB"


def list_changed_files() -> list[dict[str, object]]:
    changed_files: list[dict[str, object]] = []
    page = 1

    while True:
        batch = api_json(
            f"/repos/{REPOSITORY}/pulls/{PR_NUMBER}/files"
            f"?per_page=100&page={page}"
        )
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected pull-request file response")
        changed_files.extend(batch)
        if len(batch) < 100:
            return changed_files
        page += 1


def submission_tree(root: str) -> dict[str, dict[str, object]]:
    commit = api_json(f"/repos/{HEAD_REPOSITORY}/git/commits/{HEAD_SHA}")
    if not isinstance(commit, dict):
        raise RuntimeError("Unable to read submission commit")

    tree_sha = str(commit["tree"]["sha"])
    tree = api_json(
        f"/repos/{HEAD_REPOSITORY}/git/trees/{tree_sha}?recursive=1"
    )
    if not isinstance(tree, dict) or tree.get("truncated"):
        raise RuntimeError("Unable to inspect the complete submission tree")

    files: dict[str, dict[str, object]] = {}
    for item in tree.get("tree", []):
        if item.get("type") != "blob":
            continue
        path = str(item["path"])
        if path.startswith(root + "/"):
            files[path] = item
    return files


def scan_secrets(text: str, path: str) -> None:
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            add_error(f"Potential {label} detected.", path)


def validate_notebook(text: str, path: str) -> None:
    try:
        notebook = json.loads(text)
    except json.JSONDecodeError as exc:
        add_error(f"Notebook JSON is invalid: {exc}", path)
        return

    if notebook.get("nbformat") != 4:
        add_error("Notebook must use nbformat version 4.", path)

    cells = notebook.get("cells")
    if not isinstance(cells, list):
        add_error("Notebook cells must be a JSON list.", path)
        return

    for index, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            add_error(f"Notebook cell {index} is invalid.", path)
            continue
        if cell.get("attachments"):
            add_error(f"Notebook cell {index} contains attachments.", path)
        if cell.get("cell_type") == "code" and cell.get("outputs"):
            add_error(f"Notebook cell {index} contains execution outputs.", path)


def main() -> int:
    is_submission = (
        ASSOCIATION not in TRUSTED_ASSOCIATIONS
        or HEAD_REF.startswith("submission/")
    )

    if not is_submission:
        print(
            "PASS: trusted maintainer pull request; participant scope policy "
            "is not applicable."
        )
        return 0

    if not SUBMISSION_BRANCH.fullmatch(HEAD_REF):
        add_error(
            "Submission branch must use "
            f"submission/{AUTHOR}/<selected-role>."
        )

    changed_files = list_changed_files()
    if not changed_files:
        add_error("Submission pull request contains no changed files.")

    expected_prefix = f"submissions/{AUTHOR}/"
    roots: set[str] = set()

    for item in changed_files:
        paths_to_check = [str(item["filename"])]
        previous = item.get("previous_filename")
        if previous:
            paths_to_check.append(str(previous))

        for candidate in paths_to_check:
            if not candidate.startswith(expected_prefix):
                add_error(
                    "External submissions may modify only "
                    f"{expected_prefix}<submission-id>/.",
                    candidate,
                )
                continue

            parts = PurePosixPath(candidate).parts
            if len(parts) < 4:
                add_error(
                    "Submission files must be inside a submission-id folder.",
                    candidate,
                )
                continue

            submission_id = parts[2]
            if not SUBMISSION_ID.fullmatch(submission_id):
                add_error(
                    "Submission ID must use lowercase letters, numbers and hyphens.",
                    candidate,
                )
            roots.add("/".join(parts[:3]))

    if len(roots) != 1:
        add_error("One pull request must contain exactly one submission directory.")

    if errors:
        print(f"FAILED: {len(errors)} submission-policy violation(s).")
        return 1

    submission_root = next(iter(roots))
    files = submission_tree(submission_root)

    required = {
        f"{submission_root}/README.md",
        f"{submission_root}/report.pdf",
    }
    for required_path in sorted(required):
        if required_path not in files:
            add_error(f"Required file is missing: {required_path}")

    total_size = 0
    text_cache: dict[str, str] = {}

    for path, item in sorted(files.items()):
        suffix = PurePosixPath(path).suffix.lower()
        name = PurePosixPath(path).name.lower()
        size = int(item.get("size") or 0)
        total_size += size

        if name in BLOCKED_NAMES:
            add_error("Blocked credential or private file name.", path)

        if suffix not in ALLOWED_SUFFIXES:
            add_error(f"File type {suffix or '<none>'} is not allowed.", path)
            continue

        limit = SIZE_LIMITS[suffix]
        if size > limit:
            add_error(
                f"File exceeds the {human_size(limit)} policy limit.", path
            )
            continue

        if suffix not in {".md", ".ipynb", ".pdf"}:
            continue

        try:
            raw = fetch_raw(HEAD_REPOSITORY, HEAD_SHA, path)
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            add_error(f"Unable to inspect file content: {exc}", path)
            continue

        binary_text = raw.decode("latin-1", errors="ignore")
        scan_secrets(binary_text, path)

        if suffix == ".pdf":
            if not raw.startswith(b"%PDF-"):
                add_error("report.pdf is not a valid PDF file.", path)
            continue

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            add_error("Text file must use UTF-8 encoding.", path)
            continue

        text_cache[path] = text
        if suffix == ".ipynb":
            validate_notebook(text, path)

    if total_size > TOTAL_LIMIT:
        add_error("Submission exceeds the 25 MB total size limit.")

    readme_path = f"{submission_root}/README.md"
    if REQUIRED_DECLARATION not in text_cache.get(readme_path, ""):
        add_error(
            "Submission README is missing the required data declaration.",
            readme_path,
        )

    if errors:
        print(f"FAILED: {len(errors)} submission-policy violation(s).")
        return 1

    print("PASS: participant submission scope and file policy validated.")
    print(f"Author: {AUTHOR}")
    print(f"Submission root: {submission_root}")
    print(f"Files inspected: {len(files)}")
    print(f"Total size: {total_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
