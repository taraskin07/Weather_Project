import os

import matplotlib.pyplot as plt
import seaborn as sns


def graph_with_min_temperature(min_temperature, path):
    """
    Constructing plots for minimum daily temperature.
    :param min_temperature: dictionary key: date, value: minimum temperature
    :param path: path for plots, 'path/country/city'
    """

    degree_sign = "\N{DEGREE SIGN}"

    for frame in min_temperature:

        country, city = frame
        temp_dict = min_temperature[frame]

        ax = sns.lineplot(x=temp_dict.keys(), y=temp_dict.values())

        plt.xticks(ha="right", rotation=45)
        plt.subplots_adjust(bottom=0.25)

        ax.set_title("Minimum temperature daily values", fontsize=14)

        ax.set_xlabel("Date", fontsize=14)
        plt.xticks(fontsize=9)

        ax.set_ylabel(f"Temperature, {degree_sign}C", fontsize=14)
        plt.yticks(fontsize=12)

        fig = ax.get_figure()
        path_part = os.path.join(path, country)
        whole_path = os.path.join(path_part, city)
        os.makedirs(f"{whole_path}", exist_ok=True)
        file_path = os.path.join(whole_path, f"min_temperature_{city}")
        fig.savefig(f"{file_path}.png")
        plt.clf()


def graph_with_max_temperature(max_temperature, path):
    """
    Constructing plots for maximum daily temperature.
    :param max_temperature: dictionary key: date, value: maximum temperature
    :param path: path for plots, 'path/country/city'
    """

    degree_sign = "\N{DEGREE SIGN}"

    for frame in max_temperature:

        temp_dict = max_temperature[frame]
        country, city = frame

        ax = sns.lineplot(x=temp_dict.keys(), y=temp_dict.values())

        plt.xticks(ha="right", rotation=45)
        plt.subplots_adjust(bottom=0.25)

        ax.set_title("Maximum temperature daily values", fontsize=14)

        ax.set_xlabel("Date", fontsize=14)
        plt.xticks(fontsize=9)

        ax.set_ylabel(f"Temperature, {degree_sign}C", fontsize=12)
        plt.yticks(fontsize=12)

        fig = ax.get_figure()
        path_part = os.path.join(path, country)
        whole_path = os.path.join(path_part, city)
        os.makedirs(f"{whole_path}", exist_ok=True)
        file_path = os.path.join(whole_path, f"max_temperature_{city}")
        fig.savefig(f"{file_path}.png")
        plt.clf()
