from datetime import datetime

import requests


URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": -1.286389,
    "longitude": 36.817223,
    "current": (
        "temperature_2m,relative_humidity_2m,apparent_temperature,"
        "precipitation,weather_code,wind_speed_10m"
    ),
    "timezone": "Africa/Nairobi",
}
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def format_weather(data):
    current = data["current"]
    observed_at = datetime.fromisoformat(current["time"])
    condition = WEATHER_CODES.get(
        current["weather_code"],
        f"Unknown weather code ({current['weather_code']})",
    )

    return (
        "NAIROBI, KENYA - CURRENT WEATHER\n"
        "---------------------------------\n"
        f"Observed: {observed_at.strftime('%A, %B %d at %H:%M')} (local time)\n"
        f"Conditions: {condition}\n"
        f"Temperature: {current['temperature_2m']:.1f} C\n"
        f"Feels like: {current['apparent_temperature']:.1f} C\n"
        f"Humidity: {current['relative_humidity_2m']}%\n"
        f"Precipitation: {current['precipitation']:.1f} mm\n"
        f"Wind speed: {current['wind_speed_10m']:.1f} km/h"
    )


def main():
    try:
        response = requests.get(URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as error:
        print(f"Could not fetch weather data: {error}")
        return
    except ValueError as error:
        print(f"The API returned invalid data: {error}")
        return

    if not isinstance(data, dict) or not isinstance(data.get("current"), dict):
        print("The API response did not include current weather data.")
        return

    try:
        print(format_weather(data))
    except (KeyError, TypeError, ValueError) as error:
        print(f"The API response was missing valid weather details: {error}")


if __name__ == "__main__":
    main()