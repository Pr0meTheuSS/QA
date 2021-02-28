import libs.tools as tools
import Sort.CheckSortMethods as Sort
from time import sleep
import pytest
from launch_param import *
import pandas as pd

"""
1. Вход с успешным логином
2. Выбор банка
3. Выбор закладку "Операции"
4. Установка дат
5. Выбор агрегатора (-ов) и продукта (-ов)
6. Сброс всех фильтров и проверка таблицы(ожидается пустая страница)
7. Наложение фильтров из списка checkbuttons
8. Проверка таблицы на соответствие статусов сверки данным из списка checkbuttons
Result: Проверяем соответствие полей наложенным фильтрам  
"""


def check_reconciliation_status(browser,  checkbutton: list):
    """
    Функция проверки совпадения статуса сверки в таблице с наложенными checkbutton фильтрами
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    :param checkbutton:  список налагаемых фильтров (like 'Без документа СБП')
    :return: True - если все статусы сверки в таблице принадлежат списку checkbutton, False - иначе
    """
    df = pd.read_html(browser.page_source, index_col=0)
    df = df[0].dropna(how='all')
    for status in df['Статус сверки']:
        if status not in checkbutton:
            return False
    return True


def click_next_page(browser):
    """
    Функция перехода на следующую страницу таблицы
    :param browser:
    :return: boolean : False, если уже открыта последняя страница таблицы с данными, True - иначе
    """
    next_page_button = browser.find_element_by_xpath('//button[@aria-label="Следующая страница"]')
    if next_page_button.get_attribute('tabindex') == "-1":
        return False
    next_page_button.click()
    return True


@pytest.mark.parametrize(
    'browser, options, wait_time, base_url, login, password, bank_id, tab, date_start, date_end, aggregators, '
    'products, checkbuttons',
    parameters_test_checkbutton_filters)
def test_checkbutton_filters(bank_id, tab, date_start, date_end, aggregators, products, checkbuttons,
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

    # Сбрасываем фильтрацию по датам агрегатора
    if browser_initialization_authorization.find_element_by_xpath("//input[@value='agg']").is_selected():
        browser_initialization_authorization.find_element_by_xpath("//input[@value='agg']").click()
    # Сбрасываем фильтрацию по датам ЦУП
    if browser_initialization_authorization.find_element_by_xpath("//input[@value='pcc']").is_selected():
        browser_initialization_authorization.find_element_by_xpath("//input[@value='pcc']").click()

    # Двойной клик по checkbutton "Все статусы" для снятия всех фильтров
    browser_initialization_authorization.find_element_by_xpath("//input[@value='Все']").click()
    sleep(2)
    if browser_initialization_authorization.find_element_by_xpath("//input[@value='Все']").is_selected():
        browser_initialization_authorization.find_element_by_xpath("//input[@value='Все']").click()
    sleep(2)

    assert Sort.is_dataframe_empty(pd.read_html(browser_initialization_authorization.page_source, index_col=0)), \
        'no filters applied, but the table is not empty '

    # Кликаем на спаны в списке checkbuttons
    for btn in checkbutton:
        sleep(2)
        path = "//span[text()='" + btn + "']"
        browser_initialization_authorization.find_element_by_xpath(path).click()

    assert check_reconciliation_status(browser_initialization_authorization, checkbuttons), "error of filtration"
    sleep(2)
    while click_next_page(browser_initialization_authorization):
        assert check_reconciliation_status(browser_initialization_authorization, checkbuttons), "error of filtration"
        sleep(2)
