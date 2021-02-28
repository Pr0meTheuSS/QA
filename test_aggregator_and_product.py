import libs.tools as tools
import Sort.CheckSortMethods as Sort
import Operation_class as Operation
import pytest
from launch_param import *
from time import sleep
from selenium.webdriver.common.keys import Keys

"""
1. Вход с успешным логином
2. Выбор банка
3. Выбор закладку "Операции"
4. Установка дат
5. Срез данных до наложения фильтров 
6. Выбор агрегатора и продукта
7. Проверка агрегатора и продукта по каждой операции
Result: Проверка фильтра по агрегатору и продукту, вывод сообщения при наличии ошибки
"""


def create_operation_list(browser):
    """
    Функция для подготовки данных, инстанцирующих объекта класса Operation
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    :return: op_list  - список с данными-строками из окна информации об операции. Необходим для инициализации
    объекта класса Operation
    """
    op_list = []
    table = browser.find_element_by_tag_name('table')
    # Считываем строки таблицы
    rows = table.find_elements_by_tag_name('tr')

    if len(rows) == 0:
        return op_list

    for row in rows[1:]:
        if row.text != '':
            sleep(2)
            # открываем окно c информацией об операции
            row.find_element_by_tag_name('td').click()
            sleep(2)
            # Формируем список с данными для инициализации экземпляра класса Operation
            data_lst = Operation.get_operation_info(browser)
            # Закрываем окно с информацией
            browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

            if len(data_lst) != 0:
                op_list.append(Operation.Operation(data_lst))

    return op_list


@pytest.mark.parametrize(
    'browser, options, wait_time, base_url, login, password, bank_id, tab, date_start, date_end, aggregators, products',
    parameters_test_aggregator_and_product)
def test_aggregator_and_product(bank_id, tab, date_start, date_end, aggregators, products,
                                browser_initialization_authorization):
    # Выбор банка, вкладки и установка даты
    tools.choose_the_bank(browser_initialization_authorization, bank_id)
    tools.choose_tab(browser_initialization_authorization, tab)
    tools.choose_dates(browser_initialization_authorization, date_start, date_end)
    # Добавил ожидание на подгрузку данных таблицы
    sleep(2)
    op_list_before_filter = create_operation_list(browser_initialization_authorization)
    sleep(2)
    # Подсчитываем совпадения в таблице по продуктам и агрегаторам до их выбора
    match_counter: int = 0
    for op in op_list_before_filter:
        if op.aggr in aggregators and op.prod in products:
            match_counter += 1
            op.print_info()

    # Выбор агрегатора и продукта
    tools.choose_aggregator(browser_initialization_authorization, aggregators, tab, 2)
    tools.choose_product(browser_initialization_authorization, products, tab)
    # Добавил ожидание на подгрузку данных таблицы
    sleep(2)
    # Костыль: проблема перекрытия данных таблицы другим объектом
    browser_initialization_authorization.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
    sleep(2)
    op_list_after_filter = create_operation_list(browser_initialization_authorization)
    assert len(op_list_after_filter) == match_counter, 'Data loss when filtering'

    for op in op_list_after_filter:
        assert op.aggr in aggregators and op.prod in products, 'Unexpected aggregator or product after filtration'
