import pandas as pd

import project_scripts.data_processing.addresses as adrss

create_csv_file_with_addresses = adrss.create_csv_file_with_addresses
geopy_address = adrss.geopy_address


def test_geopy_address():
    coordinates_list = ['48.1955998, 16.3826989']
    df = pd.DataFrame(
        geopy_address(coordinates_list, 1, "W0oJzSg0aPkT3fAHlzAsSwKuIGeJvlOc")
    )
    addr = df["Address"].to_list()
    assert addr == ["12 Rennweg, 3. Bezirk-Landstraße, Wien, Wien, 9, AT, 1030"]
