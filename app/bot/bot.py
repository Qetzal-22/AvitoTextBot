from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
import os

from app.bot.middleware import DBMiddleware

load_dotenv()
bot = Bot(os.getenv("TOKEN_BOT_API"))
dp = Dispatcher(storage=MemoryStorage())
dp.update.middleware(DBMiddleware())