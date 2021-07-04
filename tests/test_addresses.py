from project_scripts.data_processing.addresses import (
    geopy_address,
    create_csv_file_with_addresses,
)
import pandas as pd


def test_geopy_address():
    coordinates_list = [[48.1955998, 16.3826989]]
    df = pd.DataFrame(
        geopy_address(coordinates_list, 60, "G8uzA4xdsG5B0uLcekeCowprs41bkZlb")
    )
    str = df["Address"].to_list()
    assert str == [
        "Lindner Hotel am Belvedere, 12, Rennweg, Botschaftsviertel, KG Landstraße, Landstraße, Wien, 1030, Österreich"
    ]
