"""Clean the airlines dataset.

Input : data/raw/airlines.csv
        (Airline ID, Name, Alias, IATA, ICAO, Callsign, Country, Active)
Output: data/processed/airlines.csv
        (Name, IATA, ICAO, Country)

Steps:
  * keep only active airlines (Active == 'Y');
  * replace undefined IATA/ICAO/Country values (`-`, `\\N`, `N/A`) with NULL;
  * lower-case the airline name, so it can be joined with the flights and
    fleet datasets;
  * drop Airline ID, Alias, Callsign and Active.
"""

from common import PROCESSED_DIR, RAW_DIR, drop_columns, null_if_missing, read_csv, write_csv

INPUT_FILE = RAW_DIR / "airlines.csv"
OUTPUT_FILE = PROCESSED_DIR / "airlines.csv"

AIRLINE_ID, NAME, ALIAS, IATA, ICAO, CALLSIGN, COUNTRY, ACTIVE = range(8)
COLUMNS_TO_REMOVE = {AIRLINE_ID, ALIAS, CALLSIGN, ACTIVE}


def clean_row(row):
    for col in (IATA, ICAO, COUNTRY):
        row[col] = null_if_missing(row[col])
    row[NAME] = row[NAME].lower()
    return drop_columns(row, COLUMNS_TO_REMOVE)


def main():
    header, rows = read_csv(INPUT_FILE)
    cleaned = [clean_row(r) for r in rows if r[ACTIVE] == "Y"]
    write_csv(OUTPUT_FILE, drop_columns(header, COLUMNS_TO_REMOVE), cleaned)


if __name__ == "__main__":
    main()
