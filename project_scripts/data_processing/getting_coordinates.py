def center_coordinates(df):
    """
    The function finds the coordinate centers for each city with the maximum amount of hotels.
    :param df: dataframe that contain list of cities with the maximum amount of hotels
    :return: dictionary, where each city corresponds to its geometric center
    """
    # Converting str coordinates to float.
    df = df.astype({"Latitude": float})
    df = df.astype({"Longitude": float})

    # For each unique city: 'Allocation'(Country, City) - average values, calculated from every hotel coordinates in this city.
    df = df.groupby(["Allocation"], as_index=False).agg(
        {"Latitude": "mean", "Longitude": "mean"}
    )

    # Obtaining a dictionary where each city corresponds to geometric center coordinates.
    new_dict = df.set_index("Allocation").T.to_dict("list")

    return new_dict


def get_coordinates_list(df):
    """
    The function converts the dataframe into a list of strings with coordinates 'Latitude', 'Longitude'.
    :param df: dataframe that contain list of cities with the maximum amount of hotels
    :return list: list with coordinates: ['Latitude, Longitude']
    """
    df = df[["Latitude", "Longitude"]]
    df = df.astype({"Latitude": str})
    df = df.astype({"Longitude": str})
    # Making a new column by concatenating the 'Latitude' and 'Longitude' columns (their values) separated by commas
    df["Coordinates"] = [
        (x + ", " + y) for x, y in zip(df.Latitude.values, df.Longitude.values)
    ]
    # Making a list with coordinates separated by commas.
    coordinates_list = df["Coordinates"].tolist()
    return coordinates_list
