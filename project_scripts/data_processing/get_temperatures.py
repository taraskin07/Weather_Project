import json
import time
from datetime import date, datetime, timedelta

import requests


def get_temperature(dict_city_lat_long, app_id):
    """
    The function gets the weather for city centers with the maximum number of hotels (according to the task):
    - for the previous 5 days, including the current one;
    - forecast: for the next 5 days;
    - current values;
    API used: https://api.openweathermap.org/
    :param dict_city-lat_long: dictionary with cities and their coordinates
    :param app_id: API-key from https://api.openweathermap.org/
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


if __name__=='__main__':
    import os.path as p

    import pandas as pd

    import project_scripts.data_assessment.cities_with_max_hotels as cwmh

    cities_with_max_amount_of_hotel = cwmh.cities_with_max_amount_of_hotel

    import project_scripts.data_assessment.preparing_data as prdat

    cleaning_dataframe = prdat.cleaning_dataframe
    unzip = prdat.unzip
    import project_scripts.data_processing.getting_coordinates as gsc

    center_coordinates = gsc.center_coordinates
    get_coordinates_list = gsc.get_coordinates_list

    path = p.join("../../tests", "test_1_city.zip")
    name_of_folder = p.join("tests", "test_unpacked_files")
    unzip(path, name_of_folder)
    file_path = p.join(name_of_folder, "test_1_city.csv")
    f = pd.read_csv(file_path, sep=",", encoding="utf-8")
    cl_f = cleaning_dataframe(f)
    df = cities_with_max_amount_of_hotel(cl_f)

    lat_vienna = float("{0:.2f}".format(center_coordinates(df)[("AT", "Vienna")][0]))
    lon_vienna = float("{0:.2f}".format(center_coordinates(df)[("AT", "Vienna")][1]))
    # assert lat_vienna == 48.2
    # assert lon_vienna == 16.37
    print(f'Lat Viena: {lat_vienna}')
    print(f'Lon Viena: {lon_vienna}')

    print(f'Coordinates list: {get_coordinates_list(df)}')

    # assert isinstance(get_coordinates_list(df), list)
    # assert get_coordinates_list(df) == [
    #     "48.2058584, 16.3766545",
    #     "48.1954348, 16.383429",
    #     "48.1965878, 16.3413729",
    #     "48.2163149, 16.3685103",
    #     "48.2062103, 16.3710387",
    #     "48.2002872, 16.3547746",
    #     "48.1955998, 16.3826989",
    #     "48.2082385, 16.3715725",
    # ]

    dict_city_lat_long = {("AT", "Vienna"): [48.203066462500004, 16.368756425]}
    app_id = "bb92d313e962c39150e26b5318be6a87"
    min, max = get_temperature(dict_city_lat_long, app_id)

    print (f'\nMin : \n{min}\n')

    print (f'\nMax : \n{max}')

    Min_d={('AT', 'Vienna'): {'2022-12-09': 1.44, '2022-12-10': 2.8, '2022-12-11': 2.5, '2022-12-12': -0.68,
                        '2022-12-13': -4.6, '2022-12-14': -2.27, '2022-12-15': -0.15, '2022-12-16': -0.94,
                        '2022-12-17': -2.08, '2022-12-18': -4.19}}

    Max_d={('AT', 'Vienna'): {'2022-12-09': 5.25, '2022-12-10': 5, '2022-12-11': 3.9, '2022-12-12': 2.63, '2022-12-13': 0.79,
                        '2022-12-14': 0.86, '2022-12-15': 2.51, '2022-12-16': 0.7, '2022-12-17': 0.79,
                        '2022-12-18': -0.07}}
    