import time
from datetime import date, datetime, timedelta

import requests


def get_temperature(dict_city_lat_long, app_id="G8uzA4xdsG5B0uLcekeCowprs41bkZlb"):
    """
    Функция получает для центров городов с максимальным количеством отелей(по заданию) погоду:
        - за предыдущие 5 дней;
    - прогноз: на последующие 5 дней;
    - текущие значения;
     через API сайта https://api.openweathermap.org/
    :param dict_city-lat_long: словарь с городами и их координатами
    :param api_key: API ключ сайта https://api.openweathermap.org/
    :return min_temperature, max_temperature:
    """
    days_before = date.today() - timedelta(1)
    days_before_1 = int(time.mktime(days_before.timetuple()))

    days_before = date.today() - timedelta(days=2)
    days_before_2 = int(time.mktime(days_before.timetuple()))

    days_before = date.today() - timedelta(days=3)
    days_before_3 = int(time.mktime(days_before.timetuple()))

    days_before = date.today() - timedelta(days=4)
    days_before_4 = int(time.mktime(days_before.timetuple()))

    days_before = date.today() - timedelta(days=5)
    days_before_5 = int(time.mktime(days_before.timetuple()))

    min_temperature = dict()
    max_temperature = dict()

    api_url = "https://api.openweathermap.org/data/2.5/onecall"

    for city, lat_long in dict_city_lat_long.items():
        lat = lat_long[0]
        lon = lat_long[1]

        params = {"lat": lat, "lon": lon, "appid": app_id, "units": "metric"}

        try:
            if requests.get(api_url, params=params):
                current_and_forecast_weather = requests.get(api_url, params=params)
                previous_1_day = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_1}}
                )
                previous_2_days = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_2}}
                )
                previous_3_days = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_3}}
                )
                previous_4_days = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_4}}
                )
                previous_5_days = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": days_before_5}}
                )

                current_and_forecast_data = current_and_forecast_weather.json()
                data_1_day_before = previous_1_day.json()
                data_2_days_before = previous_2_days.json()
                data_3_days_before = previous_3_days.json()
                data_4_days_before = previous_4_days.json()
                data_5_days_before = previous_5_days.json()

                min_temperature[city] = {
                    date.today().strftime("%Y-%m-%d"): current_and_forecast_data[
                        "daily"
                    ][0]["temp"]["min"],
                    days_before_1.strftime("%Y-%m-%d"): min(
                        [i["temp"] for i in data_1_day_before["hourly"]]
                    ),
                    days_before_2.strftime("%Y-%m-%d"): min(
                        [i["temp"] for i in data_2_days_before["hourly"]]
                    ),
                    days_before_3.strftime("%Y-%m-%d"): min(
                        [i["temp"] for i in data_3_days_before["hourly"]]
                    ),
                    days_before_4.strftime("%Y-%m-%d"): min(
                        [i["temp"] for i in data_4_days_before["hourly"]]
                    ),
                    days_before_5.strftime("%Y-%m-%d"): min(
                        [i["temp"] for i in data_5_days_before["hourly"]]
                    ),
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][0]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][0][
                        "temp"
                    ][
                        "min"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][1]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][1][
                        "temp"
                    ][
                        "min"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][2]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][2][
                        "temp"
                    ][
                        "min"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][3]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][3][
                        "temp"
                    ][
                        "min"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][4]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][4][
                        "temp"
                    ][
                        "min"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][4]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][5][
                        "temp"
                    ][
                        "min"
                    ],
                }

                max_temperature[city] = {
                    date.today().strftime("%Y-%m-%d"): current_and_forecast_data[
                        "daily"
                    ][0]["temp"]["max"],
                    days_before_1.strftime("%Y-%m-%d"): max(
                        [i["temp"] for i in data_1_day_before["hourly"]]
                    ),
                    days_before_2.strftime("%Y-%m-%d"): max(
                        [i["temp"] for i in data_2_days_before["hourly"]]
                    ),
                    days_before_3.strftime("%Y-%m-%d"): max(
                        [i["temp"] for i in data_3_days_before["hourly"]]
                    ),
                    days_before_4.strftime("%Y-%m-%d"): max(
                        [i["temp"] for i in data_4_days_before["hourly"]]
                    ),
                    days_before_5.strftime("%Y-%m-%d"): max(
                        [i["temp"] for i in data_5_days_before["hourly"]]
                    ),
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][0]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][0][
                        "temp"
                    ][
                        "max"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][1]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][1][
                        "temp"
                    ][
                        "max"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][2]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][2][
                        "temp"
                    ][
                        "max"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][3]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][3][
                        "temp"
                    ][
                        "max"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][4]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][4][
                        "temp"
                    ][
                        "max"
                    ],
                    datetime.utcfromtimestamp(
                        current_and_forecast_data["daily"][1:6][4]["dt"]
                    ).strftime("%Y-%m-%d"): current_and_forecast_data["daily"][1:6][5][
                        "temp"
                    ][
                        "max"
                    ],
                }
        except requests.exceptions.RequestException as ex:
            print(f"Error {ex}")

    return min_temperature, max_temperature
