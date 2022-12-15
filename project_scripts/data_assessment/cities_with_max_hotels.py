def cities_with_max_amount_of_hotel(df):
    """
    This function finds cities with maximum amount of hotels in a particular country.
    :param df: dataframe
    :return df_sorted: sorted dataframe with cities that have maximum amount of hotels
    """
    # Getting object "Series", this object is sorted by country and city. Creating the dataframe from "Series".
    # Adding "Size" column with values that reflect amount od hotels in the city.
    df_new = df.groupby(["Country", "City"]).size().to_frame("Size").reset_index()

    # Finding cities with the maximum amount of hotels.
    top_cities_with_max_hotels_df = df_new.sort_values(
        "Size", ascending=False
    ).drop_duplicates(["Country"])

    # Adding new column "Allocation" (to both initital and final dataframe).
    # This is because some cities have the same names, but are located in different countries.
    # Column "Allocation" data is a tuple that contains information about both "Country" and "City".
    top_cities_with_max_hotels_df["Allocation"] = top_cities_with_max_hotels_df[
        ["Country", "City"]
    ].apply(tuple, axis=1)
    df["Allocation"] = df[["Country", "City"]].apply(tuple, axis=1)

    # Now sorted dataframe contains information about hotel amount in a specific cities, taking into account the country in which they are located.
    df_sorted = df.loc[
        df["Allocation"].isin(top_cities_with_max_hotels_df["Allocation"].values)
    ]
    df_sorted = df_sorted.sort_values(["Country"])
    return df_sorted
