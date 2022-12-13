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
    day = date.today() + timedelta(days=day_num)
    # print(f'day  {day}')
    # print(f'today {date.today()}')

    tuple_obj = day.timetuple()
    # print(f'tuple_obj  {tuple_obj}')
    time_val = int(time.mktime(tuple_obj))

    # print(f'time_val  {time_val}')

    return time_val




def weather_historical_data_up_to_5_days(api_url, params, days):
    """
    The function gets the historical weather data for coordinates given.
    API used: https://openweathermap.org/api/one-call-api
    :param dict_city-lat_long: dictionary with cities and their coordinates
    :param app_id: API-key from https://api.openweathermap.org/
    :return current_and_forecast_data: json response
    """
    try:
        days = int(days)
        if 1 <= days <= 5:
            data_json=[]
            for i in range(days):
                response = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": day(-i)}}
                )

                response = response.json()
                d = response.strftime("%Y-%m-%d")
                print(f"Day {i} stands for {d}")

                data_json.append(response)
                return data_json
        else:
            print(f"Days value must be in range from 1 to 5 days!")
    except ValueError:
        print(f'Days value must be integer from 1 to 5.')


def current_and_forecast_weather(dict_city_lat_long, app_id):
    """
    The function gets the weather for city centers with the maximum number of hotels (according to the task):
    - forecast: for the next 5 days;
    - current values;
    API used: https://openweathermap.org/api/one-call-api
    :param dict_city-lat_long: dictionary with cities and their coordinates
    :param app_id: API-key from https://api.openweathermap.org/
    :return current_and_forecast_data: json response
    """

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
            current_and_forecast_weather = requests.get(api_url, params=params)
            current_and_forecast_data = current_and_forecast_weather.json()
            print(current_and_forecast_data)
            return current_and_forecast_data

    except requests.exceptions.RequestException as ex:
        print(f"Exception {ex}")


dict_city_lat_long = {("AT", "Vienna"): [48.203066462500004, 16.368756425]}
app_id = "bb92d313e962c39150e26b5318be6a87"
# get_temperature(dict_city_lat_long, app_id)




# def get_temperature(dict_city_lat_long, app_id):
#     """
#     The function gets the weather for city centers with the maximum number of hotels (according to the task):
#     - for the previous 5 days, including the current one;
#     - forecast: for the next 5 days;
#     - current values;
#     API used: https://openweathermap.org/api/one-call-api
#     :param dict_city-lat_long: dictionary with cities and their coordinates
#     :param app_id: API-key from https://api.openweathermap.org/
#     :return min_temperature, max_temperature:
#     """

    # # As a result it is supposed to be the dictionary {(Country, City): {date:temperature}}
    # min_temperature = dict()
    # max_temperature = dict()


if __name__=='__main__':
    api_url = "https://api.openweathermap.org/data/2.5/onecall"

    for city, lat_long in dict_city_lat_long.items():
        lat = lat_long[0]
        lon = lat_long[1]


    app_id = "bb92d313e962c39150e26b5318be6a87"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": app_id,
        "units": "metric",
        "exclude": "minutely, alerts",
    }
    days = 5



    dict_city_lat_long = {("AT", "Vienna"): [48.203066462500004, 16.368756425]}


    ret = weather_historical_data_up_to_5_days(api_url, params, days)
    print(f"Historical data: \n{ret}")

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

# Значения температуры для предыдущих дней
    previous_1_day = requests.get(f"{api_url}/timemachine", params={**params, **{"dt": days_before_1}})
    data_1_day_before = previous_1_day.json()
    print(f'Day1 stands for {data_1_day_before.strftime("%Y-%m-%d")}')

    previous_2_days = requests.get(f"{api_url}/timemachine", params={**params, **{"dt": days_before_2}})
    data_2_days_before = previous_2_days.json()
    print(f'Day2 stands for {data_2_days_before.strftime("%Y-%m-%d")}')
    previous_3_days = requests.get(f"{api_url}/timemachine", params={**params, **{"dt": days_before_3}})
    data_3_days_before = previous_3_days.json()
    print(f'Day3 stands for {data_3_days_before.strftime("%Y-%m-%d")}')
    previous_4_days = requests.get(f"{api_url}/timemachine", params={**params, **{"dt": days_before_4}})
    data_4_days_before = previous_4_days.json()
    print(f'Day4 stands for {data_4_days_before.strftime("%Y-%m-%d")}')

    new_list =[]
    new_list.append(data_1_day_before)
    new_list.append(data_2_days_before)
    new_list.append(data_3_days_before)
    new_list.append(data_4_days_before)

    tr= new_list
    print(new_list)















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