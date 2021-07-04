import os
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pandas as pd
from geopy import OpenMapQuest
from geopy.extra.rate_limiter import RateLimiter


def geopy_address(coordinates_list, workers_amount, api_key):
    """
    Функция для получения адреса по координатам. Позволяет задать количество потоков.
    :param workers_amount: количество потоков для параллельной обработки данных
    :param coordinates_list: список с координатами
    :param api_key: API ключ сайта https://developer.mapquest.com/
    :return df: dataframe с адресом и координатами
    """
    geolocator = OpenMapQuest(api_key=api_key)

    # Устанавливаем задержку в секундах, чтобы избежать Too Many Requests 429 error
    delay = 1 / 20
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=delay)

    with ThreadPoolExecutor(max_workers=workers_amount) as th:
        locations = dict(th.map(geocode, coordinates_list))
    # Словарь с координатами и адресом преобразуем в DataFrame
    df = pd.DataFrame(
        locations.values(), index=locations.keys(), columns=["Latitude", "Longitude"]
    )
    df["Address"] = df.index
    df = df.reset_index(drop=True)
    return df


def create_csv_file_with_addresses(df1, df2, path):
    """
    Функция для объединения dataframe с городами с большим числом отелей и dataframe с адресами этих отелей.
    Столбцы (Name, Address, Latitude, Longitude).
    Данные по каждой стране и городу в csv файле представлены отдельно.
    :param path: путь к директории для сохранения полученных файлов
    :param df1: dataframe с городами с большим числом отелей в стране
    :param df2: dataframe с адресами
    :return:
    """
    # Объединяем два dataframe в один добавляя столбцы в конечную таблицу.
    # Часть значений при этом является NaN.
    df = df1.combine_first(df2)

    # Убираем строки с пустыми значениями.
    df = df.dropna(axis=0)
    unique_country_city = df["New_column"].unique()

    # Чтобы сделать папку страна/город, берем информацию из New_colomn где значения - кортеж (страна, город)
    for names in unique_country_city:
        country, city = names
        output_folder_path = f"{path}/{country}/{city}"
        data_proc = df.loc[df["New_column"] == names]
        data_proc.reset_index(drop=True, inplace=True)
        del data_proc["New_column"]
        del data_proc["City"]
        del data_proc["Country"]
        save_df_in_csv_less_than_100_notes(data_proc, output_folder_path)


def save_df_in_csv_less_than_100_notes(df, path):
    """
    Функция для сохранения в csv файлы, не более 100 записей в каждом.
    :param df: dataframe
    :param path: путь, куда будет сохранен полученный csv файл
    :return:
    """
    number_of_splits = int((len(df) / 100)) + 1
    os.makedirs(f"{path}", exist_ok=True)
    chunks = np.array_split(df, number_of_splits)
    for number, chunk in enumerate(chunks):
        chunk.to_csv(
            f"{path}/address_latitude_longitude__hotels_{number}.csv",
            sep="\t",
            encoding="utf-8",
        )
