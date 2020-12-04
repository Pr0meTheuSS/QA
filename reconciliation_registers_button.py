import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import libs.tools as tools

format_table = ['',
                'Дата сверки:',
                'Номер сверки:',
                'Название файла:',
                'Сумма:',
                'Количество:',
                'Статус:',
                'Сумма расхождений:',
                'Количество расхождений:'
                ]
len_f_table = len(format_table)

if __name__ == '__main__':
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
        # логинимся
        tools.authentication(browser, 'shift1', '123qwe!@#QWE1')
        # выбираем id банка
        tools.choose_the_bank(browser, 'B001021')
        # клик на кнопку 'Реестры сверки'
        elements_sp = browser.find_elements_by_tag_name('span')
        for element_sp in elements_sp:
            if element_sp.text == 'Реестры сверки':
                element_sp.click()
                break
        # выбираем временной период
        tools.choose_dates(browser, '20.12.2019', '04.12.2020')

        # Чтение полей из таблицы
        td_elements = browser.find_elements_by_tag_name('td')

        i: int = 0
        # t - номер строки (если полей оказывается меньше, чем предполагается в format_table - цикл пропускается)
        for t in range(len(td_elements) // (len_f_table - 1)):
            # i  - номер столбца, обрабатываемго в t-ой строке
            for i in range(len_f_table):
                # Пропускаем первый столбец, тк он не содержит информации
                if td_elements[i + t * len_f_table].get_attribute('value') != '' and i in range(1,
                                                                                                len(format_table) - 1):
                    print(format_table[i] + ' ' + str(td_elements[i + t * len_f_table].get_attribute('value')) + ' ')
                i += 1

        # Выход из аккаунта
        tools.account_quit(browser)

    finally:
        if args.debug:
            sleep(10)
        browser.quit()
