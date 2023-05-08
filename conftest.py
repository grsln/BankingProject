import logging
import os

import allure
import pytest
from dotenv import load_dotenv
from selenium import webdriver

from common.send_allure import send_allure_reports

logger = logging.getLogger("globalsqa")

load_dotenv()
selenium_grid_hub = os.getenv("SELENIUM_GRID_HUB")


@pytest.fixture(scope="session", autouse=True)
def send_allure():
    yield
    send_allure_reports()


@pytest.fixture(scope="class")
def driver_init_chrome(request):
    options = webdriver.ChromeOptions()
    options.set_capability("platformName", "LINUX")
    options.set_capability("browserName", "chrome")
    web_driver = webdriver.Remote(command_executor=selenium_grid_hub, options=options)
    request.cls.driver = web_driver
    yield
    web_driver.quit()


@pytest.fixture(scope="class")
def driver_init_firefox(request):
    options = webdriver.FirefoxOptions()
    options.set_capability("platformName", "LINUX")
    options.set_capability("browserName", "firefox")
    options.set_capability("browserVersion", "112.0")
    web_driver = webdriver.Remote(command_executor=selenium_grid_hub, options=options)
    request.cls.driver = web_driver
    yield
    web_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.failed:
        try:
            with allure.step("Screen-shot done"):
                allure.attach(
                    item.cls.driver.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception as e:
            allure.step("Fail to take screen-shot: {}".format(e))
            logger.error("Fail to take screen-shot: {}".format(e))
