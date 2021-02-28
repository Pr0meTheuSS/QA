import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep


# Декоратор который говорит о том что функция ниже - фикстура
@pytest.fixture()
def browser_initialization(browser, options, wait_time):
    """
    Фикстура на инициализацию браузера
    :param browser - из списка по индексу выбираем нужный браузер;
    :param options - параметры создания драйвера (в этом случае вкл/выкл графический режим);
    :param wait_time - время неявного ожидания
    """

    # В зависимости от того, какой браузер будет среди набора параметров, выберем нужный драйвер
    if browser == "FireFox":
        # Инициализируем браузер Firefox и передадим ему options
        opt = Options()
        opt.add_argument(options)
        driver = webdriver.Firefox(options=opt)
    else:
        # Если браузер не распознан, вернем исключение
        raise Exception(f'"{browser}" does not support')
    # Неявное ожидание. В течение указанного времени будет искаться элемент, если он не будет доступен сразу
    driver.implicitly_wait(wait_time)
    # На всякий случай чистим куки
    driver.delete_all_cookies()
    # Возвращаем объект браузера после инициализации
    yield driver
    # Чистим за собой после того как объект нам больше не нужен
    driver.quit()


@pytest.fixture()
def browser_initialization_authorization(browser, options, wait_time, base_url, login, password):
    """
    Фикстура на инициализацию браузера, авторизацию и вход в АРМ
    :param browser - из списка по индексу выбираем нужный браузер;
    :param options - параметры создания драйвера (в этом случае вкл/выкл графический режим);
    :param wait_time - время неявного ожидания;
    :param base_url - адрес АРМа;
    :param login - логин;
    :param password - пароль
    """

    # В зависимости от того, какой браузер будет среди набора параметров, выберем нужный драйвер
    if browser == "FireFox":
        # Инициализируем браузер Firefox и передадим ему options
        opt = Options()
        opt.add_argument(options)
        driver = webdriver.Firefox(options=opt)
    else:
        # Если браузер не распознан, вернем исключение
        raise Exception(f'"{browser}" does not support')
    # Неявное ожидание. В течение указанного времени будет искаться элемент, если он не будет доступен сразу
    driver.implicitly_wait(wait_time)
    # На всякий случай чистим куки
    driver.delete_all_cookies()
    # Заходим на сайт
    driver.get(base_url)
    # Ищем поле с логином и вводим логин
    driver.find_element_by_id('outlined-required').send_keys(login)
    # Ищем поле с паролем и вводим пароль
    driver.find_element_by_id('outlined-password-input').send_keys(password)
    # Выставлем фокус на поле с паролем и жмем Enter
    driver.find_element_by_id('outlined-password-input').send_keys(Keys.ENTER)
    sleep(2)
    # Проверим по url что мы прошли авторизацию и видим дашборд
    assert driver.current_url == "http://ahmad.ftc.ru:10483/rsp/dashboard/empty"
    # Возвращаем объект браузера после инициализации
    yield driver
    # Чистим за собой после того как объект нам больше не нужен
    driver.quit()
