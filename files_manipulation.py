import os
import shutil

from config_exe import ABS_PATH, FILE_NAME
import pandas as pd


def download_data_from_file() -> list:
    """
    Собираем данные в массив из файла .excel
    """
    df = pd.read_excel(os.path.join(ABS_PATH, FILE_NAME), engine='openpyxl', dtype=str)
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


def zipped_file(dir_name: str) -> None:
    print("zipped_file")
    os.chdir(ABS_PATH)
    shutil.make_archive(
        base_name="Скриншоты",
        format="zip",
        root_dir=dir_name,
    )
