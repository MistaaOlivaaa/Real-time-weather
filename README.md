# Weather Data Pipeline

Pipeline météo local : Open-Meteo -> Python -> PostgreSQL -> Apache Superset.

## Prerequisites

- Ubuntu
- Python 3
- Docker and Docker Compose

## Setup

Create and activate the virtual environment:

```bash
cd ~/Desktop/weather
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Create the private environment file:

```bash
cp .env.example .env
```

Edit `.env` and replace all `replace_with_...` values with local values. Never commit `.env`.

## Run the pipeline

Start PostgreSQL and Superset:

```bash
docker compose up -d
```

Load weather observations:

```bash
source .venv/bin/activate
python scripts/seed_weather.py
```

The script collects hourly observations for Paris, Lille, Lyon, Marseille, Toulouse, and Bordeaux. Temperatures from Open-Meteo are stored in Celsius.

## Verify PostgreSQL data

```bash
docker exec weather-postgres-1 psql \
  -U weather_user \
  -d weather_db \
  -c "SELECT city, COUNT(*) FROM dev.raw_weather_data GROUP BY city;"
```

## Open Superset

Open:

```text
http://localhost:8088
```

Use the administrator credentials defined in your private `.env` file.

Add the PostgreSQL database with these values:

```text
Host: postgres
Port: 5432
Database: weather_db
Username: the value of DB_USER in .env
Password: the value of DB_PASSWORD in .env
SSL: disabled
```

Create a dataset from:

```text
Schema: dev
Table: raw_weather_data
```

For the temperature chart, use:

```text
Time column: time
Metric: AVG(temperature)
Dimension: city
Unit: Celsius (C)
```

Using `AVG(temperature)` is important. `SUM(temperature)` adds all hourly values and produces misleading results.

## Stop services

```bash
docker compose down
```

The PostgreSQL data remains in the Docker volume unless it is explicitly removed.

## Security

- `.env` is ignored by Git and must remain private.
- `.env.example` contains placeholders only.
- Do not publish passwords, secret keys, API tokens, or database connection strings with real credentials.
