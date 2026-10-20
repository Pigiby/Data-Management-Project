-- =============================================================================
-- ROLAP analysis queries over the snowflake schema (PostgreSQL).
--
-- Run after sql/schema.sql:
--     psql -d FlightsData -f sql/queries.sql
-- =============================================================================


-- Q1: For each route, the aircraft with the lowest CO2 emissions.
SELECT DISTINCT a1.airport AS departure_airport, a2.airport AS arrival_airport,
       ac.aircraft_type, f.co2_emissions
FROM flight f
JOIN airport a1  ON f.departure_airport = a1.airport_key
JOIN airport a2  ON f.arrival_airport = a2.airport_key
JOIN aircraft ac ON ac.aircraft_key = f.aircraft
WHERE f.co2_emissions <= ALL (SELECT f2.co2_emissions
                              FROM flight f2
                              WHERE f2.departure_airport = f.departure_airport
                                AND f2.arrival_airport = f.arrival_airport)
ORDER BY departure_airport, arrival_airport;


-- Q2: For each aircraft type, the average CO2 emission per minute of flight.
SELECT ac.aircraft_type, sum(f.co2_emissions) / sum(f.duration) AS average_co2_emissions_per_minute
FROM flight f
JOIN aircraft ac ON f.aircraft = ac.aircraft_key
GROUP BY ac.aircraft_type;


-- Q3: For each airline, all the routes it flies.
SELECT DISTINCT a1.airport AS departure_airport, a2.airport AS arrival_airport, al.airline
FROM flight f
JOIN airport a1 ON f.departure_airport = a1.airport_key
JOIN airport a2 ON f.arrival_airport = a2.airport_key
JOIN airline al ON al.airline_key = f.airline
ORDER BY al.airline;


-- Q4: For each airline, the month with the most extreme average CO2 emission
-- per minute.
-- NOTE: `<= ALL` returns the month with the LOWEST value; use `>= ALL` for
-- the highest.
CREATE VIEW monthly_avg_per_minute AS
SELECT a.airline, d.month, sum(f.co2_emissions) / sum(f.duration) AS monthly
FROM flight f
JOIN airline a ON f.airline = a.airline_key
JOIN date d    ON f.departure_date = d.date_key
GROUP BY a.airline, d.month;

SELECT airline, month, monthly
FROM monthly_avg_per_minute m1
WHERE monthly <= ALL (SELECT m2.monthly
                      FROM monthly_avg_per_minute m2
                      WHERE m2.airline = m1.airline);


-- Q5: For each airline and month, the number of flights (on the staging table).
SELECT airline_name, departure_month, count(*)
FROM flights_data
GROUP BY airline_name, departure_month
ORDER BY airline_name, departure_month;


-- Q6: For each route, the airline with the highest CO2 percentage with respect
-- to the average emission for that route.
SELECT DISTINCT a1.airport AS departure_airport, a2.airport AS arrival_airport,
       a.airline, f.co2_percentage
FROM flight f
JOIN airport a1 ON f.departure_airport = a1.airport_key
JOIN airport a2 ON f.arrival_airport = a2.airport_key
JOIN airline a  ON f.airline = a.airline_key
WHERE f.co2_percentage >= ALL (SELECT f2.co2_percentage
                               FROM flight f2
                               WHERE f2.departure_airport = f.departure_airport
                                 AND f2.arrival_airport = f.arrival_airport);


-- Q7: For each airport and month, the number of incoming + outgoing flights.
SELECT a.airport, a.city, a.country, d.month, count(*)
FROM flight f
JOIN date d ON f.departure_date = d.date_key,
     airport a
WHERE a.airport_key = f.departure_airport OR a.airport_key = f.arrival_airport
GROUP BY a.airport, a.city, a.country, d.month
ORDER BY a.airport, d.month;


-- Q8: For each airline, the total number of aircraft currently in its fleet.
SELECT a.airline, sum(c.current)
FROM airline a
JOIN current c ON c.airline_key = a.airline_key
GROUP BY a.airline
ORDER BY a.airline;


