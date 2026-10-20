"""Optional step 0: extract the non-stop flights from the full Kaggle dump.

Input : data/raw/flight_data.csv      (full dataset, too large for git; download
                                       it from Kaggle, see README)
Output: data/raw/flights_nonstop.csv  (committed, so this step can be skipped)

Keeps only the rows with stops == 0, as described in the project report.
"""

import sys

from common import RAW_DIR, read_csv, write_csv

INPUT_FILE = RAW_DIR / "flight_data.csv"
OUTPUT_FILE = RAW_DIR / "flights_nonstop.csv"


def main():
    if not INPUT_FILE.exists():
        sys.exit(f"{INPUT_FILE} not found: download the flights dataset first (see README).")
    header, rows = read_csv(INPUT_FILE)
    stops = header.index("stops")
    write_csv(OUTPUT_FILE, header, [r for r in rows if r[stops] == "0"])


if __name__ == "__main__":
    main()
