from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import logging

from app.db.database import get_db
from app.api.templates import templates


login_router_api = APIRouter(prefix="/login", tags=["login"])
load_dotenv()
logger = logging.getLogger(__name__)

@login_router_api.get("/")
def login(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", {"request": request})

@login_router_api.post("/")
def loging(request: Request, password: str = Form(...)):
    true_password = os.getenv("PASSWORD_API")

    if password != true_password:
        logger.info("loging: password failed")
        return RedirectResponse(url="/login", status_code=303)

    logger.info("loging: password successful")
    request.session["auth"] = True
    return RedirectResponse(url="/dashboard", status_code=303)

@login_router_api.get("/reset")
def reset_loging(request: Request):
    request.session["auth"] = False
    return RedirectResponse("/login")