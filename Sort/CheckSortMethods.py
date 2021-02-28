import pandas as pd
import datetime


def sort_invariant(orig_df, unverified_df):
    keys = orig_df[0].keys()
    orig_str_list = []
    unverified_str_list = []
    # Собираем список строк из таблицы
    for index in range(len(orig_df[0].dropna())):
        temp_str = ''
        for k in keys:
            temp_str += str(orig_df[0][k][index]) + ' '
        orig_str_list.append(temp_str)
    # Собираем список строк из таблицы
    for index in range(len(unverified_df[0].dropna())):
        temp_str = ''
        for k in keys:
            temp_str += str(unverified_df[0][k][index]) + ' '
        unverified_str_list.append(temp_str)

    return not (set(orig_str_list) ^ set(unverified_str_list))


def is_descending(date_list: list):
    for i in range(len(date_list) - 1):
        if date_list[i] < date_list[i + 1]:
            return False
    return True


def is_ascending(date_list: list):
    for i in range(len(date_list) - 1):
        if date_list[i] > date_list[i + 1]:
            return False
    return True


def is_dataframe_empty(df):
    return bool(df[0].dropna().shape[0] == 1)


def date_list_generator(browser, col_name):
    """
    Функция получения списка с датами, представленными типом datetime, из таблицы с данными по имени столбца
    :param browser: объект, возвращаемый функцией webdriver.Firefox(options=opts)
    :param col_name: имя колонки с датами, по содержимому которой необходимо получить список дат типа datetime
    :return:
    """
    # Читаем данные из таблицы
    dataframe = pd.read_html(browser.page_source)
    # Если таблица пуста - выбрасываем исключение
    if is_dataframe_empty(dataframe):
        raise Exception("Empty dataframe")

    date_list = []
    # В таблице по имени столбца(например, в столбце 'Дата ЦУП') получаем список с датами и временем
    for line in dataframe[0][col_name].dropna():
    # Для каждой строки с датой и временем производим разбиение и прведение к типу datetime, добавляем к списку дат
        date = line.split(' ')[0]
        time = line.split(' ')[1]
        date_lst = date.split('-')
        time_lst = time.split(':')
        d = datetime.datetime(int(date_lst[2], 10), int(date_lst[1], 10), int(date_lst[0], 10),
                              int(time_lst[0], 10), int(time_lst[1], 10), int(time_lst[2], 10))
        date_list.append(d)
    return date_list
