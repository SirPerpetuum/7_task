from weather import get_weather, get_weather_by_coordinates
from history import save_history, print_history
from location import get_location
from datetime import datetime
import sys


def display_menu():
    print("\n🌦️  Погодный терминал")
    print("=" * 30)
    print("1. 🌍  Погода по названию города")
    print("2. 📜  История запросов")
    print("3. 📍  Погода по моему местоположению")
    print("4. ❌  Выход")
    print("=" * 30)


def handle_choice(choice):
    try:
        if choice == '1':
            city = input("🏙️  Введите название города: ").strip()
            if not city:
                print("Название города не может быть пустым!")
                return True

            weather_info = get_weather(city)
            if weather_info:
                print(f"\n{weather_info}")
                save_history({
                    "city": city,
                    "weather": weather_info,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                print("Не удалось получить данные о погоде.")

        elif choice == '3':
            print("\n🛰️  Определяем ваше местоположение...")
            location = get_location()
            if location:
                city, region, country, lat, lon = location
                weather_info = get_weather_by_coordinates(lat, lon)
                if weather_info:
                    print(f"\n{weather_info}")
                    save_history({
                        "city": f"{city}, {region}, {country}",
                        "weather": weather_info,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                else:
                    print("Не удалось получить данные о погоде для вашего местоположения")
            else:
                print("Не удалось определить местоположение. Проверьте интернет-соединение")

        elif choice == '2':
            print("\n📚  История запросов:")
            print_history()

        elif choice == '4':
            print("\nДо свидания! Хорошего дня!")
            return False

        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 1 до 4")

    except Exception as e:
        print("Попробуйте снова")

    return True


def main():
    while True:
        try:
            display_menu()
            choice = input("👉  Выберите действие (1-4): ").strip()

            if not handle_choice(choice):
                sys.exit(0)

        except KeyboardInterrupt:
            print("\n\n Окончание работы программы")
            sys.exit(1)

if __name__ == '__main__':
    main()