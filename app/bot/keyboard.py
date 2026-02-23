from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import logging

from app.config.config import CATEGORY, EQUIPMENTS

logger = logging.getLogger(__name__)


async def main_kb():
    bld = ReplyKeyboardBuilder()
    bld.button(text="Генерация текста")
    bld.button(text="Профиль")
    bld.button(text="Подписки")
    bld.adjust(1, 2)
    return bld.as_markup(resize_keyboard=True)

async def category_kb():
    bld = InlineKeyboardBuilder()
    for key, value in CATEGORY.items():
        bld.button(text=f"{value}", callback_data=f"{key}")
    bld.adjust(1)
    return bld.as_markup()

async def equipment_kb(message_id: int, equipments: list):
    bld = InlineKeyboardBuilder()
    for key, equipment in EQUIPMENTS.items():
        if key in equipments:
            bld.button(text=f"{equipment}✅", callback_data=f"equipment:{key}:{message_id}")
        else:
            bld.button(text=f"{equipment}", callback_data=f"equipment:{key}:{message_id}")

    bld.button(text="Подтвердить✅", callback_data="equipment_success")
    bld.adjust(2, 1, 1, 1, 1, 2)
    return bld.as_markup()

async def profile_kb():
    bld = ReplyKeyboardBuilder()
    bld.button(text="Поменять тариф")
    bld.button(text="Назад")
    bld.adjust(1, 1)
    return bld.as_markup()

async def data_plan_kb():
    bld = InlineKeyboardBuilder()
    bld.button(text="PRO", callback_data="new_data_plan:pro")
    bld.button(text="PREMIUM", callback_data="new_data_plan:premium")
    bld.adjust(1, 1, 1)
    return bld.as_markup()