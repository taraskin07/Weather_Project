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


# if __name__ == '__main__':
#
#     api_key = 'W0oJzSg0aPkT3fAHlzAsSwKuIGeJvlOc'
#     from getting_coordinates import get_coordinates_list
#
#     import pandas as pd
#
#     df = pd.read_csv('../../../test_files/DF_max_amount_of_hotels.csv', sep="\t", encoding="utf-8",)
#
#     df1 = df[223:240].reset_index(drop=True)
#     print(df1)
#
#     coord = get_coordinates_list(df)
#
#     new_c1 = coord[223:240]
#     # print(new_c1)
#     # print(len(new_c1))
#
#     # # Combine two dataframes into one by adding columns to the final table.
#     # # Some of the values are NaN.
#     df2 = geopy_address(new_c1, 17, api_key)
#     df = df1.combine_first(df2)
#     print(df.columns)
#
#     # Remove rows with empty values.
#     df = df.dropna(axis=0)
#     unique_country_city = df["Allocation"].unique()
#     print(df.columns)
#
#
#
#     # To make a folder "country/city",
#     # an information is taken from "Allocation" column where the values are a tuple: (country, city).
#     for names in unique_country_city:
#
#         data_proc = df.loc[df["Allocation"] == names]
#         data_proc.reset_index(drop=True, inplace=True)
#         del data_proc["Allocation"]
#         del data_proc["City"]
#         del data_proc["Country"]
#         print(data_proc["Latitude"])
#         # save_df_in_csv_less_than_100_notes(data_proc, output_folder_path)
#
#     # print(coord)
#     # for i in range(len(coord)):
#     #     if '48.8870573, 2.3143297' in coord[i]:
#     #         ind = coord.index(coord[i])
#     #         print(coord[ind])
#     #         print(ind)
#     # new_c2 = coord[341:347]
#     # new_c = new_c1+new_c2
#     # print(new_c)
#     # print(len(new_c))
#     # lat = []
#     # lon = []
#     # for rec in new_c:
#     #     nrec = rec.split(", ")
#     #     lat.append(nrec[0])
#     #     lon.append(nrec[1])
#     # print(lat)
#     # print(lon)
#     # # df2 = pd.DataFrame(columns=df.columns)
#     # df2 = df[df['Latitude'].isin(lat) & df['Longitude'].isin(lon)]
#     # print(df2.head())
#     # print(len(df2))
#     # for string in new_c:
#     #     for i in range(len(df)):
#     #         if string == f'{df.at[i, "Latitude"]}, {df.at[i, "Longitude"]}':
#     #             concat_df = pd.concat([df2,df[i]])
#     # print(concat_df)
#
#     # ndf = geopy_address(new_c, 23, api_key)
#     # print(ndf.head(5))
#     #
#     # print(ndf[5:10])
#     # print(ndf[:5])
#     # print(ndf[10:15])
#     # print(ndf[15:20])
#     # print(ndf.tail(3))
#
#
#
#


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
