from datetime import datetime
from urllib.parse import urlencode



from api_request import fetch_data
from inser_records import LOCATIONS, WEATHER_DESCRIPTIONS, connect_to_db, create_table


def seed_location(conn, city, latitude, longitude):
    query = urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,weather_code,wind_speed_10m",
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "auto",
    })
    data = fetch_data(f"https://api.open-meteo.com/v1/forecast?{query}")
    if not data or "hourly" not in data or "current" not in data:
        print(f"No weather data available for {city}")
        return

    hourly = data["hourly"]
    utc_offset = str(data.get("utc_offset_seconds", 0) / 3600)
    now = datetime.fromisoformat(data["current"]["time"])

    rows = []
    for timestamp, temperature, code, wind_speed in zip(
        hourly["time"],
        hourly["temperature_2m"],
        hourly["weather_code"],
        hourly["wind_speed_10m"],
    ):
        if datetime.fromisoformat(timestamp) <= now:
            rows.append((
                city,
                temperature,
                WEATHER_DESCRIPTIONS.get(code, f"WMO code {code}"),
                wind_speed,
                timestamp,
                utc_offset,
            ))

    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO dev.raw_weather_data
                (city, temperature, weather_description, wind_speed, time, inserted_at, utc_offset)
            SELECT %s, %s, %s, %s, %s, NOW(), %s
            WHERE NOT EXISTS (
                SELECT 1 FROM dev.raw_weather_data WHERE city = %s AND time = %s
            );
        """, [row + (row[0], row[4]) for row in rows])
    conn.commit()
    print(f"Seeded {len(rows)} hourly observations for {city}")


def main():
    conn = connect_to_db()
    try:
        create_table(conn)
        for location in LOCATIONS:
            seed_location(conn, *location)
    finally:
        conn.close()


if __name__ == "__main__":
    main()

    

