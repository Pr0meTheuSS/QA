from time import sleep
import libs.tools as tools
import Sort.CheckSortMethods as Sort
import pandas as pd
import pytest
from launch_param import *

'''
1. Вход с успешным логином
2. Выбор банка
3. Выбор закладки "Операции"
4. Установка дат
5. Выбор агрегатора (-ов) и продукта (-ов)
6. Формирование датафреймов
7. Проверка инварианта сортировки (содержимого таблицы)
8. Проверка монотонности дат
9. При повторных сортировках - проверка изменения упорядоченности
Result: Проверяем сохранение инварианта сортировки, монотонность и изменение упорядоченности
        при повторных сортировках
'''


@pytest.mark.parametrize(
    'browser, options, wait_time, base_url, login, password, bank_id, tab, date_start, date_end, col_name, sort_attempts_counter, aggregators, products',
    parameters_test_sort_by_date)
def test_dates_in_periods(bank_id, tab, date_start, date_end, col_name, sort_attempts_counter, aggregators, products,
                          browser_initialization_authorization):
    # Выбор банка, вкладки и установка даты
    tools.choose_the_bank(browser_initialization_authorization, bank_id)
    tools.choose_tab(browser_initialization_authorization, tab)
    tools.choose_dates(browser_initialization_authorization, date_start, date_end)
    # Выбор агрегатора и продукта
    tools.choose_aggregator(browser_initialization_authorization, aggregators, tab, 2)
    tools.choose_product(browser_initialization_authorization, products, tab)

    sorted_date_list = []
    lst_df_to_check_invariant = []

    for t in range(sort_attempts_counter):
        if t > 0:
            tools.click_sort(browser_initialization_authorization, col_name)
            sleep(2)
        # Пополняем лист датафреймом для последующей проверки содержимого всех фреймов относительно нулевого
        lst_df_to_check_invariant.append(pd.read_html(browser_initialization_authorization.page_source, index_col=0))
        # Собираем лист с таблицами дат в колонке с именем col_name - их и будем проверять на монотонность
        sorted_date_list.append(Sort.date_list_generator(browser_initialization_authorization, col_name))

    # Проверка сортировки sort_attempts_counter - 1 раз на инвариант содержимого, упорядоченность и её изменение
    for it in range(1, sort_attempts_counter):

        # Если не сохранено состояние данных таблицы после очередной сортировки(потеря данных)
        assert Sort.sort_invariant(lst_df_to_check_invariant[0],
                                   lst_df_to_check_invariant[it]), f"Sort number {it}: invariant violated!"

        # Если данные после первой сортировки не монотонны
        assert (Sort.is_ascending(sorted_date_list[it]) or Sort.is_descending(
            sorted_date_list[it])), f"Sort number {it}: data was not sorted!"

        if 1 < it <= sort_attempts_counter:
            # Если после очередной сортировки упорядоенность данных не изменилась
            assert Sort.is_ascending(sorted_date_list[it - 1]) and Sort.is_descending(sorted_date_list[it]) or \
                   Sort.is_descending(sorted_date_list[it - 1]) and Sort.is_ascending(
                sorted_date_list[it]), f"error : trying to sort a {it} time does not change the sort order!"