-- Q9: Top 10 aircraft types currently in use.
SELECT ac.aircraft_type, sum(c.current)
FROM aircraft ac
JOIN current c ON ac.aircraft_key = c.aircraft_key
GROUP BY ac.aircraft_type
ORDER BY sum(c.current) DESC
LIMIT 10;


-- Q10: For each airline, how many different aircraft types it currently owns.
SELECT a.airline, count(DISTINCT c.aircraft_key)
FROM airline a
JOIN current c ON a.airline_key = c.airline_key
WHERE c.current != 0
GROUP BY a.airline;


-- Q11: Investments in the least polluting aircraft.

-- For each route, the least polluting aircraft.
CREATE VIEW less_polluting_aircraft AS
SELECT DISTINCT a1.iata_code AS departure, a2.iata_code AS arrival, ac.aircraft_type, f.co2_emissions
FROM flight f
JOIN airport a1  ON f.departure_airport = a1.airport_key
JOIN airport a2  ON f.arrival_airport = a2.airport_key
JOIN aircraft ac ON f.aircraft = ac.aircraft_key
WHERE f.co2_emissions <= ALL (SELECT f2.co2_emissions
                              FROM flight f2
                              WHERE f2.departure_airport = f.departure_airport
                                AND f2.arrival_airport = f.arrival_airport);

-- For each airline, the routes it flies.
CREATE VIEW routes_per_airline AS
SELECT DISTINCT a1.iata_code AS departure, a2.iata_code AS arrival, al.airline
FROM flight f
JOIN airport a1 ON f.departure_airport = a1.airport_key
JOIN airport a2 ON f.arrival_airport = a2.airport_key
JOIN airline al ON al.airline_key = f.airline;

-- For each route flown by an airline: how many of the route's least polluting
-- aircraft the airline owns or has ordered, and how much they are worth.
CREATE VIEW airlines_investments AS
SELECT DISTINCT al.airline, al.base_country, ac.aircraft_type,
       (c.current + fu.future) AS quantity,
       (c.current + fu.future) * ac.unit_cost_$ AS investment
FROM routes_per_airline r
JOIN less_polluting_aircraft l ON r.departure = l.departure AND r.arrival = l.arrival
JOIN airline al  ON al.airline = r.airline
JOIN aircraft ac ON ac.aircraft_type = l.aircraft_type
JOIN current c   ON c.airline_key = al.airline_key AND c.aircraft_key = ac.aircraft_key
JOIN future fu   ON fu.airline_key = al.airline_key AND fu.aircraft_key = ac.aircraft_key
WHERE c.current != 0 OR fu.future != 0;

-- Top 20 countries investing in the least polluting aircraft for their routes.
SELECT base_country, sum(quantity) AS total_aircrafts, sum(investment) AS investment_total
FROM airlines_investments
GROUP BY base_country
ORDER BY investment_total DESC
LIMIT 20;


-- Q12: For each aircraft type, the number of aircraft currently operating.
SELECT ac.aircraft_type, sum(c.current) AS total
FROM aircraft ac
JOIN current c ON ac.aircraft_key = c.aircraft_key
GROUP BY ac.aircraft_type
ORDER BY total DESC;


-- Q13: For each route and month, the average ticket price.
SELECT a1.airport, a1.city, a2.airport, a2.city, d.month, avg(f.price)
FROM flight f
JOIN airport a1 ON f.departure_airport = a1.airport_key
JOIN airport a2 ON f.arrival_airport = a2.airport_key
JOIN date d     ON f.departure_date = d.date_key
GROUP BY a1.airport, a1.city, a2.airport, a2.city, d.month
ORDER BY a1.airport, a1.city, a2.airport, a2.city, d.month;


-- Q14: For each day, the total CO2 emitted by all flights.
SELECT d.day, d.month, d.year, sum(f.co2_emissions)
FROM flight f
JOIN date d ON f.departure_date = d.date_key
GROUP BY d.day, d.month, d.year
ORDER BY d.year, d.month, d.day;
