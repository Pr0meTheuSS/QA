import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import libs.tools as tools
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

login = 'adm'
password = 'adm'
tab = 'Операции'
bank_id = 'B001021'
aggr = [ 'QIWI']
products = ['ИБ/МБ']
date_start = '27.12.2010'
date_end = '27.12.2020'


def create_operation_list(browser):
    """
    Функция для подготовки данных, инстанцирующих объект класса Operation
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


if __name__ == '__main__':
    """
    - https://jira.korona.net/browse/SHIFTLAB-1561
    1. Вход с успешным логином
    2. Выбор банка
    3. Выбор закладку "Операции"
    4. Установка дат
    5. Срез данных до наложения фильтров 
    6. Выбор агрегатора и продукта
    7. Проверка агрегатора и продукта по каждой операции
    Result: Проверка фильтра по агрегатору и продукту, вывод сообщения при наличии ошибки
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
        sleep(2)

        op_list_before_filter = create_operation_list(browser)

        match_counter: int = 0
        for op in op_list_before_filter:
            if op.aggregator in aggr and op.product in products:
                match_counter += 1
                op.print_info()
        # выбор агрегатора и продукта
        tools.choose_aggregator(browser, aggr, tab, 2)
        tools.choose_product(browser, products, tab)
        # Добавил ожидание на подгрузку данных таблицы
        sleep(2)
        # Костыль: проблема перекрытия данных таблицы другим объектом
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
        sleep(2)
        op_list_after_filter = create_operation_list(browser)
        assert len(op_list_after_filter) == match_counter, 'Data loss when filtering'

        for op in op_list_after_filter:
            if op.aggregator not in aggr or op.product not in products:
                print('Unexpected aggregator or product after filtration')
            op.print_info()

        tools.account_quit(browser)

    except Exception as ex:
        print(ex)

    finally:
        if args.debug:
            sleep(10)
        browser.quit()
