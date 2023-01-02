import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from geopy import MapQuest
from geopy.extra.rate_limiter import RateLimiter


def geopy_address(coordinates_list, workers_amount, api_key):
    """
    The function to get an address by coordinates. Allows one to set the number of threads.

    :param workers_amount: number of threads for parallel data processing
    :param coordinates_list: list with coordinates
    :param api_key: API-key from https://developer.mapquest.com/
    :return df: dataframe with address and coordinates
    """

    #Using MapQuest service.
    geolocator = MapQuest(api_key=api_key)

    # Counter for empty responses if any.
    empty_address_counter = 0

    def my_iterator(coord):
        """
        Additional function to get a proper response from API.

        :param coord: latitude and longitude values from coordinates_list
        :return str, tuple of str: "Address", ("Latitude", "Longitude")
        """
        # Set a delay in seconds to avoid "Too Many Requests 429 error".
        delay = 1 / 20
        get_address = RateLimiter(geolocator.reverse, min_delay_seconds=delay)
        location = get_address(coord, exactly_one=True)
        get_address = location.address
        if get_address == '':
            nonlocal empty_address_counter
            empty_address_counter += 1
            get_address = f'Empty response for address request #{empty_address_counter}'
        latit, longit = coord.split(', ')
        return get_address, (latit, longit)

    with ThreadPoolExecutor(max_workers=workers_amount) as th:
        locations = dict(th.map(my_iterator, coordinates_list))

    # Constructing dataframe from dictionary {"Address": ("Latitude", "Longitude")}
    df = pd.DataFrame(
        locations.values(), index=locations.keys(), columns=["Latitude", "Longitude"]
    )
    df["Address"] = df.index
    df = df.astype({"Latitude": str})
    df = df.astype({"Longitude": str})
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


    # Making sure that all significant variables of the same and desired format in both dataframes to merge (lan/lot - string).
    df1['Latitude'] = df1['Latitude'].astype(str)
    df1['Longitude'] = df1['Longitude'].astype(str)
    df2['Latitude'] = df2['Latitude'].astype(str)
    df2['Longitude'] = df2['Longitude'].astype(str)

    # Merging two dataframes into one by adding columns to the final table where 'Latitude' and 'Longitude' values are match.
    # Inner join on lat/lon (merge).
    df = pd.merge(df1, df2, how='inner', on=['Latitude', 'Longitude'])

    # Remove rows with empty values if any.
    df = df.dropna(axis=0)

    unique_country_city = df["Allocation"].unique().tolist()

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


