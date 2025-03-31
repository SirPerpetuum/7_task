import requests
from datetime import datetime, timedelta
import pytz
from location import get_location

WEATHER_EMOJIS = {
    'clear': '☀️',
    'cloud': '☁️',
    'rain': '🌧️',
    'snow': '❄️',
    'thunder': '⛈️',
    'fog': '🌫️',
    'wind': '💨',
    'default': '🌈'
}

def get_weather_emoji(description: str):
    description = description.lower()
    if 'ясно' in description: return WEATHER_EMOJIS['clear']
    if 'облач' in description: return WEATHER_EMOJIS['cloud']
    if 'дожд' in description: return WEATHER_EMOJIS['rain']
    if 'снег' in description: return WEATHER_EMOJIS['snow']
    if 'гроз' in description: return WEATHER_EMOJIS['thunder']
    if 'туман' in description: return WEATHER_EMOJIS['fog']
    if 'ветер' in description: return WEATHER_EMOJIS['wind']
    return WEATHER_EMOJIS['default']


def format_weather_response(data, city_name):
    weather = data['weather'][0]
    main = data['main']
    wind = data['wind']

    weather_emoji = get_weather_emoji(weather['description'])
    temp_emoji = '❄️' if main['temp'] < 0 else '🌡️'
    wind_emoji = '💨'
    feels_emoji = '🧊' if main['feels_like'] < 0 else '🔥'

    timezone_offset = data['timezone']
    current_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
    local_timezone = pytz.FixedOffset(timezone_offset // 60)
    current_time = local_timezone.localize(current_time)
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S %z")
    time_str = time_str[:-2] + ':' + time_str[-2:]

    return f"""
{weather_emoji}  Погода в {city_name} на {time_str} {weather_emoji}
{'-' * 40}
🌤️  Состояние: {weather['description'].capitalize()}
{temp_emoji}  Температура: {main['temp']:.1f}°C
{feels_emoji}  Ощущается как: {main['feels_like']:.1f}°C
💧  Влажность: {main['humidity']}%
{wind_emoji}  Ветер: {wind['speed']} м/с, порывы до {wind.get('gust', wind['speed'])} м/с
🌅  Давление: {main['pressure']} hPa
"""

def get_weather(city: str):
    api_key = 'e223023d4bae9e980e7acd48b79a329c'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            return f"⚠️  Город '{city}' не найден. Проверьте название."
        response.raise_for_status()

        return format_weather_response(response.json(), city)

    except requests.exceptions.RequestException as e:
        return f"⚠️  Ошибка при получении данных: {e}"


def get_weather_by_coordinates(lat, lon):
    api_key = '9dffb8fc5b389b94f248c1230a538272'
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ru"

    try:
        location = get_location()
        city_name = f"{location[0]}, {location[2]}" if location else "вашем местоположении"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return format_weather_response(response.json(), city_name)

    except requests.exceptions.RequestException as e:
        return f"⚠️  Ошибка при получении данных: {e}"