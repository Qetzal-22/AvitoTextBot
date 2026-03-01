from aiogram import Bot
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.db import crud
from app.db.database import SessionLocal
from app.services.user_services import disable_subscription
from app.services.notification_services import send_notification_ended_sub

logger = logging.getLogger(__name__)

async def check_subscriptions(bot: Bot):
    logger.info("Start check subscription")
    db = SessionLocal()
    try:
        users_data = crud.get_users_end_sub(db)
        logger.info("Found %s expired subscription", len(users_data))
        for user_data in users_data:
            try:
                user_id = user_data.tg_id
                await disable_subscription(db, user_id)
                await send_notification_ended_sub(bot, user_id)
            except Exception:
                logger.error("Error in check_subscription user_id=%s", user_id, exc_info=True)
                continue
            logger.info("Successful disable subscription user_id=%s", user_id)
    finally:
        db.close()
        logger.info("Finished check subscription")