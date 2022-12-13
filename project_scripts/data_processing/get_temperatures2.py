import time
from datetime import date, datetime, timedelta
import requests

# Определяем дату в нужном формате, предыдущий день
days_before_1dt = date.today() - timedelta(days=1)
print(f'days_before_1dt  {days_before_1dt}')
# Конвертируем время в формат, нужный при обращении к One Call API(openweathermap.org/), (Unix time, UTC time zone)
days_before_1 = int(time.mktime(days_before_1dt.timetuple()))
print(f'days_before_1 {days_before_1}')

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
    day = date.today() + timedelta(days=day_num)
    print(f'day  {day}')
    print(f'today {date.today()}')

    tuple_obj = day.timetuple()
    print(f'tuple_obj  {tuple_obj}')
    time_val = int(time.mktime(tuple_obj))

    print(f'time_val  {time_val}')

    return time_val

day(-1)

def get_temperature(dict_city_lat_long, app_id):
    """
    The function gets the weather for city centers with the maximum number of hotels (according to the task):
    - for the previous 5 days, including the current one;
    - forecast: for the next 5 days;
    - current values;
    API used: https://openweathermap.org/api/one-call-api
    :param dict_city-lat_long: dictionary with cities and their coordinates
    :param app_id: API-key from https://api.openweathermap.org/
    :return min_temperature, max_temperature:
    """

    # As a result it is supposed to be the dictionary {(Country, City): {date:temperature}}
    min_temperature = dict()
    max_temperature = dict()

    # Initial information is taken from dict with cities and coordinates.
    for city, lat_long in dict_city_lat_long.items():
        lat = lat_long[0]
        lon = lat_long[1]


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
            current_and_forecast_weather = requests.get(api_url3, params=params)
            current_and_forecast_data = current_and_forecast_weather.json()
            print(current_and_forecast_data)

    except requests.exceptions.RequestException as ex:
        print(f"Exception {ex}")


dict_city_lat_long = {("AT", "Vienna"): [48.203066462500004, 16.368756425]}
app_id = "bb92d313e962c39150e26b5318be6a87"
get_temperature(dict_city_lat_long, app_id)


























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