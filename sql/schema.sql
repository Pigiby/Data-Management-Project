-- =============================================================================
-- Build the data warehouse (PostgreSQL).
--
-- Run from the repository root, after `python src/run_pipeline.py`:
--     createdb FlightsData
--     psql -d FlightsData -f sql/schema.sql
--
-- 1. Staging tables: one per cleaned CSV in data/processed/.
-- 2. Snowflake schema: dimensions (date, airport, airline, aircraft,
--    flight_number) and facts (flight, current, future, historic).
-- =============================================================================

SET client_encoding = 'UTF8';


-- =============================================================================
-- 1. STAGING TABLES
-- =============================================================================

CREATE TABLE flights_data (
    from_airport_code varchar(255),
    from_country varchar(255),
    dest_airport_code varchar(255),
    dest_country varchar(255),
    aircraft_type varchar(255),
    airline_number varchar(255),
    airline_name varchar(255),
    flight_number varchar(255),
    departure_day int,
    departure_month int,
    departure_year int,
    departure_time time,
    arrival_day int,
    arrival_month int,
    arrival_year int,
    arrival_time time,
    duration int,
    price float,
    co2_emissions int,
    avg_co2_emissions_for_this_route int,
    co2_percentage int
);

CREATE TABLE fleet_data (
    parent_airline varchar(255),
    airline varchar(255),
    aircraft_type varchar(255),
    current int,
    future int,
    historic int,
    total int,
    unit_cost_$ float,
    total_cost_$ float,
    average_age float
);

CREATE TABLE airports_data (
    name varchar(255),
    city varchar(255),
    country varchar(255),
    iata_code varchar(255),
    icao_code varchar(255),
    latitude float,
    longitude float,
    altitude float,
    timezone float,
    tz varchar(255)
);

CREATE TABLE airlines_data (
    name varchar(255),
    iata_code varchar(255),
    icao_code varchar(255),
    country varchar(255)
);

CREATE TABLE aircrafts_data (
    name varchar(255),
    iata_code varchar(255),
    icao_code varchar(255)
);

-- Empty CSV fields are loaded as NULL.
\copy flights_data   FROM 'data/processed/flights.csv'    WITH (FORMAT csv, HEADER true)
\copy fleet_data     FROM 'data/processed/fleet_data.csv' WITH (FORMAT csv, HEADER true)
\copy airports_data  FROM 'data/processed/airports.csv'   WITH (FORMAT csv, HEADER true)
\copy airlines_data  FROM 'data/processed/airlines.csv'   WITH (FORMAT csv, HEADER true)
\copy aircrafts_data FROM 'data/processed/aircraft.csv'   WITH (FORMAT csv, HEADER true)


-- =============================================================================
-- 2. SNOWFLAKE SCHEMA
-- =============================================================================

-- ----------------------------- DATE -----------------------------------------
CREATE TABLE date (
    date_key serial PRIMARY KEY,
    day int,
    month int,
    year int,
    time time
);

INSERT INTO date (day, month, year, time)
SELECT DISTINCT departure_day, departure_month, departure_year, departure_time
FROM flights_data
UNION
SELECT DISTINCT arrival_day, arrival_month, arrival_year, arrival_time
FROM flights_data;


-- ----------------------------- AIRPORT --------------------------------------
CREATE TABLE airport (
    airport_key serial PRIMARY KEY,
    airport varchar(255),
    city varchar(255),
    country varchar(255),
    iata_code varchar(255),
    icao_code varchar(255),
    latitude float,
    longitude float,
    altitude float,
    timezone float,
    tz varchar(255)
);

INSERT INTO airport (airport, city, country, iata_code, icao_code, latitude, longitude, altitude, timezone, tz)
SELECT * FROM airports_data;


-- ----------------------------- AIRLINE --------------------------------------
CREATE TABLE airline (
    airline_key serial PRIMARY KEY,
    airline varchar(255),
    iata_code varchar(255),
    icao_code varchar(255),
    base_country varchar(255),
    parent_airline varchar(255)
);

INSERT INTO airline (airline, iata_code, icao_code, base_country, parent_airline)
SELECT DISTINCT ad.name, ad.iata_code, ad.icao_code, ad.country, f.parent_airline
FROM airlines_data ad
LEFT JOIN fleet_data f ON ad.name = f.airline;


-- ----------------------------- AIRCRAFT -------------------------------------
CREATE TABLE aircraft (
    aircraft_key serial PRIMARY KEY,
    aircraft_type varchar(255),
    iata_code varchar(255),
    icao_code varchar(255),
    unit_cost_$ float
);

