from config_exe import wait
from fuzzywuzzy import fuzz
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def check_text_in_element(xpath, text):
    """
    Ожидание конкретного текста в элементе
    """
    wait.until(
        ec.text_to_be_present_in_element(
            (
                By.XPATH,
                xpath
            ),
            text))


def comparison_of_no_request(request: str):
    "Нет заявки в файле .xlsx"
    return fuzz.ratio('нет заявк', request) > 40