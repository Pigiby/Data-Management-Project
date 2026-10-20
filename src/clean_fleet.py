"""Clean the airline fleet dataset.

Input : data/raw/fleet_data.csv (UTF-8 with BOM)
        (Parent Airline, Airline, Aircraft Type, Current, Future, Historic,
         Total, Orders, Unit Cost, Total Cost (Current), Average Age)
Output: data/processed/fleet_data.csv
        (Parent Airline, Airline, Aircraft Type, Current, Future, Historic,
         Total, Unit Cost, Total Cost (Current), Average Age)

Steps:
  * drop the Orders column;
  * lower-case Parent Airline and Airline (to join with the airlines dataset);
  * cast Current/Future/Historic/Total to int, missing values become 0;
  * convert costs from "$<millions>" strings (e.g. "$3,724") to dollars;
  * cast Average Age to float;
  * harmonise Unit Cost: the same aircraft type can be listed with different
    unit costs by different airlines, so every row gets the most frequent unit
    cost of its aircraft type.
"""

from collections import Counter

from common import PROCESSED_DIR, RAW_DIR, drop_columns, read_csv, write_csv

INPUT_FILE = RAW_DIR / "fleet_data.csv"
OUTPUT_FILE = PROCESSED_DIR / "fleet_data.csv"

COLUMNS_TO_REMOVE = {7}  # Orders

# Column positions after Orders has been removed.
(PARENT_AIRLINE, AIRLINE, AIRCRAFT_TYPE, CURRENT, FUTURE, HISTORIC, TOTAL,
 UNIT_COST, TOTAL_COST, AVERAGE_AGE) = range(10)


def parse_millions_of_dollars(value):
    """'$3,724' -> 3724000000.0 (the source expresses costs in millions of $)."""
    return float(value.lstrip("$").replace(",", "")) * 1_000_000


def clean_row(row):
    row = drop_columns(row, COLUMNS_TO_REMOVE)
    row[PARENT_AIRLINE] = row[PARENT_AIRLINE].lower()
    row[AIRLINE] = row[AIRLINE].lower()
    for col in (CURRENT, FUTURE, HISTORIC, TOTAL):
        row[col] = int(row[col]) if row[col] != "" else 0
    for col in (UNIT_COST, TOTAL_COST):
        if row[col] != "":
            row[col] = parse_millions_of_dollars(row[col])
    if row[AVERAGE_AGE] != "":
        row[AVERAGE_AGE] = float(row[AVERAGE_AGE])
    return row


def harmonise_unit_cost(rows):
    """Give every aircraft type its most frequent unit cost (ties: first seen)."""
    costs_per_type = {}
    for row in rows:
        costs_per_type.setdefault(row[AIRCRAFT_TYPE], []).append(row[UNIT_COST])
    most_common_cost = {
        aircraft_type: Counter(costs).most_common(1)[0][0]
        for aircraft_type, costs in costs_per_type.items()
    }
    for row in rows:
        row[UNIT_COST] = most_common_cost[row[AIRCRAFT_TYPE]]
    return rows


def main():
    header, rows = read_csv(INPUT_FILE, encoding="utf-8-sig")
    cleaned = harmonise_unit_cost([clean_row(r) for r in rows])
    write_csv(OUTPUT_FILE, drop_columns(header, COLUMNS_TO_REMOVE), cleaned)


if __name__ == "__main__":
    main()