INSERT INTO aircraft (aircraft_type, iata_code, icao_code, unit_cost_$)
SELECT DISTINCT ac.name, ac.iata_code, ac.icao_code, f.unit_cost_$
FROM aircrafts_data ac
JOIN fleet_data f ON ac.name = f.aircraft_type
WHERE f.unit_cost_$ IS NOT NULL;


-- ----------------------------- FLIGHT NUMBER --------------------------------
CREATE TABLE flight_number (
    flight_number_key serial PRIMARY KEY,
    flight_number varchar(255) NOT NULL,
    airline int NOT NULL REFERENCES airline(airline_key),
    airport_src int NOT NULL REFERENCES airport(airport_key),
    airport_dest int NOT NULL REFERENCES airport(airport_key)
);

INSERT INTO flight_number (flight_number, airline, airport_src, airport_dest)
SELECT DISTINCT f.flight_number, a.airline_key, a1.airport_key, a2.airport_key
FROM flights_data f
JOIN airline a  ON f.airline_name = a.airline
JOIN airport a1 ON f.from_airport_code = a1.iata_code
JOIN airport a2 ON f.dest_airport_code = a2.iata_code;


-- ----------------------------- FLIGHT (fact) --------------------------------
CREATE TABLE flight (
    departure_date int REFERENCES date(date_key),
    arrival_date int REFERENCES date(date_key),
    departure_airport int REFERENCES airport(airport_key),
    arrival_airport int REFERENCES airport(airport_key),
    aircraft int REFERENCES aircraft(aircraft_key),
    airline int REFERENCES airline(airline_key),
    flight_number int REFERENCES flight_number(flight_number_key),
    duration int,
    price float,
    co2_emissions int,
    avg_co2_emissions_for_this_route int,
    co2_percentage int,
    PRIMARY KEY (departure_date, arrival_date, departure_airport, arrival_airport, airline, aircraft, flight_number)
);

INSERT INTO flight
SELECT DISTINCT d1.date_key, d2.date_key, a1.airport_key, a2.airport_key, ac.aircraft_key,
       al.airline_key, fn.flight_number_key, f.duration, f.price, f.co2_emissions,
       f.avg_co2_emissions_for_this_route, f.co2_percentage
FROM flights_data f
JOIN date d1 ON d1.day = f.departure_day AND d1.month = f.departure_month
            AND d1.year = f.departure_year AND d1.time = f.departure_time
JOIN date d2 ON d2.day = f.arrival_day AND d2.month = f.arrival_month
            AND d2.year = f.arrival_year AND d2.time = f.arrival_time
JOIN airport a1       ON a1.iata_code = f.from_airport_code
JOIN airport a2       ON a2.iata_code = f.dest_airport_code
JOIN aircraft ac      ON ac.aircraft_type = f.aircraft_type
JOIN airline al       ON al.airline = f.airline_name
JOIN flight_number fn ON fn.flight_number = f.flight_number;


-- ----------------------------- FLEET facts ----------------------------------
-- Number of aircraft of each type an airline currently operates / has
-- ordered / operated in the past.
CREATE TABLE current (
    airline_key int NOT NULL REFERENCES airline(airline_key),
    aircraft_key int NOT NULL REFERENCES aircraft(aircraft_key),
    current int
);

INSERT INTO current
SELECT DISTINCT al.airline_key, ac.aircraft_key, f.current
FROM fleet_data f
JOIN airline al  ON f.airline = al.airline
JOIN aircraft ac ON f.aircraft_type = ac.aircraft_type;

CREATE TABLE future (
    airline_key int NOT NULL REFERENCES airline(airline_key),
    aircraft_key int NOT NULL REFERENCES aircraft(aircraft_key),
    future int
);

INSERT INTO future
SELECT DISTINCT al.airline_key, ac.aircraft_key, f.future
FROM fleet_data f
JOIN airline al  ON f.airline = al.airline
JOIN aircraft ac ON f.aircraft_type = ac.aircraft_type;

CREATE TABLE historic (
    airline_key int NOT NULL REFERENCES airline(airline_key),
    aircraft_key int NOT NULL REFERENCES aircraft(aircraft_key),
    historic int
);

INSERT INTO historic
SELECT DISTINCT al.airline_key, ac.aircraft_key, f.historic
FROM fleet_data f
JOIN airline al  ON f.airline = al.airline
JOIN aircraft ac ON f.aircraft_type = ac.aircraft_type;
