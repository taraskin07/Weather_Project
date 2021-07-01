import click

from project_scripts.data_assessment.cities_with_max_hotels import \
    cities_with_max_amount_of_hotel
from project_scripts.data_assessment.preparing_data import (
    cleaning_dataframe, func_to_create_dataframe_from_csv, unzip)
from project_scripts.data_processing.addresses import (
    create_csv_file_with_addresses, geopy_address,
    save_df_in_csv_less_than_100_notes)
from project_scripts.data_processing.get_temperatures import get_temperature
from project_scripts.data_processing.getting_coordinates import (
    center_coordinates, get_coordinates_list)
from project_scripts.data_processing.plots_min_max_temp import (
    graph_with_max_temperature, graph_with_min_temperature)


# from project_scripts.post_processing import
@click.command()
@click.argument("path_to_input_data")  # Путь для исходных данных
@click.argument("path_to_output_data")  # Путь для полученных данных
@click.argument("max_workers_amount")  # Количество потоков
def main(path_to_input_data, path_to_output_data, max_workers_amount):
    """Утилита предназначена для многопоточной обработки данных,
        аккумулирования результатов через API из Интернета и их дальнейшего представления на графиках.

    Первичная подготовка входных данных для использования data_assessment:
        1. Распаковать
        2. Создать датафреймы из распакованных файлов
        3. Убрать в них всё лишнее
        4. Достать города с максимальым количеством отелей

    Обработка данных :

        5. Получить координаты - Обогатить данные по каждому из отелей в выбранных городах
        в **многопоточном режиме** его географическим адресом, полученным при помощи пакета **geopy**;
        6. По координатам получить адреса
        7. Записать полученную информацию в csv файл
        8. В городах с максимальным количеством отелей посчитать центр координат
        9. Получить для центров мин макс погоду
            - исторические: за предыдущие 5 дней;
            - прогноз: на последующие 5 дней;
            - текущие значения.
        10. Графики с минимальной и максимальной температурой

    Пост-процессинг:

        11. Найти город и день с максимальной температурой
        12.  Найти город с максимальным приростом температуры, с максимальным изменением максимальной температуры;
        13. Найти город и день с минимальной температурой

        14. Найти город и день с максимальной разницей температур

    Сохранение результатов:

        - В каталоге с указанной структурой для каждого города:
            - все полученные графики;
            - список отелей (название, адрес, широта, долгота) в формате CSV в файлах, содержащих не более 100 записей в каждом;
            - полученную информацию по центру в произвольном формате, удобном для последующего использования.

    """
    try:
        max_workers_amount = int(max_workers_amount)
    except ValueError:
        print("Количество потоков должно быть числом")

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
    df_lon_lat_address = geopy_address(coordinates_list, max_workers_amount)

    # В указанную через консоль папку помещаем требуемые csv файлы с адресами, меньше 100 записей, все в подпапках - project_scripts.data_processing.addresses
    create_csv_file_with_addresses(df, df_lon_lat_address, path_to_output_data)

    # Находим центр координат для каждого города из топ по количеству отелей и создаем из этого словарь - project_scripts.data_processing.getting_coordinates
    central_coordinates_dict = center_coordinates(df)

    # Получаем температуры для центров городов с максимальным количеством отелей на разные дни - project_scripts.data_processing.get_temperatures
    min_temperature, max_temperature = get_temperature(central_coordinates_dict)

    # Строим графики температуры от даты - project_scripts.data_processing.plots_min_max_temp
    graph_with_min_temperature(min_temperature, path_to_output_data)
    graph_with_max_temperature(max_temperature, path_to_output_data)

    # Пост-процессинг project_scripts.post_processing
    # в разработке...


if __name__ == "__main__":
    main()
