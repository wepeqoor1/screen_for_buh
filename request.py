import os
from time import sleep
from loguru import logger as log

from check_text import check_text_in_element, comparison_of_no_request
from config_exe import driver
from files_manipulation import create_inn_dir
from service_2ltp import DataService2ltpFlask
from login_lk import login_client
from wait_element import wait_and_click, wait_and_click_class
from xpath_navigation import UserRequest, UserSign
from class_navigation import User


def first_request(data_list) -> None:
    for idx, values in enumerate(data_list):
        company_inn, request = values
        log.info(f'{idx + 1} из заявок {len(data_list)}')

        if comparison_of_no_request(request):
            log.info(f'Нет заявки {request}')
            continue

        create_inn_dir(company_inn)
        request_screenshot_file = f"r_{company_inn}.png"

        if os.path.exists(request_screenshot_file):
            log.info(f"Пропустили ИНН {company_inn} - скрин первой заявки {request}")
            os.chdir("..")
            continue

        logo_pass = DataService2ltpFlask(method='superuser', data={"inn": company_inn, "role": "client"})
        user, password = logo_pass.response.get("login"), logo_pass.response.get("password")
        log.info(user, password)

        if user.startswith('OFD'):
            log.info(f'{company_inn} старый крнтракт')
            continue

        login_client(user, password)
        screen_first_request(request, request_screenshot_file)  # Делаем скриншот первой оплаченной заявки"
        os.chdir("..")


def screen_first_request(request: str, request_screenshot_file: str) -> None:
    """
    Делает скриншот первой заявки
    """
    sleep(5)
    driver(xpath='/html/body/div[2]/div[4]/div/div/div[2]/div[2]', click=True)
    wait_and_click(xpath=UserRequest.header_btn, click=True)
    wait_and_click(xpath=UserRequest.search_request, click=True, send_keys=request)
    # Нажимаем кнопку в выпадающем списке с заявками
    wait_and_click(xpath=UserRequest.btn_search_request, click=True)
    check_text_in_element(UserRequest.number_request_in_first_row, request)
    driver.save_screenshot(request_screenshot_file)
    wait_and_click(xpath=UserSign.out, click=True)
