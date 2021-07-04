from project_scripts.data_processing.get_temperatures import get_temperature
from project_scripts.data_processing.getting_coordinates import (
    center_coordinates,
    get_coordinates_list,
)
from project_scripts.data_assessment.preparing_data import (
    cleaning_dataframe,
    func_to_create_dataframe_from_csv,
    unzip,
)
from project_scripts.data_assessment.cities_with_max_hotels import (
    cities_with_max_amount_of_hotel,
)
import os.path as p
import pandas as pd


def test_get_temperature():
    dict_city_lat_long = {("AT", "Vienna"): [48.203066462500004, 16.368756425]}
    app_id = "2bb1a0368b668b3ce5451b54f1ab78d9"
    min, max = get_temperature(dict_city_lat_long, app_id)
    assert isinstance(min, dict)
    assert isinstance(max, dict)


def test_get_and_center_coordinates():
    path = p.join("tests", "test_1_city.zip")
    unzip(path)
    file_path = p.join("unpacked_files", "test_1_city.csv")
    f = pd.read_csv(file_path, sep=",", encoding="utf-8")
    cl_f = cleaning_dataframe(f)
    df = cities_with_max_amount_of_hotel(cl_f)

    lat_vienna = float("{0:.2f}".format(center_coordinates(df)[("AT", "Vienna")][0]))
    lon_vienna = float("{0:.2f}".format(center_coordinates(df)[("AT", "Vienna")][1]))
    assert lat_vienna == 48.2
    assert lon_vienna == 16.37

    print(get_coordinates_list(df))

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
