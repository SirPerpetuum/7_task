import requests
import socket
import time

def get_location():
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.get(
                "http://ip-api.com/json/?lang=ru",
                timeout=5,
                headers={'User-Agent': 'WeatherApp/2.0'}
            )

            if response.status_code == 429:
                wait_time = int(response.headers.get('Retry-After', 10))
                print(f"⚠️  Слишком много запросов. Повторная попытка через {wait_time} сек...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            data = response.json()

            if data['status'] == 'success':
                return (
                    data.get('city', 'Неизвестный город'),
                    data.get('regionName', 'Неизвестный регион'),
                    data.get('country', 'Неизвестная страна'),
                    data.get('lat'),
                    data.get('lon')
                )
            else:
                raise ValueError(data.get('message', 'Не удалось определить местоположение.'))

        except requests.exceptions.RequestException as e:
            print(f"🌐  Ошибка сети (попытка {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
        except Exception as e:
            print(f"⚠️  Ошибка: {e}")
            break

    print("❌  Не удалось определить местоположение после нескольких попыток.")
    return None


if __name__ == "__main__":
    print("🛰️  Тестирование определения местоположения...")
    if location := get_location():
        city, region, country, lat, lon = location
        print(f"📍  Местоположение: {city}, {region}, {country}")
        print(f"🌐  Координаты: {lat:.4f}, {lon:.4f}")
    else:
        print("❌  Тест не пройден.")