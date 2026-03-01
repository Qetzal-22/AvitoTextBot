import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db import crud
from app.db.models import Data_Plan

logger = logging.getLogger(__name__)

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