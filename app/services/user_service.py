import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


from app.db import crud
from app.db.database import SessionLocal
from app.db.models import Data_Plan

logger = logging.getLogger(__name__)

def get_users(db: Session):
    logger.info("DB request get_users")
    users = crud.get_users(db)
    logger.info("DB successful response get_users")
    return users

def get_user(db: Session, user_id: int):
    logger.info("DB request get_user")
    users = crud.get_user_tg_id(user_id, db)
    logger.info("DB successful response get_user")
    return users

def get_user_by_id(db: Session, user_id: int):
    logger.info("DB request get_user")
    users = crud.get_user(user_id, db)
    logger.info("DB successful response get_user")
    return users

def get_user_dict_form(db: Session, user_id: int):
    logger.info("DB request get_user")
    user = crud.get_user(user_id, db)
    logger.info("DB successful response get_user")
    user_dict = {}
    user_dict["id"] = user.id
    user_dict["tg_id"] = user.tg_id
    user_dict["username"] = user.username
    user_dict["data_plan"] = user.data_plan
    user_dict["subscription_expires"] = user.subscription_expires
    user_dict["total_request"] = user.total_request
    user_dict["monthly_request"] = user.monthly_request
    user_dict["daily_request"] = user.daily_request
    user_dict["is_active"] = user.is_active
    user_dict["create_at"] = user.create_at
    user_dict["requests"] = user.requests
    user_dict["payments"] = user.payments
    user_dict["count_requests"] = len(user.requests)
    user_dict["count_payments"] = len(user.payments)
    return user_dict

async def disable_subscription(db: Session, user_id: int):
    logger.info("Disable subscription user_id=%s", user_id)
    subscription_expires = datetime.now() - timedelta(days=365)
    logger.info("DB request update user data plan user_id=%s", user_id)
    crud.update_user_data_plan(user_id, Data_Plan.FREE, subscription_expires, db)
    logger.info("DB successful response user_id=%s", user_id)

async def activate_subscription(user_id: int, plan: Data_Plan, db: Session):
    logger.info("Activating subscription user_id=%s plan=%s", user_id, plan)
    user_data = crud.get_user_tg_id(user_id, db)
    if user_data.date_plan == plan:
        subscription_expires = user_data.subscription_expires + timedelta(days=30)

        logger.info("DB request update_plan user_id=%s", user_id)
        crud.update_user_data_plan(user_id, plan, subscription_expires, db)
        logger.info("DB successful response update_plan user_id=%s", user_id)

    subscription_expires = datetime.now() + timedelta(days=30)

    logger.info("DB request update_plan user_id=%s", user_id)
    crud.update_user_data_plan(user_id, plan, subscription_expires, db)
    logger.info("DB successful response update_plan user_id=%s", user_id)

def get_activity_users(db: Session):
    logger.info("DB request get_activity_users")
    count_activity_users = crud.get_activity_users(db)
    logger.info("DB successful response get_activity_users")
    return count_activity_users




