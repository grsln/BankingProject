import allure
import pytest
from allure_commons.types import Severity

from common.utils import save_transactions
from pages.account_page import AccountPage
from pages.login_page import LoginPage
from pages.transactions_list_page import TransactionsListPage


@pytest.mark.usefixtures("driver_init_chrome")
class BasicTest:
    pass


@allure.epic("UI-тесты XYZBank")
@allure.feature("Транзакции")
class TestXYZBank(BasicTest):
    @allure.severity(Severity.CRITICAL)
    @allure.title("Пополнение и списание со счета пользователем")
    @pytest.mark.smoke
    def test_banking(self, day_fibonacci):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.should_be_opened()
        login_page.login_as("Harry Potter")
        login_page.should_be_login_as("Harry Potter")

        account_page = AccountPage(self.driver)
        account_page.open_deposit_form()
        account_page.deposit_amount(day_fibonacci)
        account_page.assert_deposited()

        account_page.open_withdraw_form()
        account_page.withdraw_form_should_be_opened()
        account_page.withdraw_amount(day_fibonacci)
        account_page.assert_withdrawn()
        account_page.assert_balance_equal(0)

        account_page.open_transactions()
        transactions_list_page = TransactionsListPage(self.driver)
        transactions_list_page.cells_should_be_present()
        transactions_list_page.assert_cells_equal(day_fibonacci)
        save_transactions(transactions_list_page.get_data())
        allure.attach.file(
            "transactions.csv",
            name="Transactions",
            attachment_type=allure.attachment_type.CSV,
        )
