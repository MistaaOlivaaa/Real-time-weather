CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    temperature FLOAT,
    weather_description VARCHAR(100),
    wind_speed FLOAT,
    time TIMESTAMP NOT NULL,
    inserted_at TIMESTAMP DEFAULT NOW(),
    utc_offset VARCHAR(20),
    UNIQUE (city, time)
);