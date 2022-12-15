import glob as g
import zipfile as z

import pandas as pd


def unzip(path, output_path="unpacked_files"):
    """
    A function that unzip file into 'unpacked_files' directory.
    :param path: path to zip file
    """
    with z.ZipFile(path, "r") as myzip:
        myzip.extractall(output_path)


def func_to_create_dataframe_from_csv(folder):
    """
    A function that creates dataframe from unzipped csv files.
    :param folder: folder path with csv files
    :return dataframe: result dataframe
    """
    dataframe = pd.concat(
        [
            pd.read_csv(file, sep=",", encoding="utf-8")
            for file in g.glob(folder + "/*.csv")
        ],
        ignore_index=True,
    )
    return dataframe


def cleaning_dataframe(frame):
    """
    This function clear data from invalid information
    (false or missing values).
    :param frame: initial dataframe
    :return clean_frame: fixed dataframe
    """
    frame = frame.dropna(axis=0, how="any")
    index_list_to_drop_in_dataframe = []
    for index, value in frame.iterrows():
        try:
            latitude = float(value["Latitude"])
            longitude = float(value["Longitude"])
            if abs(latitude) > 180 or abs(longitude) > 180:
                index_list_to_drop_in_dataframe.append(index)
        except ValueError:
            index_list_to_drop_in_dataframe.append(index)

    clean_frame = frame.drop(index_list_to_drop_in_dataframe)
    clean_frame.reset_index(drop=True, inplace=True)
    return clean_frame
