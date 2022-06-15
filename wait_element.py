from loguru import logger as log
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from config_exe import driver, wait


def wait_and_click(xpath: str, send_keys: str = None, click: bool = False) -> None:
    """
    Функция предназначена для быстрого перехода
    на появившейся элемент.
    """
    wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
    if send_keys:
        if click:
            elem = driver.find_element_by_xpath(xpath)
            elem.click()
            elem.send_keys(send_keys)
            return None
        driver.find_element_by_xpath(xpath).send_keys(send_keys)
        text_el = driver.find_element_by_xpath(xpath).get_attribute("value")
        if send_keys != text_el:
            driver.find_element_by_xpath(xpath).clear()
            wait_and_click(xpath=xpath, send_keys=send_keys)
        return driver.find_element_by_xpath(xpath)
    if click:
        driver.find_element_by_xpath(xpath).click()


def wait_and_click_class(class_name: str, send_keys: str = None, click: bool = False) -> None:
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, class_name)))
    if send_keys:
        if click:
            elem = driver.find_element_by_class_name(class_name)
            elem.click()
            elem.send_keys(send_keys)
            return None
        driver.find_element_by_class_name(class_name).send_keys(send_keys)
        text_el = driver.find_element_by_class_name(class_name).get_attribute("value")
        if send_keys != text_el:
            driver.find_element_by_class_name(class_name).clear()
            wait_and_click(xpath=class_name, send_keys=send_keys)
        return driver.find_element_by_class_name(class_name)
    if click:
        driver.find_element_by_class_name(class_name).click()


def wait_class_name(class_name) -> None:
    """
    Определяет наличие элемента
    """
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, class_name)))
    return None


wait_elem = WebDriverWait(driver, 2)



