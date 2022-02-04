import time
from datetime import datetime
import os
import shutil
from termcolor import colored
import requests
from typing import Optional, Any, Union
import json
import glob

import cv2
import numpy as np
import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager

from fuzzywuzzy import fuzz

# from xpath_navigation import AdminScratchcards, AdminSign, AdminContracts, UserRequest, UserSign
# from get_data_from_servise2ltp_flask import DataService2ltpFlask
import configparser


class AdminSign:
    close_banner = '//*[@id="257_window_close"]'
    login = '//*[@id="gwt-uid-3"]'
    password = '//*[@id="gwt-uid-5"]'
    come_in = '//*[@id="ROOT-2521314"]/div/div[2]/div/div/div/div[2]/div/div[3]/div/div[5]/div'


class AdminScratchcards:
    header_btn = '/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div[1]/table/tbody/tr/td[3]/div/div'
    number_from = '//*[@id="gwt-uid-45"]'
    number_to = '//*[@id="gwt-uid-47"]'
    search = '/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div/div[17]/div'
    clear = '/html/body/div[1]/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div/div[19]'
    data_first_number_card = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[7]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/div'
    value_first_row_number_card = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[7]/div/div[2]/div[1]/table/tbody/tr/td[1]/div'


class AdminContracts:
    close_bunner = '/html/body/div[2]/div[4]/div/div/div[2]/div[2]'
    header_btn = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div/div/div[1]/table/tbody/tr/td[6]'
    draw_up_new_contract = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div[1]/div/div[1]/div'
    inn_btn = '//*[@id="inn"]'
    search = '//*[@id="search"]'
    requisites = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/table/tbody/tr/td[3]'
    inn_in_contract = '//*[@id="gwt-uid-104"]'
    layout_for_screenshot = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div'
    vertical_layout = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[3]/div/div[4]/div'

    vertical_layout_class = 'v-verticallayout.v-layout.v-vertical.v-widget.margin-contract.v-verticallayout-margin-contract.contractFont.v-verticallayout-contractFont.contract-main-border.v-verticallayout-contract-main-border.v-has-width.v-margin-top.v-margin-right.v-margin-bottom.v-margin-left'


class UserSign:
    login = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[2]/div/div[2]/div/div/div/div[5]/div/div[3]/input'
    password = '//*[@id="gwt-uid-3"]'
    come_in = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[2]/div/div[2]/div/div/div/div[5]/div/div[9]/div'
    out = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[1]/div/div/div[5]/div/div[2]/div/div[5]/div/span/span'


class UserRequest:
    close_bunner = '/html/body/div[2]/div[3]/div/div/div[2]/div[2]'
    header_btn = '/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[1]/table/tbody/tr/td[3]/div'
    search_request = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[5]/div/div/div[5]/div/div/div[5]/div/input'
    btn_search_request = '//*[@id="VAADIN_COMBOBOX_OPTIONLIST"]/div/div[2]/table/tbody/tr/td'
    number_request_in_first_row = '//*[@id="ROOT-2521314"]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[5]/div/div/div[7]/div/div[2]/div[1]/table/tbody/tr[1]/td[4]/div'


class DataService2ltpFlask(object):
    from config_exe import ConfigExe
    config_exe = ConfigExe()

    login_support_service = config_exe.username
    password_support_service = config_exe.password

    def __init__(self, method: str, data: dict) -> None:
        self.__url = f"http://10.49.1.1:5000/api/{method}"
        self.__response = requests.post(
            url=self.__url,
            data=f'{json.dumps(data)}',
            auth=(self.login_support_service, self.password_support_service),
        ).json()
        self.response = self.__json_parser(self.__response, method)

    @staticmethod
    def __json_parser(response: dict, method: str) -> Union[Optional[str], Any]:
        if method == 'superuser':
            return response.get('superuser')[0] \
                if response.get('superuser') \
                else response.get('error')
        elif method == 'scratchcard_request':
            return response.get('scratchcard_request') \
                if response.get('scratchcard_request') == [] \
                else response.get('scratchcard_request')[0].get('number')[0]  \
                if response.get('scratchcard_request')  \
                else response.get('error')  \

        else:
            return 'ERROR method'


class ConfigExe:
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("config.ini")  # читаем конфиг

    LK_ADMIN_LOGIN = config['lk_admin_ofdya']['login']
    LK_ADMIN_PASSWORD = config['lk_admin_ofdya']['password']

    def __init__(self):
        self.path_config = self.__get_path_config()
        self.ooo_step = self.config["step"]["ooo_step"]
        self.ip_step = self.config["step"]["ip_step"]
        self.scroll = self.config["step"]["scroll"]
        self.username = ''
        self.password = ''
        self.xlsx_filename = self.__get_path_xlsx_filename()
        self.__get_steps()
        self.__get_login_and_password()

    @staticmethod
    def __get_path_xlsx_filename():
        count_xlsx_files = len(glob.glob('*.xlsx'))
        return glob.glob('*.xlsx')[0]

    @staticmethod
    def __get_path_config():
        basedir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(basedir, 'config.ini')

    def __get_steps(self) -> None:
        self.ooo_step = self.config["step"]["ooo_step"]
        self.ip_step = self.config["step"]["ip_step"]

    def __get_login_and_password(self):
        self.username = self.config["support_service"]["username"]
        self.password = self.config["support_service"]["password"]


