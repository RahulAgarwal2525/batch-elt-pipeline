-- Docker automatically runs this script the FIRST time the Postgres container starts.
-- It ensures our database schema is perfectly configured before any Python code runs.

-- 1. Create a raw table for ingested data (Staging Layer)
CREATE TABLE IF NOT EXISTS raw_weather_data (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    temperature_celsius NUMERIC(5, 2), -- Allow decimals like 25.50
    humidity_percentage INT,
    weather_condition VARCHAR(50),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create an analytical table for clean, processed data (Production Layer)
CREATE TABLE IF NOT EXISTS daily_weather_summary (
    id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    avg_temperature NUMERIC(5, 2),
    max_humidity INT,
    total_records INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Ensure we only have one summary row per city per day
    UNIQUE (report_date, city_name) 
);

-- Note: We are separating "raw" data from "clean" data. 