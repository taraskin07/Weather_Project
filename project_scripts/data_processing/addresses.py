import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from geopy import MapQuest
from geopy.extra.rate_limiter import RateLimiter


def geopy_address(coordinates_list, workers_amount, api_key):
    """
    The function to get an address by coordinates. Allows you to set the number of threads.
    :param workers_amount: number of threads for parallel data processing
    :param coordinates_list: list with coordinates
    :param api_key: API-key from https://developer.mapquest.com/
    :return df: dataframe with address and coordinates
    """
    geolocator = MapQuest(api_key=api_key)

    # Set a delay in seconds to avoid "Too Many Requests 429 error".
    delay = 1 / 20
    get_address = RateLimiter(geolocator.reverse, min_delay_seconds=delay)

    with ThreadPoolExecutor(max_workers=workers_amount) as th:
        locations = dict(th.map(get_address, coordinates_list))



    # Dictionary with coordinates and address is converted into a DataFrame.
    df = pd.DataFrame.from_dict(locations, orient='index')

    # There is no proper index and previous one is oriented wrong (columns: 'index', 0, 1).
    df = df.reset_index()

    # New index has been constructed.
    # Now columns need to be renamed properly (columns: 'index', 0, 1 ==> 'Address', 'Latitude', 'Longitude').
    df = df.rename(columns = {"index":"Address", 0:"Latitude", 1:"Longitude"})
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


# if __name__ == '__main__':
#     # coordinates_list = [[48.1955998, 16.3826989], [47.1955998, 15.3826989]]
#     # geolocator = MapQuest(api_key='W0oJzSg0aPkT3fAHlzAsSwKuIGeJvlOc')
#     #
#     # # Set a delay in seconds to avoid "Too Many Requests 429 error".
#     # delay = 1 / 20
#     # get_address = RateLimiter(geolocator.reverse, min_delay_seconds=delay)
#     #
#     # with ThreadPoolExecutor(max_workers=2) as th:
#     #     locations = dict(th.map(get_address, coordinates_list))
#     locations = {'12 Rennweg, 3. Bezirk-Landstraße, Wien, Wien, 9, AT, 1030': (48.19596, 16.38288), 'Am Hiening, Semriach, Graz-Umgebung, 6, AT, 8102': (47.19543, 15.38107),'12  9, AT, 1030': (22.19896, 33.38288),}
#
#     # print (f'Locations keys are: \n{locations.keys()}')
#     # print (f'Locations values are: \n{locations.values()}')
#
#     print(locations)
#
#     # Dictionary with coordinates and address is converted into a DataFrame.
#     df = pd.DataFrame(
#         locations.values(), index=locations.keys(), columns=["Latitude", "Longitude"]
#     )
#     df["Address"] = df.index
#     df = df.reset_index(drop=True)
#     print (f'Dataframe: \n\n{df.head()}')
#
#     df = pd.DataFrame.from_dict(locations, orient='index').reset_index()
#     df = df.rename(columns = {"index":"Address", 0:"Latitude", 1:"Longitude"})
#     print(f'Dataframe Address: \n\n{df.head()}')
#     # # df["Address"] = df.index
#     # #
#     # print (f'Dataframe reset: \n\n{df.head()}')