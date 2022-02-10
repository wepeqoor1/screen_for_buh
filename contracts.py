import os

from login_lk import login_admin
from wait_element import wait_and_click, wait_class_name
from xpath_navigation import AdminContracts
from files_manipulation import create_inn_dir
from generate_contract_panorama import full_screen_element


def contract(data_list: list) -> None:
    """
    Делаем скриншот контракта клиента
    """
    login_admin()
    wait_and_click(xpath=AdminContracts.header_btn, click=True)
    wait_and_click(xpath=AdminContracts.draw_up_new_contract, click=True)

    """Контракт клиента"""
    for idx, values in enumerate(data_list):
        print(f'{idx + 1} из контарктов {len(data_list)}')
        company_inn, request = values

        if len(company_inn) == 11:
            company_inn = int(str(0) + str(company_inn))
        contract_screenshot_file = f"c_{company_inn}.png"
        create_inn_dir(company_inn)

        if os.path.exists(contract_screenshot_file):
            print(f"Пропустили ИНН {company_inn} - контракт клиента")
            os.chdir("..")
            continue
        print(f"Делаем скриншот контракта: ИНН {company_inn}")
        screen_contract_client(company_inn, contract_screenshot_file)
        os.chdir("..")


def screen_contract_client(inn: str, contract_screenshot_file: str) -> None:
    """Делаем скриншот контракта клиента"""
    wait_and_click(xpath=AdminContracts.close_banner, click=True)
    wait_and_click(xpath=AdminContracts.header_btn, click=True)
    wait_and_click(xpath=AdminContracts.draw_up_new_contract, click=True)
    wait_and_click(xpath=AdminContracts.inn_btn, send_keys=inn)
    wait_and_click(xpath=AdminContracts.search, click=True)
    wait_class_name(AdminContracts.vertical_layout_class)
    full_screen_element(inn, contract_screenshot_file)
    wait_and_click(xpath=AdminContracts.requisites, click=True)


