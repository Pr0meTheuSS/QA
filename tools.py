"""
Библиотеки для тестов
"""
from selenium.webdriver.common.keys import Keys
from time import sleep


def authentication(browser, login='adm', password='adm'):
    # для использования допустимы вызовы :
    # authentication(browser) - вход под предустановленным данным login :adm, password:adm
    # authentication(browser, 'your_login', 'your_password') - вход по констанотным строкам
    # authentication(browser, login_str, pass_str) - вход с передачей переменных-строк с логином и паролем

    # Ищем поле с логином и вводим логин
    browser.find_element_by_id('outlined-required').send_keys(login)
    # Ищем поле с паролем и вводим пароль
    browser.find_element_by_id('outlined-password-input').send_keys(password)
    # Выставлем фокус на поле с паролем и жмем Enter
    browser.find_element_by_id('outlined-password-input').send_keys(Keys.ENTER)
    # Ждем пока прогрузится АРМ, на всякий случай
    sleep(3)


def choose_the_bank(brows, bank_id):
    # для использования допустимы вызовы :
    # choose_the_bank(brows, bank_id) - выбор банка с передачей переменной-строкой bank_id
    # choose_the_bank(brows, 'B001021') - выбор банка с передачей константы-строки

    # Элемент с id банков
    input_bank = brows.find_element_by_css_selector('div.MuiAutocomplete-root>div>div>input')
    input_bank.send_keys(bank_id)
    input_bank.send_keys(Keys.DOWN)
    input_bank.send_keys(Keys.ENTER)
    sleep(3)


def choose_dates(browser, date_from, date_to):
    # Кристина, спасибо большое!!!
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


def account_quit(brows):
    # Ищем выход
    t: int = 0
    buttons = brows.find_elements_by_tag_name('button')
    # Пока не придумал, как найти эту кнопку более красивым способом
    for element in buttons:
        t += True
        if t == 3:
            element.click()
    elements = brows.find_elements_by_tag_name('li')
    for element_li in elements:
        if element_li.text == 'Выход':
            element_li.click()


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
