import pandas as pd
import os


def find_day_and_city_with_max_temperature(max_temperature):
    """
    Функция ищет город и день наблюдения с максимальной температурой за рассматриваемый период.
    :param max_temperature: словарь key: дата, value: максимальная температура
    :param path: путь для сохранения csv файла
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
            "Город с максимальной температурой за рассматриваемый период",
            "Страна",
            "Дата",
            "Температура",
        ],
    )

    return df


def find_city_with_max_difference_in_max_temperature(max_temperature):
    """
    Функция ищет город с максимальным изменением максимальной температуры.
    :param max_temperature:  словарь key: дата, value: максимальная температура
    :param path: путь для сохранения csv файла
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
            "Страна",
            "Город с максимальным изменением максимальной температуры",
            "Изменение температуры",
        ],
    )

    return df


def find_day_and_city_with_min_temperature(min_temperature):
    """
    Функция ищет город и день наблюдения с минимальной температурой за рассматриваемый период.
    :param min_temperature: словарь key: дата, value: минимальная температура
    :param path: путь для сохранения csv файла
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
            "Страна",
            "Название города с минимальной температурой за рассматриваемый период",
            "Дата",
            "Температура",
        ],
        index=None,
    )

    return df


def find_day_and_city_with_max_difference_in_temperature(
    max_temperature, min_temperature
):
    """
    Функция ищет город и день с максимальной разницей между максимальной и минимальной температурой.
    :param max_temperature: словарь key: дата, value: максимальная температура
    :param min_temperature: словарь key: дата, value: минимальная температура
    :param path: путь для сохранения csv файла
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
            "Страна",
            "Название города с максимальной разницей между максимальной и минимальной температурой",
            "Дата",
            "Разница температур",
        ],
        index=None,
    )

    return df


def post_processing(max_temperature, min_temperature, path):
    path_to_output = os.path.join(path, "post_processing")
    os.makedirs(f"{path_to_output}", exist_ok=True)

    # Ищем город и день наблюдения с максимальной температурой за рассматриваемый период.
    df1 = find_day_and_city_with_max_temperature(max_temperature)
    path_to_output_file = os.path.join(
        path_to_output, "day_and_city_with_max_temperature.csv"
    )
    df1.to_csv(path_to_output_file, index=False, sep="\t", encoding="utf-8")

    # Ищем город с максимальным изменением максимальной температуры.
    df2 = find_city_with_max_difference_in_max_temperature(max_temperature)
    path_to_output_file = os.path.join(
        path_to_output, "city_with_max_difference_in_max_temperature.csv"
    )
    df2.to_csv(path_to_output_file, index=False, sep="\t", encoding="utf-8")

    # Ищем город и день наблюдения с минимальной температурой за рассматриваемый период.
    df3 = find_day_and_city_with_min_temperature(min_temperature)
    path_to_output_file = os.path.join(
        path_to_output, "day_and_city_with_min_temperature.csv"
    )
    df3.to_csv(path_to_output_file, index=False, sep="\t", encoding="utf-8")

    # Ищем город и день с максимальной разницей между максимальной и минимальной температурой.
    df4 = find_day_and_city_with_max_difference_in_temperature(
        max_temperature, min_temperature
    )
    path_to_output_file = os.path.join(
        path_to_output, "day_and_city_with_max_difference_in_temperature.csv"
    )
    df4.to_csv(path_to_output_file, index=False, sep="\t", encoding="utf-8")