def timer(func):
    """
    Декоратор времени выполнения функции
    """

    def wrapper(*args, **kwargs) -> str:
        start = datetime.now()
        result = func(*args, *kwargs)
        execute_seconds = str((datetime.now() - start).seconds)
        print(
            colored(f"{func.__name__}, Время выполнения {execute_seconds} seconds;", "red")
        )
        return result

    return wrapper


def download_data_from_file() -> list:
    """
    Собираем данные в массив из файла .excel
    """
    df = pd.read_excel(FILE_PATH, dtype=str)
    data = []
    for number, row in df.iterrows():
        company_inn, min_request = str(row["company_inn"]), str(row["type"]) + str(
            row["min_id"]
        )
        data_row = company_inn, min_request
        data.append(data_row)
    return data


def create_unload_dir(dir_name) -> str:
    """
    Создаем главную директорию или переходим в нее
    """
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)
    return dir_name


def create_inn_dir(company_inn) -> None:
    """
    Создаем директорию с ИНН клиента и/или преходим в нее
    """
    dir_name = f"./{company_inn}/"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)


def login_client(user: str, password: str):
    """
    Переходим в ЛКК
    """
    driver.get("https://lk.ofd-ya.ru/")

    wait_and_click(xpath=UserSign.login, send_keys=user)
    wait_and_click(xpath=UserSign.password, send_keys=password)
    wait_and_click(xpath=UserSign.come_in, click=True)
    # wait_and_click(xpath=UserSign.out, click=True)

def screen_first_request(request: str, request_screenshot_file: str) -> None:
    """
    Делает скриншот первой заявки
    """
    wait_and_click(xpath=UserRequest.close_bunner, click=True)
    wait_and_click(xpath=UserRequest.header_btn, click=True)
    wait_and_click(xpath=UserRequest.search_request, click=True, send_keys=request)
    # Нажимаем кнопку в выпадающем списке с заявками
    wait_and_click(xpath=UserRequest.btn_search_request, click=True)
    check_text_in_element(UserRequest.number_request_in_first_row, request)
    driver.save_screenshot(request_screenshot_file)
    wait_and_click(xpath=UserSign.out, click=True)



def login_admin() -> None:
    """
    Заходит в ЛКА
    """
    driver.get("https://partners-lk.ofd-ya.ru/")
    # Находим элементы формы и вводим данные для авторизации
    print(ConfigExe.LK_ADMIN_LOGIN, ConfigExe.LK_ADMIN_PASSWORD)
    wait_and_click(xpath=AdminSign.login, send_keys=ConfigExe.LK_ADMIN_LOGIN)
    wait_and_click(xpath=AdminSign.password, send_keys=ConfigExe.LK_ADMIN_PASSWORD)
    wait_and_click(AdminSign.come_in, click=True)
    wait_and_click(xpath=AdminSign.close_banner, click=True)


@timer
def screen_contract_client(inn: str, contract_screenshot_file: str) -> None:
    """Делаем скриншот контракта клиента"""
    wait_and_click(xpath=AdminContracts.header_btn, click=True)
    wait_and_click(xpath=AdminContracts.draw_up_new_contract, click=True)
    wait_and_click(xpath=AdminContracts.inn_btn, send_keys=inn)
    wait_and_click(xpath=AdminContracts.search, click=True)
    wait_class_name(AdminContracts.vertical_layout_class)
    full_screen_element(inn, contract_screenshot_file)
    wait_and_click(xpath=AdminContracts.requisites, click=True)


def full_screen_element(inn: str, contract_screenshot_file: str) -> None:
    """
    Функция делающая несколько скриншотов в ЛКА
    """
    elements = len(
        driver.execute_script("return document.getElementsByClassName('v-spacing')")
    )
    count = 0
    step = int(config_exe_data.ooo_step) if len(inn) == 10 else int(config_exe_data.ip_step)
    for i in range(0, elements, step):
        driver.execute_script(
            f"document.getElementsByClassName('v-spacing')[{i}].scrollIntoView(true);"
        )
        driver.save_screenshot(f"{int(i / step)}.png")
        count += 1
    crop_images(count)
    create_panorama(contract_screenshot_file)


def crop_images(count: int) -> None:
    """
    Создаются изображения для последующей склейки
    :param count: Колличество скриншотов для обрезки
    """
    crop_files_list = [file for file in os.listdir('./') if file.startswith('crop_')]
    delete_crops(crop_files_list)

    first_image = cv2.imread("0.png")
    start_y, finish_y, start_x, finish_x = get_size(first_image)
    image_name_list = [
        file
        for file in os.listdir("./")
        if file.endswith(".png")
           and not file.startswith("r_")
           and not file.startswith("s_")
    ]
    for image_name in image_name_list:
        image = Image.open(image_name)
        image = image.crop((int(start_x), int(start_y), int(finish_x), int(finish_y)))
        image.rotate(90, Image.NEAREST, expand=1).save(f"crop_{image_name}")
        os.remove(image_name)
    delete_eq_image(count)


