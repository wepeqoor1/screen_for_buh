import os


for inn in os.listdir():
    os.chdir(inn)
    image_name_list = [
        file
        for file in os.listdir("Скриншоты/")
        if file.endswith(".png")
           and not file.startswith("r_")
           and not file.startswith("s_")
    ]
    inn_dir = os.getcwd()

    if not image_name_list:
        print(inn_dir.split('\\')[-1], image_name_list)
    os.chdir('')

