import time
from datetime import date, datetime, timedelta
import json
import requests


def get_temperature(dict_city_lat_long, app_id):
    """
    Функция получает для центров городов с максимальным количеством отелей(по заданию) погоду:
        - за предыдущие 5 дней, включая текущий;
    - прогноз: на последующие 5 дней;
    - текущие значения;
     через API сайта https://api.openweathermap.org/
    :param dict_city-lat_long: словарь с городами и их координатами
    :param app_id: API ключ сайта https://api.openweathermap.org/
    :return min_temperature, max_temperature:
    """
    # Определяем дату в нужном формате, предыдущий день
    days_before_1dt = date.today() - timedelta(days=1)
    # Конвертируем время в формат, нужный при обращении к One Call API(openweathermap.org/), (Unix time, UTC time zone)
    days_before_1 = int(time.mktime(days_before_1dt.timetuple()))

    # То же и для предыдущих дней
    days_before_2dt = date.today() - timedelta(days=2)
    days_before_2 = int(time.mktime(days_before_2dt.timetuple()))

    days_before_3dt = date.today() - timedelta(days=3)
    days_before_3 = int(time.mktime(days_before_3dt.timetuple()))

    days_before_4dt = date.today() - timedelta(days=4)
    days_before_4 = int(time.mktime(days_before_4dt.timetuple()))

    # Будем возвращать словари с кортежем {(Страна, Город): {даты:температуры}}
    min_temperature = dict()
    max_temperature = dict()

    # Обращение к One Call API(openweathermap.org/)
    api_url = "https://api.openweathermap.org/data/2.5/onecall"

    # Информацию берем из словаря с городами и их координатами
    for city, lat_long in dict_city_lat_long.items():
        lat = lat_long[0]
        lon = lat_long[1]

        params = {
            "lat": lat,
            "lon": lon,
            "appid": app_id,
            "units": "metric",
            "exclude": "minutely, alerts",
        }

        try:
            if requests.get(api_url, params=params):
                # Значения температуры для текущего дня и прогноз на 5 дней
                current_and_forecast_weather = requests.get(api_url, params=params)
                current_and_forecast_data = current_and_forecast_weather.json()

                # Значения температуры для предыдущих дней
                previous_1_day = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_1}}
                )
                data_1_day_before = previous_1_day.json()

                previous_2_days = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_2}}
                )
                data_2_days_before = previous_2_days.json()

                previous_3_days = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_3}}
                )
                data_3_days_before = previous_3_days.json()

                previous_4_days = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_4}}
                )
                data_4_days_before = previous_4_days.json()

                # Записываем в переменные необходимые даты и находим минимальные/максимальные температуры для каждого дня
                four_days_before = days_before_4dt.strftime("%Y-%m-%d")
                min_temp_four_days_before = min(
                    [t["temp"] for t in data_4_days_before["hourly"]]
                )
                max_temp_four_days_before = max(
                    [t["temp"] for t in data_4_days_before["hourly"]]
                )

                three_days_before = days_before_3dt.strftime("%Y-%m-%d")
                min_temp_three_days_before = min(
                    [t["temp"] for t in data_3_days_before["hourly"]]
                )
                max_temp_three_days_before = max(
                    [t["temp"] for t in data_3_days_before["hourly"]]
                )

                two_days_before = days_before_2dt.strftime("%Y-%m-%d")
                min_temp_two_days_before = min(
                    [t["temp"] for t in data_2_days_before["hourly"]]
                )
                max_temp_two_days_before = max(
                    [t["temp"] for t in data_2_days_before["hourly"]]
                )

                day_before = days_before_1dt.strftime("%Y-%m-%d")
                min_temp_day_before = min(
                    [t["temp"] for t in data_1_day_before["hourly"]]
                )
                max_temp_day_before = max(
                    [t["temp"] for t in data_1_day_before["hourly"]]
                )

                today = date.today().strftime("%Y-%m-%d")
                min_temp_today = current_and_forecast_data["daily"][0]["temp"]["min"]
                max_temp_today = current_and_forecast_data["daily"][0]["temp"]["max"]

                next_day = datetime.utcfromtimestamp(
                    current_and_forecast_data["daily"][1:6][0]["dt"]
                ).strftime("%Y-%m-%d")
                min_temp_next_day = current_and_forecast_data["daily"][1:6][0]["temp"][
                    "min"
                ]
                max_temp_next_day = current_and_forecast_data["daily"][1:6][0]["temp"][
                    "max"
                ]

                two_days_after = datetime.utcfromtimestamp(
                    current_and_forecast_data["daily"][1:6][1]["dt"]
                ).strftime("%Y-%m-%d")
                min_temp_two_days_after = current_and_forecast_data["daily"][1:6][1][
                    "temp"
                ]["min"]
                max_temp_two_days_after = current_and_forecast_data["daily"][1:6][1][
                    "temp"
                ]["max"]

                three_days_after = datetime.utcfromtimestamp(
                    current_and_forecast_data["daily"][1:6][2]["dt"]
                ).strftime("%Y-%m-%d")
                min_temp_three_days_after = current_and_forecast_data["daily"][1:6][2][
                    "temp"
                ]["min"]
                max_temp_three_days_after = current_and_forecast_data["daily"][1:6][2][
                    "temp"
                ]["max"]

                four_days_after = datetime.utcfromtimestamp(
                    current_and_forecast_data["daily"][1:6][3]["dt"]
                ).strftime("%Y-%m-%d")
                min_temp_four_days_after = current_and_forecast_data["daily"][1:6][3][
                    "temp"
                ]["min"]
                max_temp_four_days_after = current_and_forecast_data["daily"][1:6][3][
                    "temp"
                ]["max"]

                five_days_after = datetime.utcfromtimestamp(
                    current_and_forecast_data["daily"][1:6][4]["dt"]
                ).strftime("%Y-%m-%d")
                min_temp_five_days_after = current_and_forecast_data["daily"][1:6][4][
                    "temp"
                ]["min"]
                max_temp_five_days_after = current_and_forecast_data["daily"][1:6][4][
                    "temp"
                ]["max"]

                min_temperature[city] = {
                    four_days_before: min_temp_four_days_before,
                    three_days_before: min_temp_three_days_before,
                    two_days_before: min_temp_two_days_before,
                    day_before: min_temp_day_before,
                    today: min_temp_today,
                    next_day: min_temp_next_day,
                    two_days_after: min_temp_two_days_after,
                    three_days_after: min_temp_three_days_after,
                    four_days_after: min_temp_four_days_after,
                    five_days_after: min_temp_five_days_after,
                }

                max_temperature[city] = {
                    four_days_before: max_temp_four_days_before,
                    three_days_before: max_temp_three_days_before,
                    two_days_before: max_temp_two_days_before,
                    day_before: max_temp_day_before,
                    today: max_temp_today,
                    next_day: max_temp_next_day,
                    two_days_after: max_temp_two_days_after,
                    three_days_after: max_temp_three_days_after,
                    four_days_after: max_temp_four_days_after,
                    five_days_after: max_temp_five_days_after,
                }

        except requests.exceptions.RequestException as ex:
            print(f"Exception {ex}")

    return min_temperature, max_temperature
