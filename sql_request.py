from app.models import Contract
from sqlalchemy.exc import DatabaseError, OperationalError
from psycopg2 import OperationalError
import logging
from app.custom_exceptions import MoreOne, NoOne, SignaturePresent, print_exception
from app.functions.db_controller import SessionLocal

logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(name)s]: %(message)s')
log = logging.getLogger(__name__)

session = SessionLocal()


def get_sign(inn: str) -> list or int:
    """Получаем подпись"""

    result = (
        (
            session.query(
                Contract.sign,
                Contract.id
            ).filter(Contract.contract['inn'].astext == inn)
        ).all()
    )
    session.rollback()
    if len(result) == 0:
        raise NoOne(f'No one result find with inn {inn}')
    elif len(result) > 1:
        raise MoreOne(f'Find more one result with inn {inn}. {result}')
    elif result[0][0]:
        raise SignaturePresent(f'Company {inn} have sign. {result}')
    return result[0]._asdict()


def recover_sign(contract_id: str, sign: str) -> bool or int:
    try:
        session.query(Contract).filter_by(id=contract_id).update({'sign': sign})
        session.commit()
        session.rollback()
        return True
    except (AttributeError, DatabaseError, OperationalError, OperationalError):
        log.error('Connection with DB was closed')
        return False
    except Exception:
        print_exception(log)
        session.rollback()
        return False


def remove_sign(contract_id: str) -> bool:
    try:
        session.query(Contract).filter_by(id=contract_id).update({'sign': None})
        session.commit()
        session.rollback()
        return True
    except (AttributeError, DatabaseError, OperationalError, OperationalError):
        log.error('Connection with DB was closed')
        return False
    except Exception:
        print_exception(log)
        session.rollback()
        return False


if __name__ == '__main__':
    pass
