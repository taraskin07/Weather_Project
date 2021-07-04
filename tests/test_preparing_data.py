import os.path as p

import pandas as pd

import project_scripts.data_assessment.preparing_data as prdat

cleaning_dataframe = prdat.cleaning_dataframe
func_to_create_dataframe_from_csv = prdat.func_to_create_dataframe_from_csv
unzip = prdat.unzip


def test_unzip():
    path = p.join("tests", "test.zip")
    unzip(path)
    file_path = p.join("unpacked_files", "test.csv")
    assert p.exists(file_path)


def test_func_to_create_dataframe_from_csv():
    path = p.join("tests", "test.zip")
    unzip(path)
    f = func_to_create_dataframe_from_csv("unpacked_files")
    cl_f = cleaning_dataframe(f)
    assert len(cl_f["Latitude"]) == len(cl_f["Longitude"])
    df = pd.DataFrame(cl_f)
    assert df.iloc[53]["Name"] == "Econo Lodge"
