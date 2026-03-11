from fastapi import Request
from fastapi.responses import RedirectResponse

import logging

logger = logging.getLogger(__name__)

def check_auth(request: Request):
    logger.info("check_auth: session[auth]=%s", request.session.get("auth"))
    if not request.session.get("auth"):
        logger.info("check_auth: session[auth] is None")
        return RedirectResponse("/login")