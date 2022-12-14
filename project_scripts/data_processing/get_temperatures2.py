import time
from datetime import date, datetime, timedelta
import requests

# # Определяем дату в нужном формате, предыдущий день
# days_before_1dt = date.today() - timedelta(days=1)
# print(f'days_before_1dt  {days_before_1dt}')
# # Конвертируем время в формат, нужный при обращении к One Call API(openweathermap.org/), (Unix time, UTC time zone)
# days_before_1 = int(time.mktime(days_before_1dt.timetuple()))
# print(f'days_before_1 {days_before_1}')

def day(day_num):
    """
    This class is used to convert the time data into appropriate format for One Call API(openweathermap.org/).
    :param day_num: int or str(with number) corresponding to date
    :return date: date in format for One Call API(openweathermap.org/).
    Example of usage:
    day(0) ==> return today's date
    day(-1) ==> return yesterday's date
    day(1) ==> return tomorrow's date
    """


    # Determine the date in the desired format.
    day = date.today() + timedelta(days=day_num)
    tuple_obj = day.timetuple()

    # Convert the time to the One Call API (openweathermap.org/) required format - (Unix time, UTC time zone).
    unix_time = int(time.mktime(tuple_obj))

    return unix_time




def weather_historical_data_up_to_5_days(api_url, params, days_amount):
    """
    The function gets the historical weather data for coordinates given.
    API used: https://openweathermap.org/api/one-call-api
    :param dict_city-lat_long: dictionary with cities and their coordinates
    :param app_id: API-key from https://api.openweathermap.org/
    :return current_and_forecast_data: json response
    """
    try:
        days_amount = int(days_amount)
        data_json = []
        if 2 <= days_amount <= 5:

            for i in range(1, days_amount):
                response = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": day(-i)}}
                )
                # d = response.strftime("%Y-%m-%d")
                response = response.json()

                # print(f"Day {i} stands for {d}")

                data_json.append(response)
            return data_json

        elif days_amount == 1:
            response = requests.get(
                f"{api_url}/timemachine", params={**params, **{"dt": day(-days_amount)}}
            )
            response = response.json()
            data_json.append(response)
            return data_json

        else:
            print(f"Days value must be in range from 1 to 5 days!")
    except ValueError:
        print(f'Days value must be integer from 1 to 5.')


def weather_data(lat, lon, app_id, days_amount):
    """
    The function gets the weather for city centers with the maximum number of hotels (according to the task):
    - forecast: for the next 5 days;
    - current values;
    API used: https://openweathermap.org/api/one-call-api
    :param dict_city-lat_long: dictionary with cities and their coordinates
    :param app_id: API-key from https://api.openweathermap.org/
    :return current_and_forecast_data: json response
    """


    # Base url for One Call API
    api_url = "https://api.openweathermap.org/data/2.5/onecall"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": app_id,
        "units": "metric",
        "exclude": "minutely, alerts",
    }


    try:
        if requests.get(api_url, params=params):
            # Temperature values for the current day and forecast for 5 days
            current_and_forecast_weather = requests.get(api_url, params=params)
            current_and_forecast_data = current_and_forecast_weather.json()

            # Historical temperature values for the last 5 days
            historical_data = weather_historical_data_up_to_5_days(api_url, params, days_amount)

            return historical_data, current_and_forecast_data

    except requests.exceptions.RequestException as ex:
        print(f"Exception {ex}")



if __name__=='__main__':
    dict_city_lat_long = {("AT", "Vienna"): [48.203066462500004, 16.368756425]}
    app_id = "bb92d313e962c39150e26b5318be6a87"


    def get_temperature(dict_city_lat_long, days_amount=5, app_id="bb92d313e962c39150e26b5318be6a87"):
        """
        The function gets the weather for city centers with the maximum number of hotels (according to the task):
        - for the previous 5 days, including the current one;
        - forecast: for the next 5 days;
        - current values;
        API used: https://api.openweathermap.org/
        :param dict_city-lat_long: dictionary with cities and their coordinates
        :param days_amount: amount of days before, since historical weather data should be obtained (default = 5)
        :param app_id: API-key from https://api.openweathermap.org/
        :return min_temperature, max_temperature:
        """


        for city, lat_long in dict_city_lat_long.items():
            lat = lat_long[0]
            lon = lat_long[1]

            historical_data, current_and_forecast = weather_data(lat, lon, app_id, days_amount)
            print(f'History: {historical_data}')
            print(f'Forecast: {current_and_forecast}')

    get_temperature(dict_city_lat_long)








# class Day:
#     """
#     This class is used to convert the time data into appropriate format for One Call API(openweathermap.org/).
#     Example of usage:
#     Day(0) ==> return today's date
#     Day(-1) ==> return yesterday's date
#     Day(1) ==> return tomorrow's date
#     """
#     # def __init__(self, day):
#     #     self.day=date.today()
#
#     def reg_date(self, day):
#         self.day = day
#         day = date.today() - timedelta(days=day)
#         return day
#
#
#
# print(f"day  {Day.reg_date()}")