from loguru import logger as log
from request import first_request
from scratchcards import scratchcard
from wait_element import wait_and_click, wait_class_name, driver, wait
from contracts import contract
from files_manipulation import download_data_from_file, create_unload_dir, zipped_file
from config_exe import unload_dir_name


def script() -> None:
    first_request(data_list)
    scratchcard(data_list)
    contract(data_list)


if __name__ == "__main__":
    data_list = download_data_from_file()
    create_unload_dir(unload_dir_name)
    script()
    zipped_file(unload_dir_name)
    driver.close()
    driver.quit()

    log.info(wait.__sizeof__())

