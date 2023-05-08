from selenium.common import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver) -> None:
        self.driver = driver

    def be_present(self, locator, timeout=10):
        wait = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=1,
            ignored_exceptions=[ElementNotVisibleException, NoSuchElementException],
        )
        web_element = wait.until(ec.presence_of_element_located(locator))
        return web_element

    def have_text(self, locator, text, timeout=10):
        wait = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=1,
            ignored_exceptions=[ElementNotVisibleException, NoSuchElementException],
        )
        web_element = wait.until(ec.text_to_be_present_in_element(locator, text))
        return web_element

    def click(self, locator):
        web_element = self.be_present(locator)
        web_element.click()

    def type(self, locator, text):
        web_element = self.be_present(locator)
        web_element.send_keys(text)

    def get_text(self, locator):
        web_element = self.be_present(locator)
        return web_element.text

    def assert_text_in_page_source(self, text):
        assert text in self.driver.page_source

    def select_by_text(self, locator, text):
        web_element = self.be_present(locator)
        web_element.click()
        web_element.find_element(By.XPATH, "//option[.='{}']".format(text)).click()
