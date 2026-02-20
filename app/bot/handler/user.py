from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
import logging

from app.bot.static import RegisterUser
from app.db import crud

logger = logging.getLogger(__name__)
user_router_bot = Router()

@user_router_bot.message(Command("register"))
async def register(message: Message, state: FSMContext):
    await message.answer("Регистрация")
    await message.answer("Напиши свой username: ")
    await state.set_state(RegisterUser.username)

@user_router_bot.message(RegisterUser.username)
async def get_username(message: Message, state: FSMContext, db: Session):
    tg_id = message.from_user.id
    username = message.text
    crud.create_user(tg_id, username, db)
    await state.clear()
    logger.info("User success register")
    await message.answer("Вы успешно зарегистрированны")

@user_router_bot.message(Command("/main"))
async def to_main(message: Message):
    await message.answer("Main panel")