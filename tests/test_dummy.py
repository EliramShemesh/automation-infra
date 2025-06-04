import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from loguru import logger

from utils import wait_and_click_element, assert_element_text



@pytest.mark.dummy
@allure.title("Dummy Test")
@allure.description("This is a dummy test created solely for generating the Allure report.")
def test_dummy():
    with allure.step("Dummy step"):
        logger.info("This is a dummy test step.")
        assert True
