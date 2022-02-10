import os

import numpy as np
from PIL import Image

from wait_element import driver
from config_exe import ConfigExe
import cv2


config_exe_data = ConfigExe()


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