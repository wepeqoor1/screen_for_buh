import os
import configparser
import glob

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


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
        if count_xlsx_files > 1:
            raise ValueError('В проекте присутствует больше одного файла с разрешением ".xlsx"')
        elif count_xlsx_files == 0:
            raise ValueError('')
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


config_exe_data = ConfigExe()

chrome_options = Options()

chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--full-screen")

driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        chrome_options=chrome_options
    )
wait = WebDriverWait(driver, 30)

unload_dir_name = "Скриншоты"
ABS_PATH = os.path.abspath(".")
FILE_NAME = config_exe_data.xlsx_filename
FILE_PATH = f"{ABS_PATH}\\{FILE_NAME}"
