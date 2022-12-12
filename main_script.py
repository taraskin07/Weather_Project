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
@click.argument("path_to_input_data")  # Путь для исходных данных
@click.argument("path_to_output_data")  # Путь для полученных данных
@click.argument("max_workers_amount")  # Количество потоков
def main(
    path_to_input_data,
    path_to_output_data,
    max_workers_amount,
    api_key="W0oJzSg0aPkT3fAHlzAsSwKuIGeJvlOc",
    app_id="bb92d313e962c39150e26b5318be6a87",
):
    """Утилита предназначена для многопоточной обработки данных,
        аккумулирования результатов через API из Интернета и их дальнейшего представления на графиках.

    Первичная подготовка входных данных для использования data_assessment:
        1. Распаковка архива в папку 'unpacked_files';
        2. Создание dataframe из распакованных файлов;
        3. Исключение из файлов записей, содержащих некорректные/пустые значения;
        4. Поиск городов с максимальным количеством отелей.

    Обработка данных:

        5. Получение географического адреса для каждого из отелей в городах с максимальным количеством отелей
        в многопоточном режиме, при помощи пакета geopy;
        6. Формирование списка отелей (название, адрес, широта, долгота) в формате CSV в файлах, содержащих не более 100 записей в каждом;
        7. Файлы сохраняются в каталог со следующей структурой: {output_folder}\{country}\{city};
        8. В городах с максимальным количеством отелей вычисляется географический центр области города, равноудаленный от крайних отелей;
        9. Получение для центров городов при помощи стороннего сервиса (openweathermap.org) показателей температуры:
            - исторических: за предыдущие 5 дней, текущих включительно;
            - прогноз: на последующие 5 дней;
            - текущих значений.
        10. Построение графиков с минимальной и максимальной температурой, помещаемых в каталог {output_folder}\{country}\{city}.

    Пост-процессинг:
        Для всех вычисленных центров (городов) находятся:
        11. Город и день наблюдения с максимальной температурой за рассматриваемый период;
        12. Город с максимальным изменением максимальной температуры;
        13. Город и день наблюдения с минимальной температурой за рассматриваемый период;
        14. Город и день с максимальной разницей между максимальной и минимальной температурой.
        Результаты помещаются в *.csv файлы в каталог {output_folder}\{post_processing}

    Основной скрипт для запуска консольной утилиты расположен в корневом каталоге проекта: main_script.py

    Для запуска скрипта необходимо выполнить команду:

        python main_script.py data/hotels.zip {output_folder} {max_workers_amount} {api_key} {app_id}
        или
        python3 main_script.py data/hotels.zip {output_folder} {max_workers_amount} {api_key} {app_id}

    Где:
     data/hotels.zip - путь к папке с входными данными;
     {output_folder} - название папки с выходными данными;
     {max_workers_amount} - число потоков (целое);
     {app_id} - API_OpenWeatherMap. Бесплатный API-ключ можно получить на https://openweathermap.org/appid.
     {api_key} - API_OpenMapQuest. Бесплатный API-ключ можно получить на https://developer.mapquest.com/.

    """
    try:
        max_workers_amount = int(max_workers_amount)
    except ValueError:
        print("Количество потоков должно быть числом!")

    # Ввели в консоли путь до файла, распаковываем архив - project_scripts.data_assessment.preparing_data
    unzip(path_to_input_data)
    # Читаем файлы и создаем из них объект dataframe - project_scripts.data_assessment.preparing_data
    df = func_to_create_dataframe_from_csv("unpacked_files")

    # Убираем неправильные записи из dataframe - project_scripts.data_assessment.preparing_data
    df = cleaning_dataframe(df)

    # Ищем города, в которых больше всего отелей в отдельной стране - project_scripts.data_assessment.cities_with_max_hotels
    df = cities_with_max_amount_of_hotel(df)

    # Помещаем в переменную список с коордниатами - project_scripts.data_processing.getting_coordinates
    coordinates_list = get_coordinates_list(df)

    # По списку координат получаем список адресов в виде dataframe - project_scripts.data_processing.addresses
    df_lon_lat_address = geopy_address(coordinates_list, max_workers_amount, api_key)

    # В указанную через консоль папку помещаем требуемые csv файлы с адресами, меньше 100 записей, все в подпапках - project_scripts.data_processing.addresses
    create_csv_file_with_addresses(df, df_lon_lat_address, path_to_output_data)

    # Находим центр координат для каждого города из топ по количеству отелей и создаем из этого словарь - project_scripts.data_processing.getting_coordinates
    central_coordinates_dict = center_coordinates(df)

    # Получаем температуры для центров городов с максимальным количеством отелей на разные дни - project_scripts.data_processing.get_temperatures
    min_temperature, max_temperature = get_temperature(central_coordinates_dict, app_id)

    # Строим графики температуры от даты - project_scripts.data_processing.plots_min_max_temp
    graph_with_min_temperature(min_temperature, path_to_output_data)
    graph_with_max_temperature(max_temperature, path_to_output_data)

    # Пост-процессинг project_scripts.post_processing
    post_processing(max_temperature, min_temperature, path_to_output_data)


if __name__ == "__main__":
    main()
