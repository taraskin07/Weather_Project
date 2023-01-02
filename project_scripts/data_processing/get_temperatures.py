import time
from datetime import datetime, timedelta

import requests


def day(day_num):

    """
    This class is used to convert the time data into an appropriate format for One Call API(openweathermap.org/).

    :param day_num: int or str(with number) corresponding to date
    :return date: date in format for One Call API(openweathermap.org/) - (Unix time, UTC time zone)

    Example of usage:
    day(0) ==> return today's date (UTC time zone)
    day(-1) ==> return yesterday's date (UTC time zone)
    day(1) ==> return tomorrow's date (UTC time zone)
    """

    # Determine the date in the desired format.
    utc_day = datetime.utcnow().date() + timedelta(days=day_num)
    tuple_obj = utc_day.timetuple()

    # Convert the time to the One Call API (openweathermap.org/) required format - (Unix time, UTC time zone).
    utc_unix_time = int(time.mktime(tuple_obj))

    return utc_unix_time


def weather_historical_data_up_to_5_days(api_url, params, days_amount):

    """
    The function gets the historical weather data for coordinates given.
    API used: https://openweathermap.org/api/one-call-api

    :param api_url: One Call Api url
    :param params: 'get' method parameters for the request
    :param days_amount: amount of +/- days (relative to today) for which weather data should be obtained (default = 5)
    :return current_and_forecast_data: JSON response
    """

    # Making a GET request to api_url and getting JSON data.
    try:
        days_amount = int(days_amount)
        data_json = []
        if 2 <= days_amount <= 5:

            for i in range(days_amount):
                response = requests.get(
                    f"{api_url}/timemachine", params={**params, **{"dt": day(-i)}}
                )
                response = response.json()
                data_json.append(response)
            return data_json

        else:
            print(f"Days value must be in range from 1 to 5 days!")
    except ValueError:
        print(f"Days value must be integer from 1 to 5.")


def weather_data(lat, lon, app_id, days_amount):
    """
    The function gets the weather for city centers with the maximum number of hotels (according to the task):
        - for the previous 5 days;
        - forecast: for the next 5 days;
        - current values;
    API used: https://openweathermap.org/api/one-call-api

    :param lat: latitude
    :param lon: longtitude
    :param app_id: API-key from https://api.openweathermap.org/
    :param days_amount: amount of +/- days (relative to today) for which weather data should be obtained (default = 5)
    :return historical_data, current_and_forecast_data: tuple of dictionaries
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
            historical_data = weather_historical_data_up_to_5_days(
                api_url, params, days_amount
            )

            return historical_data, current_and_forecast_data

    except requests.exceptions.RequestException as ex:
        print(f"Exception {ex}")


def get_temperature(
    dict_city_lat_long, app_id="bb92d313e962c39150e26b5318be6a87", days_amount=5
):
    """
    The function gets the weather for city centers with the maximum number of hotels (according to the task).
    Moreover, minimum and maximum temperature daily values.
    - for the previous 5 days;
    - forecast: for the next 5 days;
    - current values;
    API used: https://api.openweathermap.org/
    :param dict_city-lat_long: dictionary with cities and their coordinates
    :param days_amount: amount of +/- days (relative to today) for which weather data should be obtained (default = 5)
    :param app_id: API-key from https://api.openweathermap.org/
    :return min_temperature, max_temperature: dictionaries with minimum and maximum daily temperature for every city today +/- 5 days
    """

    # Output are two dictionaries, containing information about minimum and maximum temperature daily values for each 'Allocation' inspected.
    min_temperature = dict()
    max_temperature = dict()

    for city, lat_long in dict_city_lat_long.items():
        lat = lat_long[0]
        lon = lat_long[1]
        # Calling weather_data(lat, lon, app_id, days_amount) function to get the weather for city coordinates.
        historical_data, current_and_forecast = weather_data(
            lat, lon, app_id, days_amount
        )

        # Creating dictionaries inside the resulting ones for each city of interest.
        min_temperature[city] = dict()
        max_temperature[city] = dict()

        # Finding historical min and max daily temperature values.
        for days_before in historical_data[::-1]:
            date_utc = datetime.utcfromtimestamp(days_before["current"]["dt"]).strftime(
                "%Y-%m-%d"
            )
            min_temp = min([t["temp"] for t in days_before["hourly"]])
            max_temp = max([t["temp"] for t in days_before["hourly"]])

            # Adding values to dictionary.
            min_temperature[city][date_utc] = min_temp
            max_temperature[city][date_utc] = max_temp

        # Finding current and forecast min and max daily temperature values.
        for days_ahead in range(days_amount + 1):
            date_utc = datetime.utcfromtimestamp(
                current_and_forecast["daily"][days_ahead]["dt"]
            ).strftime("%Y-%m-%d")
            max_temp = current_and_forecast["daily"][days_ahead]["temp"]["max"]
            min_temp = current_and_forecast["daily"][days_ahead]["temp"]["min"]

            # Adding values to the dictionaries.
            min_temperature[city][date_utc] = min_temp
            max_temperature[city][date_utc] = max_temp

    return min_temperature, max_temperature
