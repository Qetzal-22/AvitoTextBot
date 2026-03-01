import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.models import Data_Plan
from app.db import crud


logger = logging.getLogger(__name__)