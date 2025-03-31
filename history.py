from datetime import datetime

history = []

def save_history(entry):
    try:
        if not isinstance(entry, dict):
            raise ValueError("Запись должна быть словарем")

        required_keys = ['city', 'weather', 'time']
        if not all(key in entry for key in required_keys):
            raise ValueError(f"Запись должна содержать ключи: {required_keys}")

        entry["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.append(entry)

    except Exception as e:
        print(f"Ошибка при сохранении истории: {e}")


def print_history():
    if not history:
        print("📭  История запросов пуста.")
        return

    try:
        count = input("🔢  Сколько последних запросов показать? (Enter - все): ").strip()
        history_to_show = history[-int(count):][::-1] if count.isdigit() else history[::-1]

        print("\n📜  Последние запросы:")
        print("=" * 50)
        for i, entry in enumerate(history_to_show, 1):
            print(f"\n🔍  Запрос #{i}: {entry['time']}")
            print(f"🏙️  Город: {entry['city']}")
            print(entry['weather'])
            print("-" * 50)

    except Exception as e:
        print(f"Ошибка при выводе истории: {e}")