import glob as g
import zipfile as z

import pandas as pd


def unzip(path):
    """
    Функция распаковывет zip файл в директорию unpacked_files
    :param path: путь до zip файла
    """
    with z.ZipFile(path, "r") as myzip:
        myzip.extractall("unpacked_files")


def func_to_create_dataframe_from_csv(folder):
    """
    Функция создает объект dataframe из распакованных csv файлов
    :param folder: папка с csv файлами
    :return dataframe: полученный dataframe
    """
    dataframe = pd.concat(
        [pd.read_csv(f, sep=",", encoding="utf-8") for f in g.glob(folder + "/*.csv")],
        ignore_index=True,
    )
    return dataframe


def cleaning_dataframe(frame):
    """
    Функция очищает данные от невалидных записей
    (содержащих заведомо ложные значения или отсутствующие необходимые элементы)
    :param frame: полученный dataframe
    :return clean_frame: исправленный dataframe
    """
    frame = frame.dropna(axis=0, how="any")
    index_list_to_drop_in_dataframe = []
    for index, value in frame.iterrows():
        try:
            latitude = float(value["Latitude"])
            longitude = float(value["Longitude"])
            if abs(latitude) > 180 or abs(longitude) > 180:
                index_list_to_drop_in_dataframe.append(index)
        except ValueError:
            index_list_to_drop_in_dataframe.append(index)

    clean_frame = frame.drop(index_list_to_drop_in_dataframe)
    clean_frame.reset_index(drop=True, inplace=True)
    return clean_frame


if __name__ == "__main__":
    unzip("hotels.zip")
    f = func_to_create_dataframe_from_csv("unpacked_files")
    cl_f = cleaning_dataframe(f)
    res = pd.concat([f, cl_f]).drop_duplicates(keep=False)
    print(res["Latitude"], res["Longitude"])
