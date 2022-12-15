import os.path as p

import pandas as pd

import project_scripts.data_assessment.cities_with_max_hotels as cwmh

cities_with_max_amount_of_hotel = cwmh.cities_with_max_amount_of_hotel

import project_scripts.data_assessment.preparing_data as prdat

cleaning_dataframe = prdat.cleaning_dataframe
unzip = prdat.unzip
import project_scripts.data_processing.getting_coordinates as gsc
from project_scripts.data_processing.get_temperatures import get_temperature

center_coordinates = gsc.center_coordinates
get_coordinates_list = gsc.get_coordinates_list


def test_get_temperature():
    dict_city_lat_long = {("AT", "Vienna"): [48.203066462500004, 16.368756425]}
    app_id = "bb92d313e962c39150e26b5318be6a87"
    min, max = get_temperature(dict_city_lat_long, app_id)
    assert isinstance(min, dict)
    assert isinstance(max, dict)


def test_get_and_center_coordinates():
    path = p.join("tests", "test_1_city.zip")
    name_of_folder = p.join("tests", "test_unpacked_files")
    unzip(path, name_of_folder)
    file_path = p.join(name_of_folder, "test_1_city.csv")
    f = pd.read_csv(file_path, sep=",", encoding="utf-8")
    cl_f = cleaning_dataframe(f)
    df = cities_with_max_amount_of_hotel(cl_f)

    lat_vienna = float("{0:.2f}".format(center_coordinates(df)[("AT", "Vienna")][0]))
    lon_vienna = float("{0:.2f}".format(center_coordinates(df)[("AT", "Vienna")][1]))
    assert lat_vienna == 48.2
    assert lon_vienna == 16.37

    assert isinstance(get_coordinates_list(df), list)
    assert get_coordinates_list(df) == [
        "48.2058584, 16.3766545",
        "48.1954348, 16.383429",
        "48.1965878, 16.3413729",
        "48.2163149, 16.3685103",
        "48.2062103, 16.3710387",
        "48.2002872, 16.3547746",
        "48.1955998, 16.3826989",
        "48.2082385, 16.3715725",
    ]
