"""
Библиотеки для тестов
"""
from selenium.webdriver.common.keys import Keys
from time import sleep
import datetime


def authentication(browser, login='adm', password='adm'):
    """
    Функция входа в АРМ
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    :param login:  константа-строка ( like 'shift') или переменная-строка, по дефолту - 'adm'
    :param password: константа-строка ( like 'shift') или переменная-строка, по дефолту - 'adm'
    :return: void
    """
    # Ищем поле с логином и вводим логин
    browser.find_element_by_id('outlined-required').send_keys(login)
    # Ищем поле с паролем и вводим пароль
    browser.find_element_by_id('outlined-password-input').send_keys(password)
    # Выставлем фокус на поле с паролем и жмем Enter
    browser.find_element_by_id('outlined-password-input').send_keys(Keys.ENTER)
    # Ждем пока прогрузится АРМ, на всякий случай
    sleep(3)


def choose_the_bank(browser, bank_id):
    """
    Функция выбора id банка
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    :param bank_id: выбор банка с передачей константы-строки ( like 'B001021') или переменной-строки
    :return: void
    """
    # Элемент с id банков
    input_bank = browser.find_element_by_css_selector('div.MuiAutocomplete-root>div>div>input')
    input_bank.send_keys(bank_id)
    input_bank.send_keys(Keys.DOWN)
    input_bank.send_keys(Keys.ENTER)
    sleep(3)


def choose_tab(browser, tab_name_str):
    """
    Функция выбора закладки
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    :param tab_name_str: строка с именем закладки
    :return: void
    """
    elements_sp = browser.find_elements_by_tag_name('span')
    for element_sp in elements_sp:
        if element_sp.text == tab_name_str:
            element_sp.click()
            break


def choose_dates(browser, date_from, date_to):
    """
    Функция выбора временного периода
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    :param date_from: выбор начала периода с передачей константы-строки(в формате 'dd.mm.yyyy') или переменной-строки
    :param date_to: выбор конца периода с передачей константы-строки(в формате 'dd.mm.yyyy') или переменной-строки
    :return: void
    """
    text_boxes = browser.find_elements_by_css_selector('input[type="text"]')
    # Удаляем значение поля "Начало периода", выставленное по умолчанию
    text_boxes[1].clear()
    # Вводим дату в поле "Начало периода"
    text_boxes[1].send_keys(date_from)
    # Жмем Enter
    text_boxes[1].send_keys(Keys.ENTER)
    # Удаляем значение поля "Конец периода", выставленное по умолчанию
    text_boxes[2].clear()
    # Вводим дату в поле "Конец периода"
    text_boxes[2].send_keys(date_to)
    # Жмем Enter
    text_boxes[2].send_keys(Keys.ENTER)


def choose_aggregator(browser, aggregators: list, tab_name_str, method):
    """
    Функция выбора агрегатора
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    :param aggregators: выбор агрегаторов, данные в виде list (список), пример: ['ABS', 'QIWI']
    :param tab_name_str: выбор закладки с передачей константы-строки ( like 'Операции') или переменной-строки
    :param method: выбор способа сделать поле "Агреготоры" неактивным
    (1 - кликнуть в любое место страницы, 2 - нажать клавишу Ecs)
    :return: void
    """
    if tab_name_str == 'История сверок':
        browser.find_element_by_xpath('//body/div[1]/div/div[2]/main/div/div[1]/div/div/div[2]').click()
    if tab_name_str == 'Операции':
        browser.find_element_by_xpath('//body/div[1]/div/div[2]/main/div/div[1]/div[3]').click()
    if tab_name_str == 'Файлы агрегатора' or tab_name_str == 'Реестры сверки':
        browser.find_element_by_xpath('//body/div[1]/div/div[2]/main/div/div[1]/div[2]').click()
    # Выбор агрегатора
    for aggregator in aggregators:
        if aggregator == 'QIWI':
            browser.find_element_by_xpath('//li[1]').click()
        if aggregator == 'СБП НСПК':
            browser.find_element_by_xpath('//li[2]').click()
        if aggregator == 'ABS':
            browser.find_element_by_xpath('//li[3]').click()
        if aggregator == 'НКО':
            browser.find_element_by_xpath('//li[4]').click()
        if aggregator == 'CyberPlat':
            browser.find_element_by_xpath('//li[5]').click()
        if aggregator == 'ОЧЛ-ОМСК':
            browser.find_element_by_xpath('//li[6]').click()
    # Способы сделать поле "Агреготоры" неактивным
    if method == 1:
        browser.find_element_by_xpath('//body/div[3]/div[1]').click()
    elif method == 2:
        browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    sleep(1)


