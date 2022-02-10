import os

from login_lk import login_admin
from wait_element import wait_and_click
from xpath_navigation import AdminScratchcards
from service_2ltp import DataService2ltpFlask
from check_text import check_text_in_element, comparison_of_no_request
from files_manipulation import create_inn_dir
from config_exe import driver


def scratchcard(data_list) -> None:
    """
    Скрин номер карты оплаты
    """
    login_admin()
    wait_and_click(AdminScratchcards.header_btn, click=True)
    for idx, values in enumerate(data_list):
        company_inn, request = values
        if comparison_of_no_request(request):
            continue
        request = request[1:]

        print(f'{idx + 1} из карт оплаты {len(data_list)}')
        number_scr = DataService2ltpFlask(
            method='scratchcard_request',
            data={"request": request}
        )  # Заявка оплачена картой оплаты?
        number_scr = number_scr.response
        create_inn_dir(company_inn)

        if number_scr == []:
            print(f"ИНН {company_inn} - Заявка № {request} - Нет карты оплаты")
            os.chdir("..")
            continue
        scratchcard_screenshot_file = f"s_{company_inn}.png"

        if os.path.exists(scratchcard_screenshot_file):
            print(f"Пропустили ИНН {company_inn} - номер карты оплаты: {number_scr}")
        else:
            screen_scratchcard_number(
                number_scr, scratchcard_screenshot_file
            )
        os.chdir("..")


def screen_scratchcard_number(
        number_scr: str, scratchcard_screenshot_file: str
) -> None:
    """
    Делаем скриншот карты оплаты в ЛКА
    """
    wait_and_click(AdminScratchcards.number_from, send_keys=number_scr)
    wait_and_click(AdminScratchcards.number_to, send_keys=number_scr)
    wait_and_click(AdminScratchcards.search, click=True)

    text_number_from = driver.find_element_by_xpath(
        AdminScratchcards.number_from
    ).get_attribute("value")

    text_number_to = driver.find_element_by_xpath(
        AdminScratchcards.number_to
    ).get_attribute("value")

    """Проверяем совпадение (номер от) и (номер до)"""
    if text_number_from != text_number_to:
        wait_and_click(AdminScratchcards.clear, click=True)

    check_text_in_element(
        AdminScratchcards.value_first_row_number_card,
        number_scr
    )

    driver.save_screenshot(scratchcard_screenshot_file)

    wait_and_click(AdminScratchcards.clear, click=True)
    check_text_in_element(
        AdminScratchcards.value_first_row_number_card,
        '010200001'
    )


