import os

import pandas as pd


def find_day_and_city_with_max_temperature(max_temperature):
    """
    The function looks for the city and day with the maximum temperature for the period under consideration.
    :param max_temperature: dictionary, key: date, value: max temperature
    :param path: path for csv file
    :return:
    """

    df = pd.DataFrame(max_temperature)
    city_with_max_temperature = df.max()[df.max() == df.max(axis=1).max()].index
    data_max_temperature = df.idxmax()[city_with_max_temperature][0]
    city, country = city_with_max_temperature[0][1], city_with_max_temperature[0][0]
    temp = max_temperature[(country, city)][data_max_temperature]
    temp = float("{0:.2f}".format(temp))

    data = [[city, country, data_max_temperature, temp]]
    df = pd.DataFrame(
        data,
        columns=[
            "City with the highest temperature for the specified period",
            "Country",
            "Date",
            "Temperature",
        ],
    )

    return df


def find_city_with_max_difference_in_max_temperature(max_temperature):
    """
    The function looks for the city with the maximum change in maximum temperature.
    :param max_temperature: dictionary, key: date, value: max temperature
    :param path: path for csv file
    :return:
    """

    df = pd.DataFrame(max_temperature)
    max_temp = df.max()
    min_temp = df.min()
    temp_difference = max_temp - min_temp
    city_with_max_difference = temp_difference.idxmax()[1]
    country = temp_difference.idxmax()[0]
    difference = float("{0:.2f}".format(temp_difference.max()))

    data = [[country, city_with_max_difference, difference]]
    df = pd.DataFrame(
        data,
        columns=[
            "Country",
            "The city with the maximum change in maximum temperature",
            "Temperature change",
        ],
    )

    return df


def find_day_and_city_with_min_temperature(min_temperature):
    """
    The function looks for the city and day with the minimum temperature for the period under consideration.
    :param max_temperature: dictionary, key: date, value: min temperature
    :param path: path for csv file
    :return:
    """

    df = pd.DataFrame(min_temperature)
    city_with_min_temperature = df.min()[df.min() == df.min(axis=1).min()].index
    data_min_temperature = df.idxmin()[city_with_min_temperature][0]
    city, country = city_with_min_temperature[0][1], city_with_min_temperature[0][0]
    min_temp = min_temperature[(country, city)][data_min_temperature]
    min_temp = float("{0:.2f}".format(min_temp))

    data = [[country, city, data_min_temperature, min_temp]]
    df = pd.DataFrame(
        data,
        columns=[
            "Country",
            "City with the lowest temperature for the specified period",
            "Data",
            "Temperature",
        ],
        index=None,
    )

    return df


def find_day_and_city_with_max_difference_in_temperature(
    max_temperature, min_temperature
):
    """
    The function looks for the city and day with the maximum difference between the maximum and minimum temperatures.
    :param max_temperature: dictionary, key: date, value: max temperature
    :param min_temperature: dictionary, key: date, value: min temperature
    :param path: path for csv file
    :return:
    """

    df_max_temp = pd.DataFrame(max_temperature)
    df_min_temp = pd.DataFrame(min_temperature)
    df_difference = df_max_temp - df_min_temp
    city_with_max_difference = df_difference.max()[
        df_difference.max() == df_difference.max(axis=1).max()
    ].index
    data_max_difference_temp = df_difference.idxmax()[city_with_max_difference][0]

    city, country = city_with_max_difference[0][1], city_with_max_difference[0][0]
    difference = (
        max_temperature[(country, city)][data_max_difference_temp]
        - min_temperature[(country, city)][data_max_difference_temp]
    )
    difference = float("{0:.2f}".format(difference))

    data = [[country, city, data_max_difference_temp, difference]]
    df = pd.DataFrame(
        data,
        columns=[
            "Country",
            "City with maximum difference between maximum and minimum temperature",
            "Date",
            "Temperature difference",
        ],
        index=None,
    )

    return df


def post_processing(max_temperature, min_temperature, path):

    path_to_output = os.path.join(path, "post_processing")
    os.makedirs(f"{path_to_output}", exist_ok=True)

    # Looking for the city and the day of observation with the maximum temperature for the period under consideration.
    df1 = find_day_and_city_with_max_temperature(max_temperature)
    path_to_output_file = os.path.join(
        path_to_output, "day_and_city_with_max_temperature.csv"
    )
    df1.to_csv(path_to_output_file, index=False, sep="\t", encoding="utf-8")

    # Looking for a city with the maximum change in maximum temperature.
    df2 = find_city_with_max_difference_in_max_temperature(max_temperature)
    path_to_output_file = os.path.join(
        path_to_output, "city_with_max_difference_in_max_temperature.csv"
    )
    df2.to_csv(path_to_output_file, index=False, sep="\t", encoding="utf-8")

    # Looking for the city and the day of observation with the minimum temperature for the period under consideration.
    df3 = find_day_and_city_with_min_temperature(min_temperature)
    path_to_output_file = os.path.join(
        path_to_output, "day_and_city_with_min_temperature.csv"
    )
    df3.to_csv(path_to_output_file, index=False, sep="\t", encoding="utf-8")

    # Looking for a city and a day with a maximum difference between the maximum and minimum temperatures.
    df4 = find_day_and_city_with_max_difference_in_temperature(
        max_temperature, min_temperature
    )
    path_to_output_file = os.path.join(
        path_to_output, "day_and_city_with_max_difference_in_temperature.csv"
    )
    df4.to_csv(path_to_output_file, index=False, sep="\t", encoding="utf-8")
