"""Shared paths and CSV helpers used by every cleaning step."""

import csv
from pathlib import Path

# Paths are resolved from the repository root, so the scripts work no matter
# which directory they are launched from.
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

# Placeholders the source datasets use for "no value".
NULL_MARKERS = {"\\N", "-", "N/A"}


def read_csv(path, encoding="utf-8"):
    """Return (header, rows) of a CSV file."""
    with open(path, "r", newline="", encoding=encoding) as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return header, rows


def write_csv(path, header, rows):
    """Write a UTF-8 CSV file with Unix line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Wrote {len(rows):>6} rows to {path.relative_to(ROOT_DIR)}")


def drop_columns(row, indices):
    """Return `row` without the columns at the given positions."""
    return [value for idx, value in enumerate(row) if idx not in indices]


def null_if_missing(value, markers=NULL_MARKERS):
    """Replace a missing-value placeholder with an empty string (NULL in SQL)."""
    return "" if value in markers else value
