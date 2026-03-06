from sqlalchemy.orm import Session
import logging
from datetime import datetime

from app.db import crud
from app.db.database import SessionLocal

logger = logging.getLogger(__name__)

def get_requests(db: Session):
    logger.info("DB request get_requests")
    requests = crud.get_requests(db)
    logger.info("DB successful response get_requests")
    return requests

def get_request_today(db: Session):
    logger.info("DB Request get_request_today")
    request_today = crud.get_today_requests(db)
    logger.info("DB successful response get_request_today")
    return request_today

def get_request_for_week(db: Session):
    request_for_week = crud.get_request_for_week(db)
    logger.info("get_request_for_week: request_for_week=%s", request_for_week)

    today_weekday = datetime.now().weekday()+1
    num_to_weekday = {
        "0": "Mon",
        "1": "Tue",
        "2": "Web",
        "3": "The",
        "4": "Fri",
        "5": "Sat",
        "6": "Sun"
    }
    data = [str((i % 7)) for i in range(today_weekday, today_weekday + 7)]
    week = {}
    for i in data:
        week[num_to_weekday[i]] = 0

    for request in request_for_week:
        day = request.create_at.weekday()
        week[num_to_weekday[str(day)]] += 1

    logger.info("get_request_for_week: week=%s", week)
    return list(week.values())

def get_requests_ai(db: Session):
    requests = crud.get_requests_sort_date(db)
    requests_ai = []
    for key, request in enumerate(requests):
        logger.info("get_requests_ai: request.id=%s request.user_id=%s", request.id, request.user_id)
        logger.info("get_requests_ai: request.user=%s", request.user)
        request_ai = {}
        request_ai["id"] = key+1
        request_ai["user_id"] = request.user_id
        request_ai["username"] = request.user.username
        request_ai["len_req"] = len(request.request)
        request_ai["date"] = request.create_at
        requests_ai.append(request_ai)
    return requests_ai
