from aiohttp import request
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
import logging
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.templates import templates
from app.services import finance_service
from app.services.api_service import check_auth
from app.db.models import Data_Plan, Status_Pay

payment_router_api = APIRouter(prefix="/payments", tags=["payments"])
logger = logging.getLogger(__name__)

@payment_router_api.get("/")
def get_payments(request: Request, db: Session = Depends(get_db)):
    auth = check_auth(request)
    if auth:
        return auth

    payments = finance_service.get_payments(db)
    payments_data = enumerate(payments)
    return templates.TemplateResponse("payments.html", {"request": request, "payments": payments_data})

@payment_router_api.get("/{id}")
def get_payment(request: Request, db: Session = Depends(get_db), id: int = None):
    auth = check_auth(request)
    if auth:
        return auth

    payment = finance_service.get_payment(db, id)
    return templates.TemplateResponse("payment.html", {"request": request, "payment": payment})

@payment_router_api.post("/edit-product")
def change_product(request: Request, payment_id: int = Form(...), product: Data_Plan = Form(...), db: Session = Depends(get_db)):
    auth = check_auth(request)
    if auth:
        return auth

    finance_service.update_product(db, payment_id, product)
    return RedirectResponse(url=f"/payments/{payment_id}", status_code=303)

@payment_router_api.post("/edit-status")
def change_status(request: Request, payment_id: int = Form(...), status: Status_Pay = Form(...), db: Session = Depends(get_db)):
    auth = check_auth(request)
    if auth:
        return auth

    finance_service.update_status(db, payment_id, status)
    return RedirectResponse(url=f"/payments/{payment_id}", status_code=303)