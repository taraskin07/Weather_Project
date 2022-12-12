import pandas as pd

import project_scripts.data_processing.addresses as adrss

create_csv_file_with_addresses = adrss.create_csv_file_with_addresses
geopy_address = adrss.geopy_address


def test_geopy_address():
    coordinates_list = [[48.1955998, 16.3826989]]
    df = pd.DataFrame(
        geopy_address(coordinates_list, 60, "W0oJzSg0aPkT3fAHlzAsSwKuIGeJvlOc")
    )
    str = df["Address"].to_list()
    assert str == [
        "Lindner Hotel am Belvedere, 12, Rennweg, Botschaftsviertel, KG Landstraße, Landstraße, Wien, 1030, Österreich"
    ]
