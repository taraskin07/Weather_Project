from project_scripts.post_processing import (
    find_day_and_city_with_max_temperature,
    find_city_with_max_difference_in_max_temperature,
    find_day_and_city_with_min_temperature,
    find_day_and_city_with_max_difference_in_temperature,
)


def test_post_processing():
    min_temperature = {
        ("AT", "Vienna"): {
            "2021-06-30": 18.52,
            "2021-07-01": 15.06,
            "2021-07-02": 14.39,
            "2021-07-03": 15.81,
            "2021-07-04": 16.61,
            "2021-07-05": 17.22,
            "2021-07-06": 16.79,
            "2021-07-07": 19.78,
            "2021-07-08": 21.04,
            "2021-07-09": 17.81,
        }
    }
    max_temperature = {
        ("AT", "Vienna"): {
            "2021-06-30": 31.68,
            "2021-07-01": 23.6,
            "2021-07-02": 22.48,
            "2021-07-03": 17.8,
            "2021-07-04": 27.23,
            "2021-07-05": 26.5,
            "2021-07-06": 33.58,
            "2021-07-07": 35.19,
            "2021-07-08": 36.98,
            "2021-07-09": 31,
        }
    }
    a = find_day_and_city_with_max_temperature(max_temperature)["Температура"].iloc[0]
    b = find_city_with_max_difference_in_max_temperature(max_temperature)[
        "Изменение температуры"
    ].iloc[0]
    c = find_day_and_city_with_min_temperature(min_temperature)["Температура"].iloc[0]
    d = find_day_and_city_with_max_difference_in_temperature(
        max_temperature, min_temperature
    )["Разница температур"].iloc[0]

    assert a == 36.98
    assert b == 19.18
    assert c == 14.39
    assert d == 16.79
