import csv
import re
import locale


def get_data():
    files = ["info_1.txt", "info_2.txt", "info_3.txt"]  # указываем файлы для чтения
    search_parameters = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []  # в данных списках данные собраны по типу
    general_lists = [os_prod_list, os_name_list, os_code_list, os_type_list]
    main_data = []  # в данном списке данные будут храниться построчно
    main_data.append(search_parameters)
    for file in files:
        with open(file, encoding="cp1251") as f:
            lines = f.read()
            for num, param in enumerate(search_parameters):
                parameter = re.search(f"{param}:(.+)", lines)[1]  # ищем нужные параметры
                general_lists[num].append(parameter.strip())
    [main_data.append(list(i)) for i in zip(os_prod_list, os_name_list, os_code_list, os_type_list)]
    return main_data


def write_to_csv(name):

    locale.setlocale(locale.LC_ALL, "")  # без этих 2 строк в exel пишет все в один столбик
    DELIMITER = ";" if locale.localeconv()["decimal_point"] == "," else ","

    with open(f"{name}.csv", "w", newline="") as f_n:
        f_n_writer = csv.writer(f_n, delimiter=DELIMITER)
        f_n_writer.writerows(get_data())


if __name__ == "__main__":
    write_to_csv("task_1")  # задаем имя без расширения
    with open("task_1.csv") as f_n:
        print(f_n.read())
