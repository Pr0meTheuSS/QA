import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import libs.tools as tools
from selenium.webdriver.firefox.webdriver import WebDriver
import pandas as pd

login = 'adm'
password = 'adm'
tab = 'Операции'
bank_id = 'B001021'
date_start = '27.12.2010'
date_end = '27.12.2020'
aggregators = ['СБП НСПК']
products = ['Отчет по успешным операциям Банка Отправителя']
checkbutton = ['Нет документа СБП']
col_name = 'Статус сверки'


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


if __name__ == '__main__':
    """
    - https://jira.korona.net/browse/SHIFTLAB-1561
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
    # Обрабатываем входящие аргументы при запуске теста
    parser = argparse.ArgumentParser(description='Тестируем WEB-АРМ при помощи библиотеки Selenium')
    parser.add_argument('-d', '--debug', action='store_true', help='Выставить режим отладки')
    args = parser.parse_args()

    # Включаем графический режим драйвера Firefox в режиме отладки
    opts = Options()
    if not args.debug:
        opts.add_argument('--headless')

    # Инициализируем браузер Firefox
    browser: WebDriver = webdriver.Firefox(options=opts)
    browser.implicitly_wait(5)

    try:
        # На всякий случай чистим куки
        browser.delete_all_cookies()
        # Заходим на сайт
        browser.get('http://ahmad.ftc.ru:10483')

        tools.authentication(browser, login, password)

        # Выбор банка, вкладки и установка даты
        tools.choose_the_bank(browser, bank_id)
        tools.choose_tab(browser, tab)
        tools.choose_dates(browser, date_start, date_end)

        # Выбор Агрегатора
        tools.choose_aggregator(browser, aggregators, tab, 2)
        # Выбор Продукта
        tools.choose_product(browser, products, tab)
        # Сбрасываем фильтрацию по датам агрегатора
        browser.find_element_by_xpath("//span[text()='Дата агрегатора']").click()
        # Двойной клик по checkbutton "Все статусы" для снятия всех фильтров
        browser.find_element_by_xpath("//input[@value='Все']").click()
        sleep(2)
        if browser.find_element_by_xpath("//input[@value='Все']").is_selected():
            browser.find_element_by_xpath("//input[@value='Все']").click()
        sleep(2)

        if not Sort.is_dataframe_empty(pd.read_html(browser.page_source, index_col=0)):
            print('no filters applied, but the table is not empty')

        # Кликаем на спаны в списке checkbutton
        for btn in checkbutton:
            sleep(2)
            path = "//span[text()='" + btn + "']"
            browser.find_element_by_xpath(path).click()

        assert check_reconciliation_status(browser, checkbutton), "error of filtration"
        sleep(2)
        while click_next_page(browser):
            assert check_reconciliation_status(browser, checkbutton), "error of filtration"
            sleep(2)

        tools.account_quit(browser)
    finally:
        if args.debug:
            sleep(10)
        browser.quit()
