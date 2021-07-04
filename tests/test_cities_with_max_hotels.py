import os.path as p

import pandas as pd

import project_scripts.data_assessment.cities_with_max_hotels as cwmh

cities_with_max_amount_of_hotel = cwmh.cities_with_max_amount_of_hotel
import project_scripts.data_assessment.preparing_data as prdat

cleaning_dataframe = prdat.cleaning_dataframe
func_to_create_dataframe_from_csv = prdat.func_to_create_dataframe_from_csv
unzip = prdat.unzip


def test_cities_with_max_amount_of_hotel():
    path = p.join("tests", "test.zip")
    unzip(path)
    f = func_to_create_dataframe_from_csv("unpacked_files")
    cl_f = cleaning_dataframe(f)
    df_sorted = cities_with_max_amount_of_hotel(cl_f)
    df = pd.DataFrame(df_sorted)

    for index in range(7):
        assert df.iloc[index]["New_column"] == ("AT", "Vienna")
