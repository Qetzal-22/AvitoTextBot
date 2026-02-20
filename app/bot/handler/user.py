from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
import logging

from app.bot.static import RegisterUser
from app.bot.keyboard import main_kb, category_kb
from app.db import crud
from app.config.config import CATEGORY

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
    await to_main(message)


############################################################################################################################
################################################ main ######################################################################
############################################################################################################################
@user_router_bot.message(Command("main"))
async def to_main(message: Message):
    await message.answer("Main panel", reply_markup=await main_kb())


############################################### generate text ##############################################################
@user_router_bot.message(F.text.casefold().endswith("генерация текста"))
async def text_generate_handler(message: Message):
    await message.answer("Выберите категорию в которой хотите продать товар:", reply_markup=await category_kb())

@user_router_bot.callback_query(F.data.startswith("car"))
async def text_generate_get_category(callback: CallbackQuery):
    await callback.message.answer("Выбрана категория автомобили")



############################################### profil #####################################################################



############################################### data plan ##################################################################




############################################################################################################################
############################################################################################################################
############################################################################################################################
