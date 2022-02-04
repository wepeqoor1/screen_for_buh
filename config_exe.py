import os
import sys
import configparser
import glob


class ConfigExe:
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("config.ini")  # читаем конфиг

    LK_ADMIN_LOGIN = config['lk_admin_ofdya']['login']
    LK_ADMIN_PASSWORD = config['lk_admin_ofdya']['password']

    def __init__(self):
        self.path_config = self.__get_path_config()
        self.ooo_step = 4
        self.ip_step = 4
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
