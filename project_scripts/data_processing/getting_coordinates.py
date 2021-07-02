import pandas as pd


def center_coordinates(df):
    """
    Функция находит центры координат для каждого города с максимальным количеством отелей
    :param df: dataframe с городами в которых больше всего отелей в стране
    :return: словарь, где каждому городу соответствует его геометрический центр
    """
    # Превращаем координаты в числа
    df = df.astype({"Latitude": float})
    df = df.astype({"Longitude": float})
    # df.to_csv('before.csv', sep='\t', encoding='utf-8')

    # Приводим для каждого города средние значения по каждой координате
    df = df.groupby(["City"], as_index=False).agg(
        {"Latitude": "mean", "Longitude": "mean"}
    )
    # df.to_csv('after.csv', sep='\t', encoding='utf-8')

    # Формируем словарь, где каждому городу соответствует его геометрический центр
    new_dict = df.set_index("City").T.to_dict("list")
    return new_dict


def get_coordinates_list(df):
    """
    Функция преобразует dataframe в список строк с координатами Latitude, Longitude
    :param df: dataframe с городами в которых больше всего отелей в стране
    :return list: список с координатами в виде: ['Latitude, Longitude']
    """
    df = df[["Latitude", "Longitude"]]
    df = df.astype({"Latitude": str})
    df = df.astype({"Longitude": str})
    # Делаем новый столбец, объединив столбцы ширины и долготы(их значения) через запятую
    df["Coordinates"] = [
        (x + ", " + y) for x, y in zip(df.Latitude.values, df.Longitude.values)
    ]
    # Формируем список с координатами через запятую
    coordinates_list = df["Coordinates"].tolist()
    return coordinates_list


if __name__ == "__main__":
    from cities_with_max_hotels import cities_with_max_amount_of_hotel
    from preparing_data import (
        cleaning_dataframe,
        func_to_create_dataframe_from_csv,
        unzip,
    )

    unzip("hotels.zip")
    f = func_to_create_dataframe_from_csv("unpacked_files")
    cl_f = cleaning_dataframe(f)
    # res = pd.concat([f, cl_f]).drop_duplicates(keep=False)
    csvvvv = cities_with_max_amount_of_hotel(cl_f)
    # print(type(csvvvv))
    # csvvvv.to_csv('csvvvv.csv', sep='\t', encoding='utf-8')

    print(center_coordinates(csvvvv))
    print(get_list_with_coordinates(csvvvv))
