"""Clean the aircraft dataset.

Input : data/raw/aircraft.csv        (index, Name, IATA code, ICAO code)
Output: data/processed/aircraft.csv  (Name, IATA code, ICAO code)

Steps:
  * drop the pandas `index` column;
  * replace missing IATA/ICAO codes (`\\N`) with NULL.
"""

from common import PROCESSED_DIR, RAW_DIR, drop_columns, null_if_missing, read_csv, write_csv

INPUT_FILE = RAW_DIR / "aircraft.csv"
OUTPUT_FILE = PROCESSED_DIR / "aircraft.csv"

INDEX, NAME, IATA, ICAO = range(4)
COLUMNS_TO_REMOVE = {INDEX}


def clean_row(row):
    row[IATA] = null_if_missing(row[IATA], {"\\N"})
    row[ICAO] = null_if_missing(row[ICAO], {"\\N"})
    return drop_columns(row, COLUMNS_TO_REMOVE)


def main():
    header, rows = read_csv(INPUT_FILE)
    write_csv(OUTPUT_FILE, drop_columns(header, COLUMNS_TO_REMOVE), [clean_row(r) for r in rows])


if __name__ == "__main__":
    main()
