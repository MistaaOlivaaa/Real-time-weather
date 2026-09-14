import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()

WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    95: "Thunderstorm",
}

LOCATIONS = (
    ("Paris", 48.8566, 2.3522),
    ("Lille", 50.6292, 3.0573),
    ("Lyon", 45.7640, 4.8357),
    ("Marseille", 43.2965, 5.3698),
    ("Toulouse", 43.6045, 1.4442),
    ("Bordeaux", 44.8378, -0.5792),
)


def connect_to_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "weather_db"),
        user=os.getenv("DB_USER", "weather_user"),
        password=os.getenv("DB_PASSWORD", "weather_password"),
    )


def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS dev")
        cursor.execute(
            """
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
            )
            """
        )
    connection.commit()
