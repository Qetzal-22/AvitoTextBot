from fastapi import APIRouter, Depends, Request
import logging
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.templates import templates

request_router_api = APIRouter(prefix="/requests", tags=["requests"])
logger = logging.getLogger(__name__)

@request_router_api.get("/")
def get_request(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("requests.html", {"request": request})