from datetime import datetime

from sqlalchemy.orm import Session
import logging

from app.db import crud
from app.db.database import SessionLocal

logger = logging.getLogger(__name__)

def get_payments(db: Session):
    logger.info("DB request get_payments")
    payments = crud.get_payments(db)
    logger.info("DB successful response get_payments")
    return payments

def get_monthly_income(db: Session):
    logger.info("DB request get_monthly_income")
    income = crud.get_monthly_income(db)
    logger.info("DB successful response get_monthly_income")
    if len(income) == 0:
        return 0
    income = sum(list(map(lambda x: x[0], income))  )
    return income

def get_income_for_week(db: Session):
    income_for_week = crud.get_income_for_week(db)
    logger.info("get_income_for_week: income_for_week=%s", income_for_week)

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
        week[num_to_weekday[i]] = []

    for payment in income_for_week:
        day = payment.create_at.weekday()
        week[num_to_weekday[str(day)]].append(payment.amount)

    logger.info("get_income_for_week: week=%s", week)
    week = list(map(sum, list(week.values())))
    return week

def get_transactions(db: Session):
    payments = crud.get_transactions_sort_date(db)
    transactions = []
    for key, payment in enumerate(payments):
        transaction = {}
        transaction["id"] = key+1
        transaction["user_id"] = payment.user_id
        transaction["username"] = payment.user.username
        transaction["data_plan"] = payment.plan.value
        transaction["amount"] = payment.amount
        transaction["date"] = payment.create_at
        transactions.append(transaction)
    return transactions
