import click

import project_scripts.data_assessment.cities_with_max_hotels as cty

cities_with_max_amount_of_hotel = cty.cities_with_max_amount_of_hotel
import project_scripts.data_assessment.preparing_data as prdat

cleaning_dataframe = prdat.cleaning_dataframe
func_to_create_dataframe_from_csv = prdat.func_to_create_dataframe_from_csv
unzip = prdat.unzip
import project_scripts.data_processing.addresses as adrs

create_csv_file_with_addresses = adrs.create_csv_file_with_addresses
geopy_address = adrs.geopy_address
import project_scripts.data_processing.getting_coordinates as gsc
from project_scripts.data_processing.get_temperatures import get_temperature

center_coordinates = gsc.center_coordinates
get_coordinates_list = gsc.get_coordinates_list
import project_scripts.data_processing.plots_min_max_temp as plots

graph_with_max_temperature = plots.graph_with_max_temperature
graph_with_min_temperature = plots.graph_with_min_temperature
from project_scripts.post_processing import post_processing


@click.command()
@click.argument("path_to_input_data")  # Path to input data
@click.argument("path_to_output_data")  # Path to output data
@click.argument("max_workers_amount")  # Number of threads
def main(
    path_to_input_data,
    path_to_output_data,
    max_workers_amount,
    api_key="wy01c9Acc0xG02747DcgFvOx90KPkCAq",
    app_id="bb92d313e962c39150e26b5318be6a87",
):
    """The utility is designed for multi-threaded data processing,
         accumulation of results via API from the Internet and their further presentation on charts.
    
    Initial preparation of input data (scripts folder - data_assessment):
        1. Unpacking the archive into the 'unpacked_files' folder;
        2. Creating a dataframe from unpacked files;
        3. Exclusion from files of records containing incorrect/empty values;
        4. Search for cities with the maximum number of hotels.

    Data processing (folder - data_processing):

        5. Getting the geographic address for each of the hotels in the cities with the maximum number of hotels
         in multithread mode, using the geopy package;
        6. Creation a list of hotels (name, address, latitude, longitude) in CSV format in files containing no more than 100 entries each;
        7. Files are saved to a directory with the following structure: {output_folder}\{country}\{city};
        8. In cities with the maximum number of hotels, the geographical center of the city area is calculated, equidistant from the extreme hotels;
        9. Obtaining temperature indicators for city centers using a third-party service (openweathermap.org):
            - historical: for the previous 5 days;
            - forecast: for the next 5 days;
            - current values.
        10. Plotting the minimum and maximum temperatures placed in the {output_folder}\{country}\{city} directory.

    Post-processing (post_processing.py):
        For all calculated centers (cities) it is necessary to find:
        11. City and day of observation with the maximum temperature for the period under consideration;
        12. The city with the maximum change in maximum temperature;
        13. City and day of observation with the minimum temperature for the period under consideration;
        14. The city and day with the maximum difference between the maximum and minimum temperatures.
        The results are placed in *.csv files in the directory {output_folder}\{post_processing}

    The main script for running the console utility is located in the root directory of the project: main_script.py

    To run the script, enter the following command:

        python main_script.py data/hotels.zip {output_folder} {max_workers_amount} {api_key} {app_id}
        or
        python3 main_script.py data/hotels.zip {output_folder} {max_workers_amount} {api_key} {app_id}

    Where:
     data/hotels.zip - path to the folder with input data;
     {output_folder} - the name of the output folder;
     {max_workers_amount} - number of threads (integer);
     {app_id} - API_OpenWeatherMap. You can get a free API key at https://openweathermap.org/appid.
     {api_key} - API_MapQuest. A free API key can be obtained at https://developer.mapquest.com/.
    Additional key api_key="W0oJzSg0aPkT3fAHlzAsSwKuIGeJvlOc"

    """
    try:
        max_workers_amount = int(max_workers_amount)
    except ValueError:
        print("The number of threads must be an integer!")

    # The path to the file is entered via CLI, unpack the archive - project_scripts.data_assessment.preparing_data
    unzip(path_to_input_data)
    # Reading files and creating a dataframe object from them - project_scripts.data_assessment.preparing_data
    df = func_to_create_dataframe_from_csv("unpacked_files")

    # Removing invalid entries from the dataframe - project_scripts.data_assessment.preparing_data
    df = cleaning_dataframe(df)

    # Looking for cities with the most hotels in a particular country - project_scripts.data_assessment.cities_with_max_hotels
    df = cities_with_max_amount_of_hotel(df)

    # Place a list with coordinates in a variable - project_scripts.data_processing.getting_coordinates
    coordinates_list = get_coordinates_list(df)

    # According to the list of coordinates, get a list of addresses in the form of a dataframe - project_scripts.data_processing.addresses
    df_lon_lat_address = geopy_address(coordinates_list, max_workers_amount, api_key)

    # In the folder specified via the console, place the required csv files with addresses, less than 100 entries, all in subfolders - project_scripts.data_processing.addresses
    create_csv_file_with_addresses(df, df_lon_lat_address, path_to_output_data)

    # Find the center of coordinates for each city from the top by the number of hotels and create a dictionary from this - project_scripts.data_processing.getting_coordinates
    central_coordinates_dict = center_coordinates(df)

    # Getting temperatures for city centers with the maximum number of hotels on different days - project_scripts.data_processing.get_temperatures
    min_temperature, max_temperature = get_temperature(central_coordinates_dict, app_id)

    # Build temperature graphs from the date - project_scripts.data_processing.plots_min_max_temp
    graph_with_min_temperature(min_temperature, path_to_output_data)
    graph_with_max_temperature(max_temperature, path_to_output_data)

    # Post-processing - project_scripts.post_processing
    post_processing(max_temperature, min_temperature, path_to_output_data)


if __name__ == "__main__":
    main()
