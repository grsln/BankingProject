from datetime import datetime

from allure import step
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class TransactionsListPage(BasePage):
    credit_cell = (
        By.XPATH,
        "//tr[contains(.,'Credit')]/td[(count(//td[contains(.,'Amount')]/preceding-sibling::td)+1)]",
    )
    debit_cell = (
        By.XPATH,
        "//tr[contains(.,'Debit')]/td[(count(//td[contains(.,'Amount')]/preceding-sibling::td)+1)]",
    )
    columns_titles = (By.CSS_SELECTOR, "thead td")
    table_rows = (By.CSS_SELECTOR, "tbody tr")

    @step("Проверка отображения пополнения и списания")
    def cells_should_be_present(self):
        self.be_present(self.debit_cell)
        self.be_present(self.credit_cell)

    @step("Проверка наличия транзакций пополнения и списания на сумму {amount}")
    def assert_cells_equal(self, amount):
        assert self.get_text(self.credit_cell) == str(amount)
        assert self.get_text(self.debit_cell) == str(amount)

    @staticmethod
    def convert_datetime(date_time):
        date = datetime.strptime(date_time, "%B %d, %Y %I:%M:%S %p")
        return date.strftime("%d %B %Y %H:%M:%S")

    def get_data(self):
        transactions_types = ("Credit", "Debit")
        transactions_list = []
        rows = self.driver.find_elements(*self.table_rows)
        for row in rows:
            cells_texts = [
                cell.text for cell in row.find_elements(By.CSS_SELECTOR, "td")
            ]
            date_time = self.convert_datetime(cells_texts[0])
            amount = int(cells_texts[1])
            transaction_type = (
                cells_texts[2] if cells_texts[2] in transactions_types else ""
            )
            transactions_list.append([date_time, amount, transaction_type])
        return transactions_list
