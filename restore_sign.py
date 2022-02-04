from app import app
from app.sender import send_message_sign_status
from app.celery_config import celery
from billiard.exceptions import SoftTimeLimitExceeded
from datetime import datetime as dt
import json
import logging
from app.custom_exceptions import MoreOne, NoOne, SignaturePresent, RecoverError, print_exception
from app.functions.restore_sign.sql_request import get_sign, recover_sign, remove_sign, session
from sqlalchemy.exc import DatabaseError, OperationalError
from psycopg2 import OperationalError

logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(name)s]: %(message)s')
log = logging.getLogger(__name__)


def recreate_sign(inn: str, duration: int, email: str):
    try:
        sign_row: dict = get_sign(inn)
        contract_id: str = sign_row['id']
        result: bool = restore_sign(inn, contract_id, duration, email)
        if result:
            delete_sign.apply_async(args=[inn, contract_id, duration, email], ignore_result=True, countdown=duration*60)

        return f"По истечению {duration} минут(ы) будет направлено письмо на электронный адрес {email} об отзыве " \
               f"подписи у компании {inn}. Если  такое сообщение не поступит - " \
               f"просьба обратиться к 3-й линии поддержки за отменой."
    except MoreOne:
        return f'Найдено более одной компании с данным ИНН {inn}. Просьба обратиться к 3-й линии поддержки.'
    except NoOne:
        return f'Информация по данному ИНН {inn} не найдена.'
    except RecoverError as er_message:
        return er_message
    except SignaturePresent:
        return f'Подпись у данной компании {inn} уже существует.'
    except (AttributeError, DatabaseError, OperationalError, OperationalError) as er:
        session.rollback()
        log.error(f'Connection with DB was closed, {er}')
        return 'Ошибка соединения с БД'
    except Exception as er:
        print_exception(log)
        session.rollback()
        session.rollback()
        return f'Непредвиденная ошибка {er}'


def set_task_recover_sign(inn: str, contract_id: str, duration: int, email: str) -> None:
    result: bool = restore_sign(inn, contract_id, duration, email)
    if result:
        delete_sign.apply_async(args=[inn, contract_id, duration, email], ignore_result=True, countdown=duration * 60)


def check_error(inn: str, flag: bool, action: str) -> bool or None:
    if not flag:
        if action == 'recover':
            log.error(f'Recover sign for inn {inn} complete with error')
            message: str = f'Во время восстановления подписи для ИНН {inn} произошла ошибка'
        else:
            log.error(f'Delete sign for inn {inn} complete with error')
            message: str = f'Во время удаления подписи для ИНН {inn} произошла ошибка'
        raise RecoverError(message)
    log.info(f'{action.capitalize()} sign complete for inn {inn}')
    return flag


def restore_sign(inn: str, contract_id: str, duration: int, email: str) -> bool:
    action: str = 'recover'
    with open(f"{app.config['STATIC_FILES']}sign.json", 'r') as json_file:
        sign = json.loads(json_file.read()).get(inn, f'NOKEP_{int(dt.now().timestamp())}')
    flag: bool = recover_sign(contract_id, sign)
    send_message_sign_status(inn, duration, email, flag, action)
    return check_error(inn, flag, action)


@celery.task(name='sign.delete')
def delete_sign(inn: str, contract_id: str, duration: int, email: str) -> bool:
    try:
        action = 'delete'
        flag = remove_sign(contract_id)
        send_message_sign_status(inn, duration, email, flag, action)
        return check_error(inn, flag, action)
    except SoftTimeLimitExceeded:
        log.info('Task killed')
        return False


if __name__ == '__main__':
    pass
