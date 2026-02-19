from aiogram.fsm.middleware import BaseMiddleware

from app.db.database import SessionLocal

class DBMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        db = SessionLocal()
        data["db"] = db

        try:
            return await handler(event, data)
        finally:
            db.close()