def delete_eq_image(count: int):
    for i in range(1, count - 1):
        last_image = f"crop_{i - 1}.png"
        image_name = f"crop_{i}.png"
        if difference_images(last_image, image_name):
            os.remove(last_image)


def get_size(first_image_name) -> tuple:
    gray = cv2.cvtColor(first_image_name, cv2.COLOR_BGR2GRAY)
    height, weight, _ = first_image_name.shape
    gray = cv2.Canny(gray, 150, 150)
    kernel = np.ones((5, 5), np.uint8)
    start = 0  # ~ 160
    finish = 0  # ~ 786
    scroll = config_exe_data.scroll  # px
    gray = cv2.dilate(gray, kernel, iterations=2)
    for i, row in enumerate(gray):
        if sum(row) > weight * 200:
            if i < height / 2:
                start = i
            else:
                finish = i
                break
    return start, finish, scroll, weight - int(scroll)


def difference_images(img1, img2):
    image_1 = cv2.imread(img1)
    image_2 = cv2.imread(img2)
    return np.all(image_1 == image_2)


def create_panorama(contract_screenshot_file: str) -> None:
    stitcher = cv2.Stitcher().create()
    image_name_list = [file for file in os.listdir("./") if file.startswith("crop_")]
    images = [cv2.imread(x) for x in image_name_list]

    (status, result) = stitcher.stitch(images)
    if status == cv2.STITCHER_OK:
        result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite(contract_screenshot_file, result)
        delete_crops(image_name_list)
    else:
        raise TypeError("что-то не сложилось")


def delete_crops(name_list: list) -> None:
    for name in name_list:
        os.remove(name)


@timer
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


def wait_and_click(xpath: str, send_keys: str = None, click: bool = False) -> None:
    """
    Функция предназначена для быстрого перехода
    на появившейся элемент.
    """
    wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
    if send_keys and click:
        elem = driver.find_element_by_xpath(xpath)
        elem.click()
        elem.send_keys(send_keys)
        return None
    if send_keys:
        driver.find_element_by_xpath(xpath).send_keys(send_keys)
        text_el = driver.find_element_by_xpath(xpath).get_attribute("value")
        if send_keys != text_el:
            driver.find_element_by_xpath(xpath).clear()
            wait_and_click(xpath=xpath, send_keys=send_keys)
        return driver.find_element_by_xpath(xpath)
    if click:
        driver.find_element_by_xpath(xpath).click()


def wait_class_name(class_name) -> None:
    """
    Определяет наличие элемента
    """
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, class_name)))
    return None


def zipped_file(dir_name: str) -> None:
    print("zipped_file")
    os.chdir(ABS_PATH)
    shutil.make_archive(
        base_name="Скриншоты",
        format="zip",
        root_dir=dir_name,
    )


def comparison_of_no_request(request: str):
    return fuzz.ratio('нет заявк', request) > 40



@timer
def first_request(data_list) -> None:
    """
    Скрин первой заявки
    """
    start = datetime.now()

    for idx, values in enumerate(data_list):
        company_inn, request = values
        print(f'{idx + 1} из заявок {len(data_list)}')

        if comparison_of_no_request(request):
            print(f'Нет заявки {request}')
            continue

        create_inn_dir(company_inn)
        request_screenshot_file = f"r_{company_inn}.png"

        if os.path.exists(request_screenshot_file):
            print(f"Пропустили ИНН {company_inn} - скрин первой заявки {request}")
            os.chdir("..")
            continue

        logo_pass = DataService2ltpFlask(method='superuser', data={"inn": company_inn, "role": "client"})
        print(logo_pass.response)
        user, password = logo_pass.response.get("login"), logo_pass.response.get("password")
        print(user, password)

        if user.startswith('OFD'):
            print(f'{company_inn} старый крнтракт')
            continue

        login_client(user, password)
        screen_first_request(
            request, request_screenshot_file
        )  # Делаем скриншот первой оплаченной заявки"
        os.chdir("..")
    print(colored(
        f"Время выполнения скриншотов по первой заявке у улиентов "
        f"{len(data_list)} шт: {datetime.now() - start}",
        'blue'
    )
    )


@timer
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


@timer
def script() -> None:
    contract(data_list)
    # first_request(data_list)
    # scratchcard(data_list)


if __name__ == "__main__":
    config_exe_data = ConfigExe()
    unload_dir_name = "Скриншоты"
    ABS_PATH = os.path.abspath(".")
    FILE_NAME = config_exe_data.xlsx_filename
    FILE_PATH = f"{ABS_PATH}\\{FILE_NAME}"

    "Chrome starting"
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--full-screen")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options
    )
    wait = WebDriverWait(driver, 30)

    data_list = download_data_from_file()
    create_unload_dir(unload_dir_name)
    script()
    zipped_file(unload_dir_name)
    driver.close()
    driver.quit()
