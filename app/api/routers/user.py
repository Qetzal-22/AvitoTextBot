from fastapi import APIRouter, Depends, Request
import logging
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.templates import templates
from app.services.api_service import check_auth
from app.services import user_service

user_router_api = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

@user_router_api.get("/")
def get_users(request: Request, db: Session = Depends(get_db)):
    check_auth(request)
    users = user_service.get_users(db)
    data_users = enumerate(users)
    return templates.TemplateResponse("users.html", {"request": request, "users": data_users})

@user_router_api.get("/{id}")
def get_user(request: Request, db: Session = Depends(get_db), id: int = None):
    check_auth(request)
    user = user_service.get_user_dict_form(db, id)
    view_data = {
        "id": "ID",
        "tg_id": "Telegram ID",
        "username": "Username",
        "data_plan": "Data plan",
        "subscription_expires": "Subscription expires",
        "total_request": "Total request",
        "monthly_request": "Monthly request",
        "daily_request": "Daily request",
        "is_active": "Is active",
        "create_at": "Create at"
    }
    return templates.TemplateResponse("user.html", {"request": request, "user": user, "view_data": view_data})