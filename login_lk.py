from wait_element import wait_and_click, driver
from config_exe import ConfigExe
from xpath_navigation import AdminSign, UserSign


def login_admin() -> None:
    driver.get("https://partners-lk.ofd-ya.ru/")
    wait_and_click(xpath=AdminSign.login, send_keys=ConfigExe.LK_ADMIN_LOGIN)
    wait_and_click(xpath=AdminSign.password, send_keys=ConfigExe.LK_ADMIN_PASSWORD)
    wait_and_click(AdminSign.come_in, click=True)
    wait_and_click(xpath=AdminSign.close_banner, click=True)


def login_client(user: str, password: str):
    driver.get("https://lk.ofd-ya.ru/")
    wait_and_click(xpath=UserSign.login, send_keys=user)
    wait_and_click(xpath=UserSign.password, send_keys=password)
    wait_and_click(xpath=UserSign.come_in, click=True)
