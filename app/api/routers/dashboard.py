import logging

from fastapi import APIRouter, Depends, Request

from sqlalchemy.orm import Session
import logging

from app.api.templates import templates
from app.db.database import get_db
from app.services.user_service import get_activity_users
from app.services.finance_service import get_monthly_income, get_income_for_week, get_transactions
from app.services.request_service import get_request_today, get_request_for_week, get_requests_ai
from app.services.api_service import check_auth
from app.utils.datetime_utils import get_weekday_start_now

dashboard_router_api = APIRouter(prefix="/dashboard", tags=["dashboard"])

logger = logging.getLogger(__name__)

@dashboard_router_api.get("/")
def get_dashboard(request: Request, db: Session = Depends(get_db)):
    check_auth(request)
    activity_users = get_activity_users(db)
    monthly_income = get_monthly_income(db)
    request_today = get_request_today(db)
    logger.info("get_dashboard: activity_users=%s", activity_users)
    logger.info("get_dashboard: monthly_income=%s", monthly_income)
    logger.info("get_dashboard: request_today=%s", request_today)


    weekdays = get_weekday_start_now()
    income_for_week = get_income_for_week(db)
    request_for_week = get_request_for_week(db)
    logger.info("get_dashboard: income_for_week=%s", income_for_week)
    logger.info("get_dashboard: request_for_week=%s", request_for_week)

    transactions = get_transactions(db)
    requests_ai = get_requests_ai(db)
    logger.info("get_dashboard: transactions=%s", transactions)
    logger.info("get_dashboard: requests_ai=%s", requests_ai)



    return templates.TemplateResponse("dashboard.html",
                                      {
                                          "request": request,
                                          "activity_users": activity_users,
                                          "monthly_income": monthly_income,
                                          "request_today": request_today,
                                          "weekdays": weekdays,
                                          "income_for_week": income_for_week,
                                          "request_for_week": request_for_week,
                                          "transactions": transactions,
                                          "requests_ai": requests_ai,
                                      })