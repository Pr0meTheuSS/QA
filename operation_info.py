import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import Operation_class as Operation
import libs.tools as tools
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
import Sort.CheckSortMethods as Sort
import pandas as pd

login = 'adm'
password = 'adm'
tab = 'Операции'
bank_id = 'B001021'
date_start = '27.12.2010'
date_end = '27.12.2020'


if __name__ == '__main__':
    """
    - https://jira.korona.net/browse/SHIFTLAB-1561
    1. Вход с успешным логином
    2. Выбор банка
    3. Выбор закладку "Операции"
    4. Установка дат
    5. Вывод информации об операциях в таблице
    Result: Вывод данных
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
        # выбор агрегатора и продукта
        tools.choose_aggregator(browser, ['QIWI'], tab, 2)
        tools.choose_product(browser, ['ИБ/МБ'], tab)

        # Добавил ожидание на подгрузку данных таблицы
        sleep(2)
        table = browser.find_element_by_tag_name('table')
        # Считываем строки таблицы
        rows = table.find_elements_by_tag_name('tr')
        # Если таблица не пуста
        if not Sort.is_dataframe_empty(pd.read_html(browser.page_source, index_col=0)):
            for row in rows[1:]:
                if row.text != '':
                    # открываем окно c информацией об операции
                    row.find_element_by_tag_name('td').click()
                    sleep(2)
                    op = Operation.Operation(Operation.get_operation_info(browser))
                    op.print_info()
                    # Закрываем окно с информацией
                    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
                    sleep(2)
        else:
            print('Table is empty')

        tools.account_quit(browser)

    except Exception as ex:
        print(ex)

    finally:
        if args.debug:
            sleep(10)
        browser.quit()
