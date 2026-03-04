from fastapi import APIRouter, Depends, Request
import logging
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.templates import templates
from app.services import user_service

user_router_api = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

@user_router_api.get("/")
def get_users(request: Request, db: Session = Depends(get_db)):
    users = user_service.get_users(db)
    data_users = enumerate(users)
    return templates.TemplateResponse("users.html", {"request": request, "users": data_users})