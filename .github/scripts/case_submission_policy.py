#!/usr/bin/env python3
"""Validate external case-study pull requests without executing contributor code."""

from __future__ import annotations

import base64
import http.client
import json
import os
import re
import sys
import urllib.parse
from collections import Counter
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
REPOSITORY_NAME = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
COMMIT_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
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
SECRET_PATTERNS = (
    re.compile(r"KGAT_[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)
REQUIRED_DECLARATION = (
    "Data declaration: No real employee or confidential company data is included."
)

ERROR_MESSAGES = {
    "branch": "Submission branch naming policy failed.",
    "no-files": "Submission pull request contains no changed files.",
    "scope": "External submissions may modify only the author's submission path.",
    "folder": "Submission files must be inside a submission-id folder.",
    "submission-id": "Submission ID must use lowercase letters, numbers and hyphens.",
    "single-root": "One pull request must contain exactly one submission directory.",
    "missing-readme": "Required README.md is missing.",
    "missing-report": "Required report.pdf is missing.",
    "blocked-name": "Blocked credential or private file name detected.",
    "file-type": "File type is not allowed for participant submissions.",
    "file-size": "File exceeds its policy size limit.",
    "content-read": "File content could not be inspected.",
    "pdf": "report.pdf is not a valid PDF file.",
    "utf8": "Text file must use UTF-8 encoding.",
    "secret": "Potential secret or private key detected.",
    "notebook-json": "Notebook JSON is invalid.",
    "notebook-format": "Notebook must use nbformat version 4.",
    "notebook-cells": "Notebook cells must be a JSON list.",
    "notebook-cell": "Notebook contains an invalid cell.",
    "notebook-attachments": "Notebook contains cell attachments.",
    "notebook-outputs": "Notebook contains execution outputs.",
    "total-size": "Submission exceeds the 25 MB total size limit.",
    "declaration": "Submission README is missing the required data declaration.",
}

violations: list[str] = []


def validate_github_identifier(value: str, label: str) -> str:
    """Accept only canonical owner/repository names supplied by GitHub events."""
    if not REPOSITORY_NAME.fullmatch(value):
        raise RuntimeError(f"Invalid {label} repository identifier")
    return value


def validate_commit_sha(value: str) -> str:
    """Accept only a full hexadecimal commit SHA."""
    if not COMMIT_SHA.fullmatch(value):
        raise RuntimeError("Invalid pull-request head commit SHA")
    return value.lower()


def github_api_json(path: str) -> object:
    """Call only the fixed GitHub API host and reject redirects."""
    if not path.startswith("/") or "\r" in path or "\n" in path:
        raise RuntimeError("Invalid GitHub API path")

    connection = http.client.HTTPSConnection("api.github.com", timeout=30)
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "hossain-group-case-submission-validator",
    }
    try:
        connection.request("GET", path, headers=headers)
        response = connection.getresponse()
        payload = response.read()
    finally:
        connection.close()

    if response.status < 200 or response.status >= 300:
        raise RuntimeError(f"GitHub API request failed with status {response.status}")
    return json.loads(payload.decode("utf-8"))


def fetch_repository_file(repository: str, sha: str, path: str) -> bytes:
    """Read one file through GitHub's fixed API host without following redirects."""
    safe_repository = validate_github_identifier(repository, "head")
    safe_sha = validate_commit_sha(sha)
    pure_path = PurePosixPath(path)
    if pure_path.is_absolute() or ".." in pure_path.parts or not pure_path.parts:
        raise RuntimeError("Invalid repository file path")

    encoded_path = "/".join(
        urllib.parse.quote(part, safe="") for part in pure_path.parts
    )
    query = urllib.parse.urlencode({"ref": safe_sha})
    endpoint = f"/repos/{safe_repository}/contents/{encoded_path}?{query}"
    payload = github_api_json(endpoint)

    if not isinstance(payload, dict) or payload.get("type") != "file":
        raise RuntimeError("Unexpected GitHub file response")
    encoded = payload.get("content")
    if not isinstance(encoded, str) or payload.get("encoding") != "base64":
        raise RuntimeError("Unsupported GitHub file encoding")
    return base64.b64decode(encoded, validate=True)


def add_violation(code: str, path: str | None = None) -> None:
    violations.append(code)
    message = ERROR_MESSAGES[code]
    if path:
        print(f"::error file={path}::{message}")
    else:
        print(f"::error::{message}")


def list_changed_files() -> list[dict[str, object]]:
    repository = validate_github_identifier(REPOSITORY, "base")
    changed_files: list[dict[str, object]] = []
    page = 1
    while True:
        batch = github_api_json(
            f"/repos/{repository}/pulls/{PR_NUMBER}/files"
            f"?per_page=100&page={page}"
        )
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected pull-request file response")
        changed_files.extend(batch)
        if len(batch) < 100:
            return changed_files
        page += 1


def submission_tree(root: str) -> dict[str, dict[str, object]]:
    repository = validate_github_identifier(HEAD_REPOSITORY, "head")
    sha = validate_commit_sha(HEAD_SHA)
    commit = github_api_json(f"/repos/{repository}/git/commits/{sha}")
    if not isinstance(commit, dict):
        raise RuntimeError("Unable to read submission commit")

    tree_sha = str(commit["tree"]["sha"])
    if not COMMIT_SHA.fullmatch(tree_sha):
        raise RuntimeError("Invalid submission tree SHA")
    tree = github_api_json(
        f"/repos/{repository}/git/trees/{tree_sha}?recursive=1"
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


def scan_secrets(raw: bytes, path: str) -> None:
    text = raw.decode("latin-1", errors="ignore")
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        add_violation("secret", path)


def validate_notebook(text: str, path: str) -> None:
    try:
        notebook = json.loads(text)
    except json.JSONDecodeError:
        add_violation("notebook-json", path)
        return

    if notebook.get("nbformat") != 4:
        add_violation("notebook-format", path)

    cells = notebook.get("cells")
    if not isinstance(cells, list):
        add_violation("notebook-cells", path)
        return

    for cell in cells:
        if not isinstance(cell, dict):
            add_violation("notebook-cell", path)
            continue
        if cell.get("attachments"):
            add_violation("notebook-attachments", path)
        if cell.get("cell_type") == "code" and cell.get("outputs"):
            add_violation("notebook-outputs", path)


def finish() -> int:
    if not violations:
        return 0
    summary = Counter(violations)
    print("Submission policy violation summary:")
    for code, count in sorted(summary.items()):
        print(f"- {code}: {count}")
    print(f"FAILED: {len(violations)} policy violation(s).")
    return 1


def main() -> int:
    validate_github_identifier(REPOSITORY, "base")
    validate_github_identifier(HEAD_REPOSITORY, "head")
    validate_commit_sha(HEAD_SHA)

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
        add_violation("branch")

    changed_files = list_changed_files()
    if not changed_files:
        add_violation("no-files")

    expected_prefix = f"submissions/{AUTHOR}/"
    roots: set[str] = set()

    for item in changed_files:
        paths_to_check = [str(item["filename"])]
        previous = item.get("previous_filename")
        if previous:
            paths_to_check.append(str(previous))

        for candidate in paths_to_check:
            if not candidate.lower().startswith(expected_prefix):
                add_violation("scope", candidate)
                continue

            parts = PurePosixPath(candidate).parts
            if len(parts) < 4:
                add_violation("folder", candidate)
                continue

            submission_id = parts[2]
            if not SUBMISSION_ID.fullmatch(submission_id):
                add_violation("submission-id", candidate)
            roots.add("/".join(parts[:3]))

    if len(roots) != 1:
        add_violation("single-root")

    if violations:
        return finish()

    submission_root = next(iter(roots))
    files = submission_tree(submission_root)

    readme_path = f"{submission_root}/README.md"
    report_path = f"{submission_root}/report.pdf"
    if readme_path not in files:
        add_violation("missing-readme", readme_path)
    if report_path not in files:
        add_violation("missing-report", report_path)

    total_size = 0
    readme_text = ""

    for path, item in sorted(files.items()):
        suffix = PurePosixPath(path).suffix.lower()
        name = PurePosixPath(path).name.lower()
        size = int(item.get("size") or 0)
        total_size += size

        if name in BLOCKED_NAMES:
            add_violation("blocked-name", path)

        if suffix not in ALLOWED_SUFFIXES:
            add_violation("file-type", path)
            continue

        if size > SIZE_LIMITS[suffix]:
            add_violation("file-size", path)
            continue

        if suffix not in {".md", ".ipynb", ".pdf"}:
            continue

        try:
            raw = fetch_repository_file(HEAD_REPOSITORY, HEAD_SHA, path)
        except (RuntimeError, ValueError, json.JSONDecodeError):
            add_violation("content-read", path)
            continue

        scan_secrets(raw, path)

        if suffix == ".pdf":
            if not raw.startswith(b"%PDF-"):
                add_violation("pdf", path)
            continue

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            add_violation("utf8", path)
            continue

        if path == readme_path:
            readme_text = text
        if suffix == ".ipynb":
            validate_notebook(text, path)

    if total_size > TOTAL_LIMIT:
        add_violation("total-size")

    if REQUIRED_DECLARATION not in readme_text:
        add_violation("declaration", readme_path)

    if violations:
        return finish()

    print("PASS: participant submission scope and file policy validated.")
    print(f"Submission root: {submission_root}")
    print(f"Files inspected: {len(files)}")
    print(f"Total size: {total_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
