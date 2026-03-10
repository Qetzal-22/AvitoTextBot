from aiohttp import request
from sqlalchemy.orm import Session
from sqlalchemy import func
import datetime
from datetime import timedelta
from datetime import datetime
import logging


from app.db.models import User, Request, Payment, Data_Plan, Status_Pay

logger = logging.getLogger(__name__)

def create_user(tg_id: int, username: str, db: Session):
    logger.info("Create user tg_id=%s username=%s", tg_id, username)
    user_db = User(tg_id=tg_id, username=username)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    logger.info("Create user successful tg_id=%s", tg_id)
    return user_db

def get_user_tg_id(tg_id: int, db: Session):
    logger.debug("Get user tg_id=%s", tg_id)
    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    return user_db

def get_user(id: int, db: Session):
    logger.debug("Get user id=%s", id)
    user_db = db.query(User).filter(User.id == id).first()
    return user_db

def get_users(db: Session):
    logger.debug("Get users")
    users_db = db.query(User).all()
    return users_db

def get_users_end_sub(db: Session):
    logger.debug("Get users")
    users_db = db.query(User).filter((User.subscription_expires <= datetime.datetime.now()) & (User.subscription_expires > (datetime.datetime.now() - timedelta(days=182)))).all()
    return users_db

def get_activity_users(db: Session):
    logger.debug("Get activity users")

    one_week_ago = datetime.now() - timedelta(weeks=1)
    count_activity_users = db.query(func.count(func.distinct(Request.user_id))).filter(Request.create_at > one_week_ago).scalar()
    return count_activity_users

def update_user_tg_id(tg_id: int,
                      db: Session,
                      username: str = None,
                      data_plan: Data_Plan = None,
                      subscription_expires: datetime = None,
                      total_request: int = None,
                      monthly_request: int = None,
                      is_active: bool = None):
    logger.info("Update user tg_id=%s", tg_id)

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    if not username is None:
        logger.info("Update user tg_id=%s username=%s", tg_id, username)
        user_db.username = username

    if not data_plan is None:
        logger.info("Update user tg_id=%s data_plan=%s", tg_id, data_plan)
        user_db.data_plan = data_plan

    if not subscription_expires is None:
        logger.info("Update user tg_id=%s subscription_expires=%s", tg_id, subscription_expires)
        user_db.subscription_expires = subscription_expires

    if not total_request is None:
        logger.info("Update user tg_id=%s total_request=%s", tg_id, total_request)
        user_db.total_request = total_request

    if not monthly_request is None:
        logger.info("Update user tg_id=%s monthly_request=%s", tg_id, monthly_request)
        user_db.monthly_request = monthly_request

    if not is_active is None:
        logger.info("Update user tg_id=%s is_active=%s", tg_id, is_active)
        user_db.is_active = is_active

    db.commit()
    db.refresh(user_db)
    logger.info("Update user successful tg_id=%s", tg_id)
    return user_db

def update_user_data_plan(tg_id: int, data_plan: Data_Plan, subscription_expires: datetime, db: Session):
    logger.info("Update user data plan tg_id=%s data_plan=%s subscription_expires=%s", tg_id, data_plan, subscription_expires)

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.data_plan = data_plan
    user_db.subscription_expires = subscription_expires

    db.commit()
    db.refresh(user_db)
    logger.info("Update user successful tg_id=%s", tg_id)
    return user_db

def update_user_add_request(tg_id: int, db: Session):
    logger.info("Update user add request tg_id=%s", tg_id)

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.total_request = user_db.total_request + 1
    user_db.monthly_request = user_db.monthly_request + 1
    user_db.daily_request = user_db.daily_request + 1
    db.commit()
    db.refresh(user_db)
    logger.info("Update user successful tg_id=%s", tg_id)
    return user_db

def update_user_clear_request(tg_id: int, db: Session):
    logger.info("Update user clear request tg_id=%s", tg_id)

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.monthly_request = 0
    user_db.daily_request = 0
    db.commit()
    db.refresh(user_db)
    logger.info("Update user successful tg_id=%s", tg_id)
    return user_db

def update_user_clear_request_daily(tg_id: int, db: Session):
    logger.info("Update user clear request daily tg_id=%s", tg_id)

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.daily_request = 0
    db.commit()
    db.refresh(user_db)
    logger.info("Update user successful tg_id=%s", tg_id)
    return user_db

