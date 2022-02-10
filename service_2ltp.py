import json

import requests
from typing import Optional, Any, Union


class DataService2ltpFlask(object):
    """
    Забирает данные по скрейтчкарте или логин с паролем
        логин и пароль
            method='superuser'
            data = f'{{"inn": "{inn}", "role": "{role}"}}'
        response:
            {'login': 'login', 'password': 'password'} : dict
            [{'loc': ['inn'], 'msg': 'It is not INN', 'type': 'value_error'}] : list

        проверка на карту оплаты
            method='scratchcard_request'
            data = f'{{"request": "{request}"}}'
        response:
            030115681: str
            [{'loc': ['request'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]: list
            []: list - no scratchcard from request
    """
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
        print(self.__response)
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


# inn, role, request = '701730700158', 'client', '1058552'
# # logopass = DataService2ltpFlask(method='superuser', data={"inn": inn, "role": role})
# scratchcard = DataService2ltpFlask(method='scratchcard_request', data={"request": request})
#
# inn, role, request = '701730700158', 'client', 'i1058552'
# # logopass = DataService2ltpFlask(method='superuser', data={"inn": inn, "role": role})
# scratchcard = DataService2ltpFlask(method='scratchcard_request', data={"request": request})
