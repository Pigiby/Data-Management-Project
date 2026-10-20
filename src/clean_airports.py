"""Clean the airports dataset.

Input : data/raw/airports.csv (Latin-1 encoded)
        (Airport_ID, Name, City, Country, IATA, ICAO, Latitude, Longitude,
         Altitude, Timezone, DST, TZ, Type, Source)
Output: data/processed/airports.csv
        (Name, City, Country, IATA, ICAO, Latitude, Longitude, Altitude,
         Timezone, TZ)

Steps:
  * drop Airport_ID, DST, Type and Source;
  * replace missing values (`\\N`) with NULL;
  * cast Latitude, Longitude, Altitude and Timezone to float.
"""

from common import PROCESSED_DIR, RAW_DIR, drop_columns, null_if_missing, read_csv, write_csv

INPUT_FILE = RAW_DIR / "airports.csv"
OUTPUT_FILE = PROCESSED_DIR / "airports.csv"

COLUMNS_TO_REMOVE = {0, 10, 12, 13}  # Airport_ID, DST, Type, Source

# Column positions after the columns above have been removed.
NAME, CITY, COUNTRY, IATA, ICAO, LATITUDE, LONGITUDE, ALTITUDE, TIMEZONE, TZ = range(10)


def clean_row(row):
    row = drop_columns(row, COLUMNS_TO_REMOVE)
    for col in (IATA, ICAO, TIMEZONE, TZ):
        row[col] = null_if_missing(row[col], {"\\N"})
    for col in (LATITUDE, LONGITUDE, ALTITUDE, TIMEZONE):
        if row[col] != "":
            row[col] = float(row[col])
    return row


def main():
    header, rows = read_csv(INPUT_FILE, encoding="latin-1")
    write_csv(OUTPUT_FILE, drop_columns(header, COLUMNS_TO_REMOVE), [clean_row(r) for r in rows])


if __name__ == "__main__":
    main()
