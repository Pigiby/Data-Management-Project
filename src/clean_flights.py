"""Clean the flights dataset and align its airline names with the airlines dataset.

Inputs: data/raw/flights_nonstop.csv  (non-stop flights, see filter_nonstop_flights.py)
        data/processed/airlines.csv   (output of clean_airlines.py)
Output: data/processed/flights.csv

Steps:
  * remove the square brackets around the airline name and lower-case it;
  * cast duration, CO2 emissions and CO2 percentage to int, price to float;
  * strip the '%' sign from co2_percentage ('None%' becomes NULL);
  * drop stops (always 0), currency (always USD) and scan_date;
  * split departure/arrival timestamps into day, month, year and time columns;
  * rename airlines whose name is a shortened form of a name in the airlines
    dataset (e.g. "lufthansa" -> "lufthansa german airlines"), provided that
    the IATA airline code matches too.
"""

from datetime import datetime

from common import PROCESSED_DIR, RAW_DIR, drop_columns, read_csv, write_csv

INPUT_FILE = RAW_DIR / "flights_nonstop.csv"
AIRLINES_FILE = PROCESSED_DIR / "airlines.csv"
OUTPUT_FILE = PROCESSED_DIR / "flights.csv"

(FROM_AIRPORT, FROM_COUNTRY, DEST_AIRPORT, DEST_COUNTRY, AIRCRAFT_TYPE,
 AIRLINE_NUMBER, AIRLINE_NAME, FLIGHT_NUMBER, DEPARTURE_TIME, ARRIVAL_TIME,
 DURATION, STOPS, PRICE, CURRENCY, CO2_EMISSIONS, AVG_CO2_EMISSIONS,
 CO2_PERCENTAGE, SCAN_DATE) = range(18)
COLUMNS_TO_REMOVE = {STOPS, CURRENCY, SCAN_DATE}

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def split_datetime(value):
    """'2022-05-29 12:55:00' -> [29, 5, 2022, time(12, 55)]"""
    dt = datetime.strptime(value, DATETIME_FORMAT)
    return [dt.day, dt.month, dt.year, dt.time()]


def build_header(header):
    new_header = []
    for idx, name in enumerate(header):
        if idx in COLUMNS_TO_REMOVE:
            continue
        if idx == DEPARTURE_TIME:
            new_header += ["departure_day", "departure_month", "departure_year", "departure_time"]
        elif idx == ARRIVAL_TIME:
            new_header += ["arrival_day", "arrival_month", "arrival_year", "arrival_time"]
        else:
            new_header.append(name)
    return new_header


def clean_row(row):
    row[AIRLINE_NAME] = row[AIRLINE_NAME].strip("[]").lower()
    for col in (DURATION, CO2_EMISSIONS, AVG_CO2_EMISSIONS):
        if row[col] != "":
            row[col] = int(row[col])
    if row[PRICE] != "":
        row[PRICE] = float(row[PRICE])
    if row[CO2_PERCENTAGE] != "":
        percentage = row[CO2_PERCENTAGE].rstrip("%")
        row[CO2_PERCENTAGE] = "" if percentage == "None" else int(percentage)

    new_row = []
    for idx, value in enumerate(row):
        if idx in COLUMNS_TO_REMOVE:
            continue
        if idx in (DEPARTURE_TIME, ARRIVAL_TIME):
            new_row += split_datetime(value)
        else:
            new_row.append(value)
    return new_row


def match_airline_name(name, iata_code, airlines):
    """Map a flight's airline name onto a name from the airlines dataset.

    `airlines` is a list of (name, iata_code) pairs. A known name replaces
    `name` when `name` is a strict substring of it and the IATA codes agree.
    The comparison continues with the replaced name, so the last match wins.
    """
    if name in {known_name for known_name, _ in airlines}:
        return name
    for known_name, known_iata in airlines:
        if len(name) < len(known_name) and name in known_name and iata_code == known_iata:
            name = known_name
    return name


def main():
    _, airline_rows = read_csv(AIRLINES_FILE)
    airlines = [(row[0], row[1]) for row in airline_rows]  # (Name, IATA)

    header, rows = read_csv(INPUT_FILE)
    cleaned = [clean_row(r) for r in rows]

    # Column positions are unchanged before AIRLINE_NAME, so they still apply.
    for row in cleaned:
        row[AIRLINE_NAME] = match_airline_name(row[AIRLINE_NAME], row[AIRLINE_NUMBER], airlines)

    write_csv(OUTPUT_FILE, build_header(header), cleaned)


if __name__ == "__main__":
    main()
