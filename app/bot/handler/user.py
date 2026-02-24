from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
import logging

from app.bot.static import RegisterUser
from app.bot.keyboard import main_kb, category_kb, equipment_kb, profile_kb, data_plan_kb, data_plan_pay_kb
from app.bot.static import GetDataForCar
from app.db import crud
from app.db.models import Data_Plan
from app.config.config import DATA_PLAN

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
    await message.answer("Гавная:", reply_markup=await main_kb())


############################################### generate text ##############################################################
@user_router_bot.message(F.text.casefold().endswith("генерация текста"))
async def text_generate_handler(message: Message):
    await message.answer("Выберите категорию в которой хотите продать товар:", reply_markup=await category_kb())

@user_router_bot.callback_query(F.data.startswith("car"))
async def text_generate_get_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Выбрана категория автомобили")
    await state.set_state(GetDataForCar.car_make)
    await callback.message.answer("Введите марку авто:")

    await state.update_data(equipment=[])

@user_router_bot.message(GetDataForCar.car_make)
async def text_generate_get_mark(message: Message, state: FSMContext):
    make_car = message.text
    await state.update_data(make_car=make_car)
    await message.answer("Введите модель автомобиля:")
    await state.set_state(GetDataForCar.model)

@user_router_bot.message(GetDataForCar.model)
async def text_generate_get_model(message: Message, state: FSMContext):
    model = message.text
    await state.update_data(model=model)

    await message.answer("Введите год выпуска:")
    await state.set_state(GetDataForCar.year_manufacture)

@user_router_bot.message(GetDataForCar.year_manufacture)
async def text_generate_get_year_manufacture(message: Message, state: FSMContext):
    year_manufacture = message.text
    await state.update_data(year_manufacture=year_manufacture)

    await message.answer("Введите пробег:")
    await state.set_state(GetDataForCar.mileage)

@user_router_bot.message(GetDataForCar.mileage)
async def text_generate_get_mileage(message: Message, state: FSMContext):
    mileage = message.text
    await state.update_data(mileage=mileage)

    await message.answer("Введите кол-во владельцев:")
    await state.set_state(GetDataForCar.count_owner)

@user_router_bot.message(GetDataForCar.count_owner)
async def text_generate_get_count_owner(message: Message, state: FSMContext):
    count_owner = message.text
    await state.update_data(count_owner=count_owner)

    await message.answer("Введите кол-во ДТП:")
    await state.set_state(GetDataForCar.count_accidents)

@user_router_bot.message(GetDataForCar.count_accidents)
async def text_generate_get_count_accidents(message: Message, state: FSMContext):
    count_accidents = message.text
    await state.update_data(count_accidents=count_accidents)

    await message.answer("Опишите состояние корпуса состояние корпуса:")
    await state.set_state(GetDataForCar.body_condition)

@user_router_bot.message(GetDataForCar.count_accidents)
async def text_generate_get_count_accidents(message: Message, state: FSMContext):
    count_accidents = message.text
    await state.update_data(count_accidents=count_accidents)

    await message.answer("Опишите состояние корпуса:")
    await state.set_state(GetDataForCar.body_condition)

@user_router_bot.message(GetDataForCar.body_condition)
async def text_generate_get_body_condition(message: Message, state: FSMContext):
    body_condition = message.text
    await state.update_data(body_condition=body_condition)

    await message.answer("Опишите состояние двигателя:")
    await state.set_state(GetDataForCar.engine_condition)

@user_router_bot.message(GetDataForCar.engine_condition)
async def text_generate_get_engine_condition(message: Message, state: FSMContext):
    bot = message.bot
    engine_condition = message.text
    await state.update_data(engine_condition=engine_condition)

    bot_message = await message.answer("Выберете имеющиеся у вас комплектующие: ")
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=bot_message.message_id,
        reply_markup=await equipment_kb(bot_message.message_id, [])
    )



