from django.test import TestCase

import requests


def test_connection():
    city = "London"
    api_key = '84fad9dbc7b69150bca2b74bcbfd4b94'  # Замените на ваш API ключ
    geo_api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"

    try:
        geo_response = requests.get(geo_api_url)
        geo_response.raise_for_status()
        print("Geolocation API works.")
        geo_data = geo_response.json()[0]
        lat, lon = geo_data['lat'], geo_data['lon']

        weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_api_url)
        weather_response.raise_for_status()
        print("Weather API works.")
        weather_data = weather_response.json()
        print(weather_data)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


test_connection()
