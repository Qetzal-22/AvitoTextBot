import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.models import Data_Plan
from app.db import crud


logger = logging.getLogger(__name__)

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