import requests


def fetch_data(url):
    print("Fetching data from Open Meteo API...")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Data fetched successfully.")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
        