def choose_product(browser, products: list, tab_name_str):
    """
    Функция выбора продукта
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    :param products: выбор продуктов, данные в виде list (список), пример: ['ИБ/МБ', 'ОЧЛ_ОМСК']
    :param tab_name_str: выбор закладки с передачей константы-строки ( like 'Операции') или переменной-строки
    :return: void
    """
    if tab_name_str == 'История сверок':
        browser.find_element_by_xpath('//body/div[1]/div/div[2]/main/div/div[1]/div/div/div[3]').click()
    if tab_name_str == 'Операции':
        browser.find_element_by_xpath('//body/div[1]/div/div[2]/main/div/div[1]/div[4]').click()
    if tab_name_str == 'Файлы агрегатора' or tab_name_str == 'Реестры сверки':
        browser.find_element_by_xpath('//body/div[1]/div/div[2]/main/div/div[1]/div[3]').click()
    # Выбор продукта
    lis = browser.find_elements_by_tag_name('li')
    for el_li in lis:
        if el_li.text in products:
            el_li.click()
    # Сделать "Продукт" неактивным
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    sleep(1)


def is_in_interval(date_list, left_date: str, right_date: str):
    """
    Функция проверки даты на принадлежность интервалу
    :param date_list: список с проверяемыми датами в формате datetime
    :param left_date: дата - левая граница (в формате строки)
    :param right_date:: дата - правая граница (в формате строки)
    :return: boolean (True or False)
    """
    # Получаем лист со значениями dd mm yyyy и привели значения к типу datetime
    left_lst = left_date.split('.')
    left = datetime.datetime(int(left_lst[2], 10), int(left_lst[1], 10), int(left_lst[0], 10), 0, 0, 0)

    right_lst = right_date.split('.')
    right = datetime.datetime(int(right_lst[2], 10), int(right_lst[1], 10), int(right_lst[0], 10), 23, 59, 59)

    # Для каждого значения в списке дат проверяем принадлежность отрезку [left;right]
    for cur_date in date_list:
        if not (left <= cur_date <= right):
            return False
    return True


def account_quit(browser):
    """
    Выход из АРМ
    :param browser: объект, возвращаемый методом webdriver.Firefox()
    """
    # Ищем выход
    t: int = 0
    buttons = browser.find_elements_by_tag_name('button')
    # Пока не придумал, как найти эту кнопку более красивым способом
    for element in buttons:
        t += True
        if t == 3:
            element.click()
    elements = browser.find_elements_by_tag_name('li')
    for element_li in elements:
        if element_li.text == 'Выход':
            element_li.click()


def click_sort(browser, col_name):
    # Кликаем на спан c именем col_name для сортировки
    spans = browser.find_elements_by_css_selector('tr>th>span')
    for el in spans:
        if el.text == col_name:
            el.click()


def example_tool(example):
    print(example)


def find_elements_in_pages_debug(elements: list):
    """
    Вывод на консоль значений элементов на странице при вызове функции find_elements_*
    :param elements: Список элементов
    """
    for element in elements:
        print(f'Tag name: {element.tag_name}')
        print(f'Text: {element.text}')
        print(f'Location: {element.location}')
        print(f'Location once scrolled into view: {element.location_once_scrolled_into_view}',
              end='\n-----------------------------\n')
