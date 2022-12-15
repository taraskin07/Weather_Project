# PythonLab - 2021
# Final course project

It is necessary to write a console utility for multi-threaded data processing, accumulation of results via API from the Internet and their further presentation on charts.

## Input data
The input data is located in the **/data** directory in this repository, packaged in the **hotels.zip** file.

Inside this archive there are several files in the _.CSV_ format containing many lines with information on hotels. Including, among the information you will find:

- the name of the hotel;
- latitude and longitude of the hotel;
- the country and city where the object is located.

## Output
All generated results should be located in the output directory with the following structure:

`{output_folder}\{country}\{city}\`

## Task

The task consists of several blocks and requirements, which are listed below:

1. The application must be a console utility that accepts the following parameters as input:

   - path to the directory with input data;
   - path to the output directory;
   - number of threads for parallel data processing
   - possible other parameters necessary for the operation of the application.
    
2. Initial preparation of input data for use:

    - unpack the archive with data;
    - clear data from invalid records (containing deliberately false values or missing necessary elements);
    - make a grouping: for each country, select the city containing the maximum number of hotels.
    
3. Data processing:
    
    - Enrich the data for each of the hotels in the selected cities in **multi-threaded mode** with its geographic address obtained using the **geopy** package;
    - Calculate the geographical center of the city area, equidistant from the extreme hotels.
    - For the center of the region, using a third-party service (for example, _openweathermap.org_) get weather data:
    
        - historical: for the previous 5 days;
        - forecast: for the next 5 days;
        - current values.
    - Create charts (for example, using the **matplotlib** package) containing day dependencies:
    
        - minimum temperature;
        - maximum temperature.
    
4. Post processing:

    - Among all centers (cities) find:
        
        - city and day of observation with the maximum temperature for the period under consideration;
        - the city with the maximum change in maximum temperature;
        - city and day of observation with the minimum temperature for the period under consideration;
        - city and day with the maximum difference between the maximum and minimum temperatures.
    
5. Saving results:

   - In the directory with the specified structure for each city, save:
        
        - all received charts;
        - a list of hotels (name, address, latitude, longitude) in CSV format in files containing no more than 100 entries each;
        - the information received by the center in an arbitrary format, convenient for subsequent use.
    
# Project Requirements:

- The version of the interpreter is not lower than 3.7;
- Completed _requirements.txt_ or _poetry.toml_;
- Completed _.gitignore_;
- The choice of the final toolkit for completing the task is largely up to the performer, for example:
  
 - argparser - for processing command line parameters;
 - geopy - to get an address by coordinates;
 - matplotlib - for plotting;
 - zipfile - for working with archives;
 - requests, urllib, aiohttp client, etc - for making requests to an external API;
 - threading, multiprocessing, asyncio, etc - for "parallelization" of tasks;
 - pytest, unittest - for creating tests;
 - pandas - for representing data in the form of data frames;
 - csv - for working with CSV files;
 - and many more - both from the python bundle and third-party packages.
 
- Key code snippets should be covered by unit tests;
- The code must be drawn up in accordance with the recommendations given to you during the course;
- Documentation must be present to allow a stranger to start using the application.

