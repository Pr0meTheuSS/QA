import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import libs.tools as tools
import Sort.CheckSortMethods as Sort
from selenium.webdriver.firefox.webdriver import WebDriver
import pandas as pd

login = 'adm'
password = 'adm'
tab = 'Операции'
bank_id = 'B001021'
date_start = '27.12.2010'
date_end = '27.12.2020'
col_name = 'Дата ЦУП'
sort_attempts_counter = 7
aggregators = ['СБП НСПК']
products = ['Отчет по успешным операциям Банка Отправителя']


if __name__ == '__main__':
    '''
    - https://jira.korona.net/browse/SHIFTLAB-1561
    1. Вход с успешным логином
    2. Выбор банка
    3. Выбор закладку "Операции"
    4. Установка дат
    5. Выбор агрегатора (-ов)
    6. Формирование датафреймов
    7. Проверка инварианта сортировки (содержимого таблицы)
    8. Проверка наличия упорядоченности
    9. При повторных сортировках - проверка изменения упорядоченности 
    Result: Проверяем сохранение инварианта сортировки, упорядоченность и изменение упорядоченности 
            при повторных сортировках
    '''
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

        # Выбрать Агрегатора
        tools.choose_aggregator(browser, aggregators, tab, 2)
        tools.choose_product(browser, products, tab)

        sorted_date_list = []
        lst_df_to_check_invariant = []

        for t in range(sort_attempts_counter):
            if t > 0:
                tools.click_sort(browser, col_name)
                sleep(2)
            # Пополняем лист датафреймом для последующей проверки содержимого всех фреймов относительно нулевого
            lst_df_to_check_invariant.append(pd.read_html(browser.page_source, index_col=0))
            # Собираем лист с таблицами дат в колонке с именем col_name - их и будем проверять на упорядоченность
            sorted_date_list.append(Sort.date_list_generator(browser, col_name))

        # Проверка сортировки sort_attempts_counter раз на инвариант содержимого, упорядоченность и её изменение
        for it in range(1, sort_attempts_counter):

            # Если не сохранено состояние данных таблицы после очередной сортировки
            if not Sort.sort_invariant(lst_df_to_check_invariant[0], lst_df_to_check_invariant[it]):
                print(f"Sort number {it}: invariant violated!")

            # Если данные после первой сортировки не упорядочены ни по невозрастанию, ни по неубыванию
            if not Sort.is_ascending(sorted_date_list[it]) and not Sort.is_descending(sorted_date_list[it]):
                print(f"Sort number {it}: data was not sorted!")

            if 1 < it <= sort_attempts_counter:
                # Если после очередной сортировки упорядоенность данных не изменилась
                if Sort.is_ascending(sorted_date_list[it - 1]) and not Sort.is_descending(sorted_date_list[it]) or \
                       Sort.is_descending(sorted_date_list[it - 1]) and not Sort.is_ascending(sorted_date_list[it]):
                    print(f"error : trying to sort a {it} time does not change the sort order!")

        tools.account_quit(browser)

    except Exception as ex:
        print(ex)

    finally:
        if args.debug:
            sleep(10)
        browser.quit()
