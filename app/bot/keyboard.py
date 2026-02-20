from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.config.config import CATEGORY

async def main_kb():
    bld = ReplyKeyboardBuilder()
    bld.button(text="Генерация текста")
    bld.button(text="Профиль")
    bld.button(text="Подписки")
    bld.adjust(1, 2)
    return bld.as_markup(resize_keyboard=True)

async def category_kb():
    bld = InlineKeyboardBuilder()
    for key, value in CATEGORY:
        bld.button(text=f"{value}", callback_data=f"{key}")
    return bld.as_markup()