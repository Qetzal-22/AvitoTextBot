from sqlalchemy.dialects.postgresql.psycopg import logger
from sqlalchemy.orm import Session
import datetime
import logging

from app.db.database import SessionLocal
from app.db.models import User, Request, Payment, Data_Plan, Status_Pay

logger = logging.getLogger(__name__)

def create_user(tg_id: int, username: int, db: Session):
    logger.info(f"Create user - tg_id: {tg_id} | username: {username}")
    user_db = User(tg_id=tg_id, username=username)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def get_user_tg_id(tg_id: int, db: Session):
    logger.info(f"Get user - tg_id: {tg_id}")
    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    return user_db

def update_user_tg_id(tg_id: int,
                      db: Session,
                      username: str = None,
                      data_plan: Data_Plan = None,
                      subscription_expires: datetime = None,
                      total_request: int = None,
                      monthly_request: int = None,
                      is_active: bool = None):
    logger.info(f"Update user - tg_id: {tg_id} | username: {username} | data_plan: {data_plan} | subscription_expires: {subscription_expires} | total_request: {total_request} | monthly_request: {monthly_request} | is_active: {is_active}")

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    if not username is None:
        user_db.username = username

    if not data_plan is None:
        user_db.data_plan = data_plan

    if not subscription_expires is None:
        user_db.subscription_expires = subscription_expires

    if not total_request is None:
        user_db.total_request = total_request

    if not monthly_request is None:
        user_db.monthly_request = monthly_request

    if not is_active is None:
        user_db.is_active = is_active

    db.commit()
    db.refresh(user_db)
    return user_db

def update_user_data_plan(tg_id: int, data_plan: Data_Plan, subscription_expires: datetime, db: Session):
    logger.info(f"Update user data plan - tg_id: {tg_id} | data_plan: {data_plan} | subscription_expires: {subscription_expires}")

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.data_plan = data_plan
    user_db.subscription_expires = subscription_expires

    db.commit()
    db.refresh(user_db)
    return user_db

def update_user_add_request(tg_id: int, db: Session):
    logger.info(f"Update user add request - tg_id: {tg_id}")

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.total_request = user_db.total_request + 1
    user_db.monthly_request = user_db.monthly_request + 1
    db.commit()
    db.refresh(user_db)
    return user_db

def update_user_clear_request(tg_id: int, db: Session):
    logger.info(f"Update user clear request - tg_id: {tg_id}")

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.monthly_request = 0
    db.commit()
    db.refresh(user_db)
    return user_db

def update_user_is_active(tg_id: int, db: Session):
    logger.info(f"Update user is_active - tg_id: {tg_id}")

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.is_active = not user_db.is_active
    db.commit()
    db.refresh(user_db)
    return user_db



def create_request(user_id: int, request: str, db: Session):
    logger.info(f"Create request - user_id: {user_id}")

    request_db = Request(user_id=user_id, request=request)
    db.add(request_db)
    db.commit()
    db.refresh(request_db)
    return request_db

def get_request(id: int, db: Session):
    logger.info(f"Get request - id: {id}")

    request_db = db.query(Request).filter(Request.id == id).first()
    return request_db

def create_payment(provider_payment_id: int, user_id: int, amount: int, status: Status_Pay, db: Session):
    logger.info(f"Create payment - provider_payment_id: {provider_payment_id} | user_id: {user_id} | amount: {amount} | status: {status}")

    payment_db = Payment(provider_payment_id=provider_payment_id, user_id=user_id, amount=amount, status=status)
    db.add(payment_db)
    db.commit()
    db.refresh(payment_db)
    return payment_db

def get_payment(id: int, db: Session):
    logger.info(f"Get payment - id: {id}")

    payment_db = db.query(Payment).filter(Payment.id == id).first()
    return payment_db