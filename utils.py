from time import sleep

from loguru import logger


def wait_and_return_element(driver, by, element_value, timeout=5):
    logger.info(f"Waiting for element with {by}='{element_value}' for up to {timeout} seconds.")
    for _ in range(timeout):
        sleep(1)
        elements = driver.find_elements(by=by, value=element_value)
        if elements:
            logger.info(f"Element found: {elements[0]}")
            return elements[0]
    logger.warning(f"Element with {by}='{element_value}' not found after {timeout} seconds.")
    return None


def wait_and_click_element(driver, by, element_value, timeout=5):
    logger.info(f"Attempting to click element with {by}='{element_value}' within {timeout} seconds.")
    element = wait_and_return_element(driver, by, element_value, timeout)
    if element:
        element.click()
        logger.info(f"Clicked element with {by}='{element_value}'.")
    else:
        logger.error(f"Failed to click element with {by}='{element_value}' after {timeout} seconds.")
        raise Exception(f"Element with {by}='{element_value}' not found after {timeout} seconds.")


def assert_element_text(driver, by, element_value, expected_text, timeout=5):
    logger.info(f"Asserting text for element with {by}='{element_value}' within {timeout} seconds.")
    element = wait_and_return_element(driver, by, element_value, timeout)
    if element:
        actual_text = element.text
        logger.info(f"Element text: '{actual_text}', Expected text: '{expected_text}'.")
        assert actual_text == expected_text, f"Expected text '{expected_text}', but got '{actual_text}'"
    else:
        logger.error(f"Failed to find element with {by}='{element_value}' for text assertion after {timeout} seconds.")
        raise Exception(f"Element with {by}='{element_value}' not found after {timeout} seconds.")
