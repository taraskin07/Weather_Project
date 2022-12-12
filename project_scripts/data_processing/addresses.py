import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from geopy import OpenMapQuest
from geopy.extra.rate_limiter import RateLimiter


def geopy_address(coordinates_list, workers_amount, api_key):
    """
    The function to get an address by coordinates. Allows you to set the number of threads.
    :param workers_amount: number of threads for parallel data processing
    :param coordinates_list: list with coordinates
    :param api_key: API-key from https://developer.mapquest.com/
    :return df: dataframe with address and coordinates
    """
    geolocator = OpenMapQuest(api_key=api_key)

    # Set a delay in seconds to avoid "Too Many Requests 429 error".
    delay = 1 / 20
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=delay)

    with ThreadPoolExecutor(max_workers=workers_amount) as th:
        locations = dict(th.map(geocode, coordinates_list))

    # Dictionary with coordinates and address is converted into a DataFrame.
    df = pd.DataFrame(
        locations.values(), index=locations.keys(), columns=["Latitude", "Longitude"]
    )
    df["Address"] = df.index
    df = df.reset_index(drop=True)
    return df


def create_csv_file_with_addresses(df1, df2, path):
    """
    The function to combine a dataframe with cities with a large number of hotels
    and a dataframe with the addresses of these hotels.

    Columns (Name, Address, Latitude, Longitude).
    Data for each country and city in the csv file are presented separately.

    :param path: path to the directory to save the received files
    :param df1: dataframe with cities with a large number of hotels in the country
    :param df2: dataframe with addresses
    :return:
    """

    # Combine two dataframes into one by adding columns to the final table.
    # Some of the values are NaN.
    df = df1.combine_first(df2)

    # Remove rows with empty values.
    df = df.dropna(axis=0)
    unique_country_city = df["Allocation"].unique()

    # To make a folder "country/city",
    # an information is taken from "Allocation" column where the values are a tuple: (country, city).
    for names in unique_country_city:
        country, city = names
        output_folder_path = f"{path}/{country}/{city}"
        data_proc = df.loc[df["Allocation"] == names]
        data_proc.reset_index(drop=True, inplace=True)
        del data_proc["Allocation"]
        del data_proc["City"]
        del data_proc["Country"]
        save_df_in_csv_less_than_100_notes(data_proc, output_folder_path)


def save_df_in_csv_less_than_100_notes(df, path):
    """
    The function for saving files to csv, no more than 100 entries in each.
    :param df: dataframe
    :param path: the path where the resulting csv file will be saved
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


if __name__ == "__main__":
    coordinates_list = (48.1955998, 16.3826989)
    df = pd.DataFrame(
        geopy_address(coordinates_list, 1, "W0oJzSg0aPkT3fAHlzAsSwKuIGeJvlOc")
    )
    # str = df["Address"].to_list()
    # assert str == [
    #     "Lindner Hotel am Belvedere, 12, Rennweg, Botschaftsviertel, KG Landstraße, Landstraße, Wien, 1030, Österreich"
    # ]
