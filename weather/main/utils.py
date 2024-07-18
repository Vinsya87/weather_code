import requests


def get_weather(city):
    lat, lon = get_coordinates_from_api(city)
    if lat is None or lon is None:
        return None

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
        return data['current_weather']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных о погоде: {e}")
        return None


def get_coordinates_from_api(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru&format=json&strict_limit=true"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
        if 'results' in data and data['results']:
            result = data['results'][0]
            # Сравниваем в нижнем регистре для точного совпадения
            if result.get('name').lower() == city.lower():
                return result['latitude'], result['longitude']
            else:
                print(f"Не найдено точного совпадения для города: {city}")
                return None, None
        else:
            print(f"Не найдено города: {city}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения координат: {e}")
        return None, None
