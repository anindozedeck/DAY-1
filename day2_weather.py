import os

import requests
from dotenv import load_dotenv


API_URL = "https://api.openweathermap.org/data/2.5/weather"
CITY = "Mombasa"


def fetch_weather(api_key):
    try:
        response = requests.get(
            API_URL,
            params={"q": CITY, "appid": api_key, "units": "metric"},
            timeout=10,
        )
    except requests.exceptions.Timeout:
        print("The weather request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        print("Could not connect to the weather service. Check your internet connection.")
        return None
    except requests.exceptions.RequestException as error:
        print(f"Could not fetch weather data: {error}")
        return None

    if response.status_code == 401:
        print("The API key is invalid or not active. Check OPENWEATHER_API_KEY in .env.")
        return None
    if response.status_code == 404:
        print(f"City not found: {CITY}. Check the city name.")
        return None
    if response.status_code == 429:
        print("The API rate limit was reached. Wait before trying again.")
        return None

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"The weather service returned an unexpected HTTP {response.status_code} error.")
        return None

    try:
        data = response.json()
    except ValueError:
        print("The weather service returned an invalid response.")
        return None

    if not isinstance(data, dict):
        print("The weather service returned an invalid response.")
        return None

    return data


def format_weather(data):
    try:
        weather = data["weather"][0]
        return (
            f"CURRENT WEATHER - {CITY.upper()}\n"
            "------------------------------\n"
            f"Conditions: {weather['description'].capitalize()}\n"
            f"Temperature: {data['main']['temp']:.1f} C\n"
            f"Humidity: {data['main']['humidity']}%"
        )
    except (IndexError, KeyError, TypeError, ValueError):
        return None


def main():
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("OPENWEATHER_API_KEY is missing. Add it to your .env file.")
        return

    data = fetch_weather(api_key)
    if data is None:
        return

    weather_report = format_weather(data)
    if weather_report is None:
        print("The weather service response was missing valid weather details.")
        return

    print(weather_report)


if __name__ == "__main__":
    main()
