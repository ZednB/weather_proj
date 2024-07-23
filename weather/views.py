import requests
from django.shortcuts import render

from weather.forms import CityForm


def get_weather(city):
    weather_api = '84fad9dbc7b69150bca2b74bcbfd4b94'
    geo_api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={weather_api}"

    try:

        geo_response = requests.get(geo_api_url)
        geo_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation data: {e}")
        return None

    if len(geo_response.json()) > 0:
        geo_data = geo_response.json()[0]
        lat, lon = geo_data['lat'], geo_data['lon']

        weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

        try:
            weather_response = requests.get(weather_api_url)
            weather_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

        weather_data = weather_response.json()
        weather_data['city'] = city
        return weather_data

    return None


def index(request):
    weather_data = None
    error_message = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather(city)
            if not weather_data:
                error_message = "Could not retrieve weather data. Please try again later."
    else:
        form = CityForm
    return render(request, 'weather/index.html', {'form': form, 'weather_data': weather_data})
