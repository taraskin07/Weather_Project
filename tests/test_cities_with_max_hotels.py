from project_scripts.data_assessment.preparing_data import (
    cleaning_dataframe,
    func_to_create_dataframe_from_csv,
    unzip,
)
import pandas as pd
from project_scripts.data_assessment.cities_with_max_hotels import (
    cities_with_max_amount_of_hotel,
)
import os.path as p


def test_cities_with_max_amount_of_hotel():
    path = p.join("tests", "test.zip")
    unzip(path)
    f = func_to_create_dataframe_from_csv("unpacked_files")
    cl_f = cleaning_dataframe(f)
    df_sorted = cities_with_max_amount_of_hotel(cl_f)
    df = pd.DataFrame(df_sorted)

    for index in range(7):
        assert df.iloc[index]["New_column"] == ("AT", "Vienna")
