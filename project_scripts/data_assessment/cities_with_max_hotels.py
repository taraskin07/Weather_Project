def cities_with_max_amount_of_hotel(df):
    """
    Функция для поиска городов, в которых больше всего отелей в отдельной стране
    :param df: dataframe
    :return df_sorted: отсортированный dataframe с городами в которых больше всего отелей в стране
    """
    # Получение объекта Series, отсортированного по стране и городу, перевод в объект dataframe. Добавление столбца Size со значением отелей в городе
    df_new = df.groupby(["Country", "City"]).size().to_frame("Size").reset_index()

    # Поиск городов с наибольшим числом отелей
    top_cities_with_max_hotels_df = df_new.sort_values(
        "Size", ascending=False
    ).drop_duplicates(["Country"])

    # Получение новой колонки как в исходном, так и в конечном dataframe, т.к. некоторые города имеют одинаковые названия, но принадлежат разным странам
    top_cities_with_max_hotels_df["New_column"] = top_cities_with_max_hotels_df[
        ["Country", "City"]
    ].apply(tuple, axis=1)
    df["New_column"] = df[["Country", "City"]].apply(tuple, axis=1)

    #  Преобразование исходного dataframe для отображения информации лишь по отелям определенных городов
    df_sorted = df.loc[
        df["New_column"].isin(top_cities_with_max_hotels_df["New_column"].values)
    ]
    df_sorted = df_sorted.sort_values(["Country"])
    return df_sorted


if __name__ == "__main__":
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
