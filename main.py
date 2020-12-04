import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep
import libs.tools as tools


if __name__ == '__main__':
    """
    Методичка по selenium
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
    browser = webdriver.Firefox(options=opts)
    try:
        # На всякий случай чистим куки
        browser.delete_all_cookies()

        # Заходим на сайт
        browser.get('http://ahmad.ftc.ru:10483')

        # Ищем поле с логином и вводим логин
        browser.find_element_by_id('outlined-required').send_keys('adm')
        # Ищем поле с паролем и вводим пароль
        browser.find_element_by_id('outlined-password-input').send_keys('adm')
        # Выставлем фокус на поле с паролем и жмем Enter
        # TODO: зайти в АРМ по кнопе "ВХОД"
        browser.find_element_by_id('outlined-password-input').send_keys(Keys.ENTER)
        # Ждем пока прогрузится АРМ, на всякий случай
        sleep(3)

        # Ищем и печатаем на консоль текст из тела страницы для демонтрации
        elements_sp = browser.find_elements_by_tag_name('span')
        for element_sp in elements_sp:
            if element_sp.text != '':
                # Использую print из внешней библиотеки для примера
                tools.example_tool(element_sp.text)

        # Ищем выход
        i: int = 0
        buttons = browser.find_elements_by_tag_name('button')
        # Пока не придумал, как найти эту кнопку более красивым способом
        for element in buttons:
            i += True
            if i == 3:
                element.click()
        elements = browser.find_elements_by_tag_name('li')
        for element_li in elements:
            if element_li.text == 'Выход':
                element_li.click()
    finally:
        if args.debug:
            sleep(10)
        browser.quit()
