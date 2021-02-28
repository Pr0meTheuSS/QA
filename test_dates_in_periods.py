import libs.tools as tools
import Sort.CheckSortMethods as Sort
from time import sleep
import pytest
from launch_param import *
"""
1. Вход с успешным логином
2. Выбор банка
3. Выбор закладку "Операции"
4. Установка дат
5. Выбор агрегатора и продукта
6. Проверка дат в таблице на соответствие заданному интервалу [date_start; date_end]
Result: Проверяем отсутствие данных в таблице с датой за пределами отрезка [date_start; date_end]
"""

@pytest.mark.parametrize(
    'browser, options, wait_time, base_url, login, password, bank_id, tab, date_start, date_end, col_name, aggregators, products',
    parameters_test_dates_in_periods)
def test_dates_in_periods(bank_id, tab, date_start, date_end, col_name,  aggregators, products,
                            browser_initialization_authorization):
    # Выбор банка, вкладки и установка даты
    tools.choose_the_bank(browser_initialization_authorization, bank_id)
    tools.choose_tab(browser_initialization_authorization, tab)
    tools.choose_dates(browser_initialization_authorization, date_start, date_end)
    # Выбор агрегатора и продукта
    tools.choose_aggregator(browser_initialization_authorization, aggregators, tab, 2)
    tools.choose_product(browser_initialization_authorization, products, tab)
    # Добавил ожидание на подгрузку данных таблицы
    sleep(2)
    assert tools.is_in_interval(Sort.date_list_generator(browser_initialization_authorization, col_name), date_start, date_end), "date is not " \
                                                                                                   "in interval"
