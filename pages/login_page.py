from allure import step
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    PAGE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"
    main_heading = (By.CLASS_NAME, "mainHeading")
    customer_login_button = (By.XPATH, "//button[.='Customer Login']")
    name_select = (By.CSS_SELECTOR, "#userSelect")
    name_select_item = (By.XPATH, "//option[.='Harry Potter']")
    login_button = (By.CSS_SELECTOR, 'button[type="submit"]')
    logout_button = (By.CSS_SELECTOR, "button.logout")

    @step("Открытие страницы авторизации")
    def open(self):
        self.driver.get(self.PAGE_URL)

    @step("Проверка открытия страницы авторизации")
    def should_be_opened(self):
        assert "XYZ Bank" in self.get_text(self.main_heading)

    @step('Авторизация пользователем "{user}"')
    def login_as(self, user):
        self.click(self.customer_login_button)
        self.select_by_text(self.name_select, user)
        self.click(self.login_button)

    @step('Проверка авторизации пользователем "{user}"')
    def should_be_login_as(self, user):
        assert user in self.driver.page_source
        assert self.be_present(self.logout_button)
