def center_coordinates(df):
    """
    Функция находит центры координат для каждого города с максимальным количеством отелей
    :param df: dataframe с городами в которых больше всего отелей в стране
    :return: словарь, где каждому городу соответствует его геометрический центр
    """
    # Превращаем координаты в числа
    df = df.astype({"Latitude": float})
    df = df.astype({"Longitude": float})

    # Приводим для каждого места: New_column - (страна, город) средние значения по каждой координате
    df = df.groupby(["New_column"], as_index=False).agg(
        {"Latitude": "mean", "Longitude": "mean"}
    )

    # Формируем словарь, где каждому городу соответствует его геометрический центр
    new_dict = df.set_index("New_column").T.to_dict("list")
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
