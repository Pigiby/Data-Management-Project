"""Run every cleaning step, turning data/raw/ into data/processed/.

Usage (from the repository root):
    python src/run_pipeline.py
"""

import clean_aircraft
import clean_airlines
import clean_airports
import clean_fleet
import clean_flights

# clean_flights reads data/processed/airlines.csv, so airlines must run first.
STEPS = [clean_aircraft, clean_airlines, clean_airports, clean_fleet, clean_flights]


def main():
    for step in STEPS:
        print(f"--- {step.__name__}")
        step.main()


if __name__ == "__main__":
    main()
