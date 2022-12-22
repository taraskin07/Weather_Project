def recursion_func(df, df_allocation, precision=2):


    """
    This function clean the initial dataset (param: df) from coordinates, related to different cities with the same name in the same country,
    with the help of subset dataframe (param: df_allocation),
    that contain information about each allocation (both country and city: ('Country', 'City') tuple, column "Allocation").

    :param df: initial dataframe to be cleaned
    :param df_allocation: dataframe - subset for specific allocation ('Country', 'City')
    :param precision: float or integer - allowable error (integer or float degrees) in determining a coordinate as valid and related to the same city, default = 2 degrees
    :return df: cleaned dataframe, without irrelevant rows for particular allocation
    """
    df_allocation = df_allocation.astype({"Latitude": float})
    df_allocation = df_allocation.astype({"Longitude": float})

    # Finding mean values to establish how differs each value of latitude and latitude from their average in group of coordinates for city with the same name/
    latitude_mean = df_allocation["Latitude"].mean()

    # Setting up precision. A range in which each value should be, in order to refer to the same city.
    upper_lat = float(latitude_mean) + float(precision)
    lower_lat = float(latitude_mean) - float(precision)

    # Same for longitude.
    longitude_mean = df_allocation["Longitude"].mean()

    upper_lon = float(longitude_mean) + float(precision)
    lower_lon = float(longitude_mean) - float(precision)

    # For each coordinate in a subset for specific allocation it is necessary to establish whether it is inside the valid value range or not.
    for index, row in df_allocation.iterrows():

        latitude=row['Latitude']
        longitude=row['Longitude']

        # If some value is outside the valid range we need to understand what is the most common coordinate value.
        if not lower_lat < float(latitude) < upper_lat:

            # List for values in order to find the mosst common one.
            max_difference_lat_list = []

            # Difference for each value from the most common one.
            max_difference_lat=0

            # Finding the most common value of coordinate.
            for index, row in df_allocation.iterrows():
                lat = row['Latitude']
                # Coordinates differs from each other, but if they will be rounded to the integer part, then for the most part they will be the same.
                lat = round(lat, 0)
                max_difference_lat_list.append(lat)
            most_common_value_lat = max(set(max_difference_lat_list), key=max_difference_lat_list.count)

            # Finding the value that differs the most from the most common coordinate
            for index, row in df_allocation.iterrows():
                value = abs(abs(row['Latitude'])-abs(most_common_value_lat))
                if value > max_difference_lat:
                    max_difference_lat = value
                    # Both dataframes have column with IDs which identify the rows.
                    # Eventually the ID for the most difference will be saved in 'id_m' variable.
                    id_m = row['Id']

            # This row (corresponding to specific ID) now deleted from both initial dataframe and its subset.
            df_allocation = df_allocation[df_allocation.Id != id_m]
            df = df[df.Id != id_m]

            # Procedure need to be repeated to clear dataframe from all invalid coordinates step by step.
            return recursion_func(df, df_allocation)

        # If latitude coordinates now fine longitude values need to be checked.
        elif not lower_lon < float(longitude) < upper_lon:

            # List for values in order to find the mosst common one.
            max_difference_lon_list = []

            # Difference for each value from the most common one.
            max_difference_lon = 0
            for index, row in df_allocation.iterrows():
                lon = row['Longitude']
                lon = round(lon, 0)
                max_difference_lon_list.append(lon)
            most_common_value_lon = max(set(max_difference_lon_list), key=max_difference_lon_list.count)

            # Finding the most common value of coordinate.
            for index, row in df_allocation.iterrows():
                value = abs(abs(row['Longitude'])-abs(most_common_value_lon))
                if value > max_difference_lon:
                    max_difference_lon = value
                    id_m = row['Id']
            # Again this row (corresponding to specific ID) now deleted from both initial dataframe and its subset.
            df_allocation = df_allocation[df_allocation.Id != id_m]
            df = df[df.Id != id_m]
            return recursion_func(df, df_allocation)

    # After all procedures the initial dataframe without irrelevant rows for particular allocation is returned.
    return df

def city_location_check(df, precision=2):


    """
    This function clean the initial dataset (param: df) from coordinates,
    related to different cities with the same name
    by constructing the subset dataframe for each unique allocation found,
    (both country and city: ('Country', 'City') tuple, column "Allocation")
    and start the process of cleaning with the help of 'recursion_func'.

    :param df: initial dataframe to be cleaned
    :param precision: integer - allowable error (integer degrees) in determining a coordinate as valid and related to the same city, default = 2 degrees
    :return df: clean dataframe, without irrelevant rows
    """


    # Finding list of uniqie allocations.
    df_allocation = df["Allocation"].unique()
    df_allocation=list(map(tuple, df_allocation))

    # Constructing a subset dataframe.
    for allocation in df_allocation:
        df_allocation = df.loc[df['Allocation'] == allocation]

        # Launching the recursion_func for each allocation.
        df = recursion_func(df, df_allocation)

    return df
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

    # Launching the city_location_check function in order to clean dataframe from cities with the same name and country.
    df_max_hotels = city_location_check(df_sorted)

    return df_max_hotels


