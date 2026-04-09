#!/usr/bin/env python3
"""
compare_results.py  –  write expected.txt / actual.txt for a model's errors

Reads evaluation/results/<model>/errors.csv and writes expected.txt and
actual.txt into that same folder so they can be opened side by side.

Usage:
    python evaluation/compare_results.py                  # auto-detects if one model folder exists
    python evaluation/compare_results.py nuextract_2_0_2b
    python evaluation/compare_results.py nuextract_2_0_7b
"""

import csv
import json
import sys
from pathlib import Path

RESULTS_ROOT = Path(__file__).parent / "results"


def pretty(s: str) -> str:
    try:
        return json.dumps(json.loads(s), indent=2)
    except Exception:
        return s.strip()


def write_comparison(model_dir: Path):
    errors_path = model_dir / "errors.csv"
    if not errors_path.exists():
        print(f"No errors.csv found in {model_dir}")
        sys.exit(1)

    with open(errors_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("errors.csv is empty — nothing to compare.")
        return

    expected_lines, actual_lines = [], []
    for row in rows:
        sep    = f"{'='*60}\nRow {row['index']}\n{'='*60}\n"
        prompt = f"PROMPT:\n{row['text'].strip()}\n\n"
        expected_lines.append(sep + prompt + "EXPECTED:\n" + pretty(row["target"])       + "\n\n")
        actual_lines.append(  sep + prompt + "ACTUAL:\n"   + pretty(row["model_output"]) + "\n\n")

    (model_dir / "expected.txt").write_text("".join(expected_lines), encoding="utf-8")
    (model_dir / "actual.txt").write_text(  "".join(actual_lines),   encoding="utf-8")

    print(f"Wrote {len(rows)} rows to:")
    print(f"  {model_dir / 'expected.txt'}")
    print(f"  {model_dir / 'actual.txt'}")


def main():
    if len(sys.argv) > 1:
        model_dir = RESULTS_ROOT / sys.argv[1]
    else:
        # Auto-detect: find subdirectories that contain an errors.csv
        candidates = [d for d in RESULTS_ROOT.iterdir() if d.is_dir() and (d / "errors.csv").exists()]
        if len(candidates) == 1:
            model_dir = candidates[0]
            print(f"Auto-detected model folder: {model_dir.name}")
        elif len(candidates) == 0:
            print(f"No model subfolders with errors.csv found under {RESULTS_ROOT}")
            print("Run the benchmark notebook first, or pass the folder name explicitly.")
            sys.exit(1)
        else:
            names = [d.name for d in candidates]
            print(f"Multiple model folders found: {names}")
            print("Pass one as an argument, e.g.:")
            for n in names:
                print(f"  python evaluation/compare_results.py {n}")
            sys.exit(1)

    write_comparison(model_dir)


if __name__ == "__main__":
    main()
