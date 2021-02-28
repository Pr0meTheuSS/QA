# Адреса комплексов
BASE_URL_TEST = "http://ahmad.ftc.ru:10483/rsp/login"

# Браузер для теста
browser = ["FireFox", "Chrome"]

# Время неявного ожидания
wait_time = 10

# Закладки
tab_name_str = ['История сверок', 'Операции', 'Файлы агрегатора', 'Реестры сверки']

""" 
    Параметры запуска теста test_pytest_example
    По порядку: 
        browser - из списка по индексу выбираем нужный браузер;
        options - параметры создания драйвера (в этом случае вкл/выкл графический режим); 
        wait_time - время неявного ожидания; 
        BASE_URL - адрес комплекса;
        login - логин; 
        password - пароль
"""
parameters = [(browser[0], "", wait_time, BASE_URL_TEST, "adm", "adm"),
              (browser[0], "--headless", wait_time, BASE_URL_TEST, "shift2", "12@#QWE3qwe!"),
              (browser[1], "--headless", wait_time, BASE_URL_TEST, "adm", "adm")]

""" 
    Параметры запуска теста test_dates_in_periods
    По порядку: 
        browser - из списка по индексу выбираем нужный браузер;
        options - параметры создания драйвера (в этом случае вкл/выкл графический режим); 
        wait_time - время неявного ожидания; 
        BASE_URL - адрес комплекса;
        login - логин; 
        password - пароль;
        bank_id - id банка;
        tab_name_str - закладка;
        date_start - начало периода;
        date_end - конец периода;
        aggregators - агрегаторы;
        product_text - продукты
"""
parameters_test_dates_in_periods = [
    (browser[0], "--headless", wait_time, BASE_URL_TEST, "adm", "adm", 'B001021', tab_name_str[1],
     '12.02.2009', '15.02.2021', 'Дата ЦУП', ['СБП НСПК'], ['Отчет по успешным операциям Банка Отправителя'])]

""" 
    Параметры запуска теста test_checkbutton_filters
    По порядку: 
        browser - из списка по индексу выбираем нужный браузер;
        options - параметры создания драйвера (в этом случае вкл/выкл графический режим); 
        wait_time - время неявного ожидания; 
        BASE_URL - адрес комплекса;
        login - логин; 
        password - пароль;
        bank_id - id банка;
        tab_name_str - закладка;
        date_start - начало периода;
        date_end - конец периода
        aggregators - список агрегаторов
        products - список продуктов
        checkbuttons - накладываемые checkbuttons фильтрыпо статусу сверки
"""
parameters_test_checkbutton_filters = [
    (browser[0], "--headless", wait_time, BASE_URL_TEST, "adm", "adm", 'B001021',
     tab_name_str[1], '12.02.2018', '15.02.2020', ['СБП НСПК'], ['Отчет по успешным операциям Банка Отправителя'],
     ['Нет документа СБП'])]

""" 
    Параметры запуска теста test_aggregator_and_product
    По порядку: 
        browser - из списка по индексу выбираем нужный браузер;
        options - параметры создания драйвера (в этом случае вкл/выкл графический режим); 
        wait_time - время неявного ожидания; 
        BASE_URL - адрес комплекса;
        login - логин; 
        password - пароль;
        bank - id банка;
        tab_name_str - закладка;
        date_start - начало периода;
        date_end - конец периода
        aggregators - список агрегаторов
        products - список продуктов

"""
parameters_test_aggregator_and_product = [(browser[0], "--headless", wait_time, BASE_URL_TEST, "adm", "adm", 'B001021',
                                          tab_name_str[1], '12.02.2018', '15.02.2020', ['СБП НСПК'],
                                          ['Отчет по успешным операциям Банка Отправителя'])]

""" 
    Параметры запуска теста test_sort_by_date
    По порядку: 
        browser - из списка по индексу выбираем нужный браузер;
        options - параметры создания драйвера (в этом случае вкл/выкл графический режим); 
        wait_time - время неявного ожидания; 
        BASE_URL - адрес комплекса;
        login - логин; 
        password - пароль;
        bank - id банка;
        tab_name_str - закладка;
        date_start - начало периода;
        date_end - конец периода
        col_name - имя колонки с сортируемыми датами
        sort_attemps_counter - количество попыток сортировки 
        aggregators - список агрегаторов
        products - список продуктов

"""
parameters_test_sort_by_date = [(browser[0], "--headless", wait_time, BASE_URL_TEST, "adm", "adm", 'B001021',
                                tab_name_str[1], '12.02.2018', '15.02.2020', 'Дата ЦУП', 7, ['СБП НСПК'],
                                ['Отчет по успешным операциям Банка Отправителя'])]
