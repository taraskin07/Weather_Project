import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def graph_with_min_temperature(min_temperature, path):
    """
    Получение графиков зависимости минимальной температуры от дня
    :param min_temperature: словарь key: дата, value: минимальная температура
    :param path: путь для сохранения графиков, /country/city
    """
    df_min_temperatures = pd.DataFrame(min_temperature)
    for frame in df_min_temperatures:
        country, city = frame
        ax = sns.lineplot(x=df_min_temperatures.index, y=df_min_temperatures[frame])
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.3)
        ax.set_title("График зависимости минимальной температуры от даты", fontsize=14)
        ax.set_xlabel("Дата", fontsize=12)
        ax.set_ylabel("Температура, гр", fontsize=12)
        fig = ax.get_figure()
        path_part = os.path.join(path, country)
        whole_path = os.path.join(path_part, city)
        os.makedirs(f"{whole_path}", exist_ok=True)
        file_path = os.path.join(whole_path, f"min_temperature_{city}")
        fig.savefig(f"{file_path}.png")
        plt.clf()


def graph_with_max_temperature(max_temperature, path):
    """
    Получение графиков зависимости максимальной температуры от дня
    :param max_temperature: словарь key: дата, value: максимальная температура
    :param path: путь для сохранения графиков, /country/city
    """
    df_max_temperatures = pd.DataFrame(max_temperature)
    for frame in df_max_temperatures:
        country, city = frame
        ax = sns.lineplot(x=df_max_temperatures.index, y=df_max_temperatures[frame])
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.25)
        ax.set_title("График зависимости максимальной температуры от даты", fontsize=14)
        ax.set_xlabel("Дата", fontsize=12)
        ax.set_ylabel("Температура, гр", fontsize=12)
        fig = ax.get_figure()
        path_part = os.path.join(path, country)
        whole_path = os.path.join(path_part, city)
        os.makedirs(f"{whole_path}", exist_ok=True)
        file_path = os.path.join(whole_path, f"max_temperature_{city}")
        fig.savefig(f"{file_path}.png")
        plt.clf()
