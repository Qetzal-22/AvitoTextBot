from fastapi import APIRouter, Depends, Request
import logging
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.templates import templates

payment_router_api = APIRouter(prefix="/payments", tags=["payments"])
logger = logging.getLogger(__name__)

@payment_router_api.get("/")
def get_payments(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("payments.html", {"request": request})