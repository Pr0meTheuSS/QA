import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import libs.tools as tools
import Sort.CheckSortMethods as Sort
from selenium.webdriver.firefox.webdriver import WebDriver

login = 'adm'
password = 'adm'
tab = 'Операции'
bank_id = 'B001021'
date_start = '27.12.2010'
date_end = '27.12.2020'
col_name = 'Дата ЦУП'
aggregators = ['СБП НСПК']
products = ['Отчет по успешным операциям Банка Отправителя']


if __name__ == '__main__':
    """
    - https://jira.korona.net/browse/SHIFTLAB-1561
    1. Вход с успешным логином
    2. Выбор банка
    3. Выбор закладку "Операции"
    4. Установка дат, выбор агрегатора и продукта
    5. Проверка дат в таблице на соответствие заданному интервалу [date_start; date_end]
    Result: Проверяем отсутствие данных в таблице с датой за пределами отрезка [date_start; date_end]
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
        # Выбор агрегатора и продукта
        tools.choose_aggregator(browser, aggregators, tab, 2)
        tools.choose_product(browser, products, tab)
        # Добавил ожидание на подгрузку данных таблицы
        sleep(2)
        assert Sort.is_in_interval(Sort.date_list_generator(browser, col_name), date_start, date_end), "date is not " \
                                                                                                       "in interval"
        tools.account_quit(browser)

    except Exception as ex:
        print(ex)

    finally:
        if args.debug:
            sleep(10)
        browser.quit()
