from selenium import webdriver


class Operation:
    def __init__(self, operation_info_lst: list):
        """
        :param operation_info_lst: Список строк, собираемый методом get_operation_info
        """
        if len(operation_info_lst) != 0:
            self.reconciliation_status = operation_info_lst[1]
            self.aggr = operation_info_lst[3]
            self.prod = operation_info_lst[5]
            self.pcc_reconciliation_number = operation_info_lst[7]
            self.aggr_reconciliation_number = operation_info_lst[8]
            self.pcc_operation_status = operation_info_lst[10]
            self.aggr_operation_status = operation_info_lst[11]
            self.pcc_aggr_file = operation_info_lst[13]
            self.aggr_aggr_file = operation_info_lst[14]
            self.pcc_operation_date = operation_info_lst[16]
            self.aggr_operation_date = operation_info_lst[17]
            self.pcc_operation_sum = operation_info_lst[19]
            self.aggr_operation_sum = operation_info_lst[20]

    def print_info(self):
        print('======OPERATION_INFO======')
        print("Статус сверки: " + self.reconciliation_status)
        print("Агрегатор: " + self.aggr)
        print("Продукт:" + self.prod)
        print("Номер операции по данным ЦУП:" + self.pcc_reconciliation_number)
        print("Номер операции по данным Агрегатора:" + self.aggr_reconciliation_number)
        print("Статус операции по данным ЦУП:" + self.pcc_operation_status)
        print("Статус операции по данным Агрегатора:" + self.aggr_operation_status)
        print("Файл агрегатора по данным ЦУП:" + self.pcc_aggr_file)
        print("Файл агрегатора по данным Агрегатора:" + self.aggr_aggr_file)
        print("Дата операции по данным ЦУП:" + self.pcc_operation_date)
        print("Дата операции по данным Агрегатора:" + self.aggr_operation_date)
        print("Сумма операции по данным ЦУП:" + self.pcc_operation_sum)
        print("Сумма операции по данным Агрегатора:" + self.aggr_operation_sum)


def get_operation_info(browser):
    # Получаем список элементов с тегом <p>, расположенных в окне информации об операции
    paragraphs = browser.find_elements_by_css_selector('div>div>div>p')
    # Генерируем список с содержимым
    return [p.text for p in paragraphs]