@user_router_bot.callback_query(F.data.startswith("equipment_success"))
async def text_generate_get_equipment(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Напишите причину продажи: ")
    await state.set_state(GetDataForCar.reason_for_sale)


@user_router_bot.callback_query(F.data.startswith("equipment"))
async def text_generate_add_equipment(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    equipment = callback.data.split(":")[1]
    message_id = int(callback.data.split(":")[2])
    bot = callback.bot
    data = await state.get_data()

    if equipment in data["equipment"]:
        data["equipment"].remove(equipment)
        new_equipments = data["equipment"]
    else:
        new_equipments = data["equipment"] + [equipment]
    logger.info(f"new_equipment - {new_equipments}")

    await state.update_data(equipment=new_equipments)
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=message_id,
        reply_markup=await equipment_kb(message_id, new_equipments)
    )

@user_router_bot.message(GetDataForCar.reason_for_sale)
async def text_generate_get_reason_for_sale(message: Message, state: FSMContext):
    reason_for_sale = message.text
    await state.update_data(reason_for_sale=reason_for_sale)

    await message.answer('Если хотите добавить чтото еще напишите через запятую.\nЕсли нет, напишите "нет":')
    await state.set_state(GetDataForCar.additional)

@user_router_bot.message(GetDataForCar.additional)
async def text_generate_get_additional(message: Message, state: FSMContext):
    additional = message.text
    await state.update_data(additional=additional)
    await message.answer("Обрабатываю данные...")

    # request AI

    await state.clear()


############################################### profile ####################################################################

@user_router_bot.message(F.text.casefold().endswith("профиль"))
async def to_profile(message: Message, db: Session):
    data_user = crud.get_user_tg_id(message.from_user.id, db)
    subscription_expires = data_user.subscription_expires
    logger.info(f"data_user data_plat type - {type(data_user.data_plan)}")
    if data_user.subscription_expires is None:
        subscription_expires = "-"
    text = (
        "👤 <b>Профиль пользователя</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"

        f"👤 <b>Username:</b>\n"
        f"{data_user.username}\n\n"

        f"💎 <b>Тариф:</b>\n"
        f"{data_user.data_plan.value.upper()}\n\n"

        f"📅 <b>Подписка до:</b>\n"
        f"{subscription_expires}\n\n"

        f"📊 <b>Запросов в этом месяце:</b>\n"
        f"{data_user.monthly_request}\n\n"

        "━━━━━━━━━━━━━━━━━━\n"
        "<i>Avito Text Bot</i>"
    )

    await message.answer(text, reply_markup=await profile_kb(), parse_mode="HTML")

############################################### data plan ##################################################################

@user_router_bot.message(F.text.casefold().in_(["подписки", "поменять тариф"]))
async def to_data_plan(message: Message, db: Session):
    data_user = crud.get_user_tg_id(message.from_user.id, db)
    subscription_expires = data_user.subscription_expires
    logger.info(f"data_user data_plat type - {type(data_user.data_plan)}")
    if data_user.subscription_expires is None:
        subscription_expires = "-"
    text = (
        "💎 <b>Тарифные планы</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
    )

    for key, plan in DATA_PLAN.items():

        # Эмодзи для каждого тарифа
        if key == "free":
            emoji = "🆓"
        elif key == "pro":
            emoji = "🚀"
        elif key == "premium":
            emoji = "👑"
        else:
            emoji = "📦"

        text += (
            f"{emoji} <b>{plan['title']}</b>\n"
            "━━━━━━━━━━━━\n"
            f"💰 Стоимость: {plan['amount']} ₽\n"
            f"📊 Лимит запросов: {plan['count_request']} / день\n\n\n"
        )

    text += "━━━━━━━━━━━━━━━━━━\n<i>Avito Text Bot</i>"

    await message.answer(text, reply_markup=await data_plan_kb(), parse_mode="HTML")


@user_router_bot.callback_query(F.data.startswith("new_data_plan:view"))
async def data_plan_pro(callback: CallbackQuery):
    await callback.answer()
    data_plan_type = callback.data.split(":")[2]
    pro_data = DATA_PLAN[f"{data_plan_type}"]
    await callback.message.answer(
        f"🚀<b>{data_plan_type.upper()}</b>\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💰 <b>Цена: </b>\n"
        f"{pro_data['amount']}\n"
        "📊 <b>Запросов/день: </b>\n"
        f"{pro_data['count_request']} ₽\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "<i>Avito Text Bot</i>",
        reply_markup=await data_plan_pay_kb(data_plan_type),
        parse_mode="HTML"
    )

@user_router_bot.callback_query(F.data.startswith("new_data_plan:pay"))
async def data_plan_pay(callback: CallbackQuery):
    await callback.answer()
    data_plan_type = callback.data.split(":")[2]


############################################################################################################################

@user_router_bot.message(F.text.casefold().endswith("назад на главную"))
async def back_main(message: Message):
    return await to_main(message)


############################################################################################################################
############################################################################################################################
############################################################################################################################
