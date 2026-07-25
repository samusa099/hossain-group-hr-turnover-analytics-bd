#!/usr/bin/env python3
"""Execute notebook code cells without Jupyter server dependencies.

The smoke test runs every code cell in order from the notebook directory so the
repository-relative data fallback behaves exactly as intended. Matplotlib must
use a non-interactive backend in CI.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "Hossain_Group_Turnover_Analysis.ipynb"


def main() -> int:
    os.environ.setdefault("MPLBACKEND", "Agg")

    if not NOTEBOOK.exists():
        print(f"FAIL: notebook not found: {NOTEBOOK}")
        return 1

    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8-sig"))
    namespace: dict[str, object] = {"__name__": "__notebook_smoke__"}
    previous_cwd = Path.cwd()

    try:
        os.chdir(NOTEBOOK.parent)
        for index, cell in enumerate(notebook.get("cells", []), start=1):
            if cell.get("cell_type") != "code":
                continue

            source = cell.get("source", "")
            if isinstance(source, list):
                source = "".join(source)

            if not source.strip():
                continue

            try:
                code = compile(source, f"{NOTEBOOK.name}:cell-{index}", "exec")
                exec(code, namespace, namespace)
            except Exception as exc:
                print(f"FAIL: notebook code cell {index}: {exc}")
                return 1
    finally:
        os.chdir(previous_cwd)

    print("PASS: analytics notebook executed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