def update_user_is_active(tg_id: int, db: Session):
    logger.info("Update user is active tg_id=%s", tg_id)

    user_db = db.query(User).filter(User.tg_id == tg_id).first()
    user_db.is_active = not user_db.is_active
    db.commit()
    db.refresh(user_db)
    logger.info("Update user successful tg_id=%s", tg_id)
    return user_db



def create_request(user_id: int, request: str, db: Session):
    logger.info("Create request user_id=%s length_request=%s", user_id, len(request))

    request_db = Request(user_id=user_id, request=request)
    db.add(request_db)
    db.commit()
    db.refresh(request_db)
    logger.info("Create request successful user_id=%s", user_id)
    return request_db

def get_request(user_id: int, db: Session):
    logger.debug("Get request user_id=%s", user_id)

    request_db = db.query(Request).filter(Request.user_id == user_id).first()
    return request_db

def get_requests(db: Session):
    logger.debug("Get requests")
    requests = db.query(Request).all()
    return requests

def get_today_requests(db: Session):
    logger.debug("Get requests today")

    one_day_ago = datetime.now() - timedelta(days=1)
    count_request = db.query(func.count(Request.id)).filter(Request.create_at > one_day_ago).scalar()
    return count_request

def get_request_for_week(db: Session):
    logger.debug("Get request for week")
    one_week_ago = datetime.now() - timedelta(weeks=1)
    request_for_week = db.query(Request).filter(Request.create_at > one_week_ago).all()
    return request_for_week

def get_requests_sort_date(db: Session):
    logger.debug("Get requset sort data")
    requests = db.query(Request).order_by(Request.create_at.desc()).limit(5).all()
    return requests


def create_payment(payload: str, user_id: int, amount: int, status: Status_Pay, plan: Data_Plan, db: Session):
    logger.info(
        "Create payment payload=%s user_id=%s amount=%s status=%s plan=%s",
        payload,
        user_id,
        amount,
        status,
        plan
    )

    payment_db = Payment(payload=payload, user_id=user_id, amount=amount, status=status, plan=plan)
    db.add(payment_db)
    db.commit()
    db.refresh(payment_db)
    logger.info("Create payment successful user_id=%s payload=%s", user_id, payload)
    return payment_db

def update_payment_status(payload: str, new_status: Status_Pay, db: Session):
    logger.info("Update payment payload=%s new_status=%s", payload, new_status)

    payment_db = db.query(Payment).filter(Payment.payload == payload).first()
    payment_db.status = new_status
    db.commit()
    db.refresh(payment_db)
    logger.info("Update payment successful payload=%s", payload)
    return payment_db

def update_payment_status_success(payload: str, db: Session):
    logger.info("Update payment payload=%s", payload)

    payment_db = db.query(Payment).filter(Payment.payload == payload, Payment.status == Status_Pay.PENDING).first()
    payment_db.status = Status_Pay.SUCCESS
    db.commit()
    db.refresh(payment_db)
    logger.info("Update payment successful payload=%s", payload)
    return payment_db

def get_payment(payload: str, db: Session):
    logger.debug("Get payment payload=%s", payload)

    payment_db = db.query(Payment).filter(Payment.payload == payload).first()
    return payment_db

def get_payments(db: Session):
    logger.debug("Get payments")
    payments = db.query(Payment).all()
    return payments

def get_monthly_income(db: Session):
    logger.debug("Get monthly income")
    one_month_ago = datetime.now() - timedelta(days=31)
    income = db.query(Payment.amount).filter((Payment.create_at > one_month_ago) & (Payment.status == Status_Pay.SUCCESS)).all()
    return income

def get_income_for_week(db: Session):
    logger.debug("Get income for week")
    one_week_ago = datetime.now() - timedelta(weeks=1)
    income_for_week = db.query(Payment).filter((Payment.create_at > one_week_ago) & (Payment.status == Status_Pay.SUCCESS)).all()
    return income_for_week

def get_transactions_sort_date(db: Session):
    logger.debug("Get transactions sort date")
    transactions = db.query(Payment).order_by(Payment.create_at.desc()).filter(Payment.status == Status_Pay.SUCCESS).limit(5).all()
    return transactions
