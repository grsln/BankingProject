from allure import step
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AccountPage(BasePage):
    PAGE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/account"
    main_heading = (By.CLASS_NAME, "mainHeading")
    deposit_button = (
        By.XPATH,
        "//button[contains(text(),'Deposit') and @ng-click='deposit()']",
    )
    amount_input = (By.XPATH, "//input[@ng-model='amount']")
    deposit_amount_button = (By.CSS_SELECTOR, 'button[type="submit"]')
    message = (By.CSS_SELECTOR, ".error")
    withdraw_button = (
        By.XPATH,
        "//button[contains(text(),'Withdrawl') and @ng-click='withdrawl()']",
    )
    amount_label = (By.CSS_SELECTOR, ".form-group label")
    withdraw_amount_button = (By.CSS_SELECTOR, 'button[type="submit"]')
    balance_text = (By.XPATH, "(//*[@ng-hide='noAccount']/strong)[2]")
    transaction_button = (
        By.XPATH,
        "//button[contains(text(),'Transactions') and @ng-click='transactions()']",
    )

    @step("Открытие формы пополнения счета")
    def open_deposit_form(self):
        self.click(self.deposit_button)

    @step("Пополнения счета на сумму {amount}")
    def deposit_amount(self, amount):
        self.type(self.amount_input, amount)
        self.click(self.deposit_amount_button)

    @step("Проверка пополнения счета")
    def assert_deposited(self):
        assert "Deposit Successful" in self.get_text(self.message)

    @step("Открытие формы списания со счета")
    def open_withdraw_form(self):
        self.click(self.withdraw_button)

    @step("Проверка открытия формы списания")
    def withdraw_form_should_be_opened(self):
        self.have_text(self.amount_label, "Amount to be Withdrawn :")

    @step("Списание со счета на сумму {amount}")
    def withdraw_amount(self, amount):
        self.type(self.amount_input, amount)
        self.click(self.withdraw_amount_button)

    @step("Проверка списания со счета")
    def assert_withdrawn(self):
        assert "Transaction successful" in self.get_text(self.message)

    @step("Проверка равенства баланса сумме {balance}")
    def assert_balance_equal(self, balance):
        assert self.get_text(self.balance_text) == str(balance)

    @step("Открытие страницы транзакций")
    def open_transactions(self):
        self.click(self.transaction_button)
