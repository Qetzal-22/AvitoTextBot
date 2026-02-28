from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
import logging
from datetime import datetime

from app.bot.static import RegisterUser
from app.bot.keyboard import main_kb, category_kb, equipment_kb, profile_kb, data_plan_kb, data_plan_pay_kb, register_kb
from app.bot.static import GetDataForCar
from app.ai.request import AI
from app.db import crud
from app.db.models import Data_Plan
from app.config.config import DATA_PLAN

logger = logging.getLogger(__name__)
user_router_bot = Router()

ai = AI()

@user_router_bot.message(Command("register"))
async def register(message: Message, state: FSMContext, db: Session):
    user_id = message.from_user.id
    logger.info(f"Function register called for user_id=%s", user_id)
    logger.info("DB request get_user user_id=%s", user_id)
    user = crud.get_user_tg_id(user_id, db)
    logger.info("DB response get_user user_id=%s", user_id)
    if not user is None:
        logger.warning(f"User already register user_id=%s", user_id)
        await message.answer(f"Вы уже зарегистрированны!")
        return
    await message.answer("Регистрация")
    return await starting_register(message, state)


async def starting_register(message, state):
    logger.info("Started register user_id=%s", message.from_user.id)
    await message.answer("Напиши свой username: ")
    await state.set_state(RegisterUser.username)


@user_router_bot.message(RegisterUser.username)
async def get_username(message: Message, state: FSMContext, db: Session):
    user_id = message.from_user.id
    username = message.text
    if len(username) > 30:
        logger.warning("User entered username is too long user_id=%s", user_id)
        await message.answer("Длина username не должна превышать 30 символов!")
        await message.answer("Попробуйте снова")
        return await starting_register(message, state)
    for ch in username:
        if ch in " ,.":
            logger.warning("User entered username with bad symbol user_id=%s", user_id)
            await message.answer("Вы ввели запрещенный символ (\" \",.)!")
            await message.answer("Попробуйте снова")
            return await starting_register(message, state)
    logger.info("User entered username user_id=%s", user_id)
    logger.info("Creating user user_id=%s", user_id)
    crud.create_user(user_id, username, db)
    logger.info("Create user record user_id=%s", user_id)
    await state.clear()
    logger.info("User register successful user_id=%s", user_id)
    await message.answer("Вы успешно зарегистрированны")
    await to_main(message)


############################################################################################################################
################################################ main ######################################################################
############################################################################################################################
@user_router_bot.message(Command("main"))
async def to_main(message: Message, db: Session):
    user_id = message.from_user.id
    logger.info("Function to_main called for user_id=%s", user_id)
    logger.info("DB request get_user user_id=%s", user_id)
    user = crud.get_user_tg_id(user_id, db)
    logger.info("DB response get_user user_id=%s", user_id)
    if user is None:
        logger.warning(f"User not found in DB user_id=%s", user_id)
        await message.answer(f"Вы не зарегистрированны!", reply_markup=await register_kb())
        return
    await message.answer("Гавная:", reply_markup=await main_kb())


############################################### generate text ##############################################################
@user_router_bot.message(F.text.casefold().endswith("генерация текста"))
async def text_generate_handler(message: Message, db: Session):
    user_id = message.from_user.id
    logger.info("Getting data for text generate user_id=%s", user_id)
    logger.info("DB request get_user user_id=%s", user_id)
    user = crud.get_user_tg_id(user_id, db)
    logger.info("DB response get_user user_id=%s", user_id)
    if user is None:
        logger.warning(f"User not found in DB user_id=%s", user_id)
        await message.answer(f"Вы не зарегистрированны!", reply_markup=await register_kb())
        return
    await message.answer("Выберите категорию в которой хотите продать товар:", reply_markup=await category_kb())

@user_router_bot.callback_query(F.data.startswith("car"))
async def text_generate_get_category(callback: CallbackQuery, state: FSMContext):
    logger.info("User choose category - car, user_id=%s", callback.message.from_user.id)
    await callback.answer()
    await callback.message.answer("Выбрана категория автомобили")
    await state.update_data(category="car")
    await state.set_state(GetDataForCar.car_make)
    await callback.message.answer("Введите марку авто:")

    await state.update_data(equipment=[])

@user_router_bot.message(GetDataForCar.car_make)
async def text_generate_get_mark(message: Message, state: FSMContext):
    car_make = message.text
    logger.info("User %s entered car make", message.from_user.id)
    await state.update_data(car_make=car_make)
    await message.answer("Введите модель автомобиля:")
    await state.set_state(GetDataForCar.model)

@user_router_bot.message(GetDataForCar.model)
async def text_generate_get_model(message: Message, state: FSMContext):
    model = message.text
    logger.info("User %s entered model", message.from_user.id)
    await state.update_data(model=model)

    await message.answer("Введите год выпуска:")
    await state.set_state(GetDataForCar.year_manufacture)

@user_router_bot.message(GetDataForCar.year_manufacture)
async def text_generate_get_year_manufacture(message: Message, state: FSMContext):
    user_id = message.from_user.id
    year_manufacture = message.text
    if not year_manufacture.isdigit():
        logger.warning("User entered incorrect format year! user_id=%s", user_id)
        await message.answer("Вы ввели неверный формат года.\nВ году не должно быть никаких символов кроме чисел!")
        await message.answer("Попробуйте снова:")
        await state.set_state(GetDataForCar.year_manufacture)
        return
    if 1894 > int(year_manufacture) > datetime.now().year:
        logger.warning("User entered incorrect format year! user_id=%s", user_id)
        await message.answer(f"Вы ввели неверный формат года.\nГод должен быть цифрой в пределе от 1894 до {datetime.now().year} включительно.")
        await message.answer("Попробуйте снова:")
        await state.set_state(GetDataForCar.year_manufacture)
        return
    logger.info("User %s entered year_manufacture", user_id)
    await state.update_data(year_manufacture=year_manufacture)

    await message.answer("Введите пробег:")
    await state.set_state(GetDataForCar.mileage)

@user_router_bot.message(GetDataForCar.mileage)
async def text_generate_get_mileage(message: Message, state: FSMContext):
    user_id = message.from_user.id
    mileage = message.text
    if not mileage.isdigit():
        logger.warning("User entered incorrect format mileage! user_id=%s", user_id)
        await message.answer("Вы ввели неверный формат пробега.\nВ пробеге не должно быть никаких символов кроме чисел!")
        await message.answer("Попробуйте снова:")
        await state.set_state(GetDataForCar.mileage)
        return
    if 0 > int(mileage):
        logger.warning("User entered incorrect format mileage! user_id=%s", user_id)
        await message.answer(f"Вы ввели неверный формат года.\nПробег не может быть ниже 0.")
        await message.answer("Попробуйте снова:")
        await state.set_state(GetDataForCar.mileage)
        return

    logger.info("User %s entered mileage", user_id)
    await state.update_data(mileage=mileage)

    await message.answer("Введите кол-во владельцев:")
    await state.set_state(GetDataForCar.count_owner)

@user_router_bot.message(GetDataForCar.count_owner)
async def text_generate_get_count_owner(message: Message, state: FSMContext):
    user_id = message.from_user.id
    count_owner = message.text
    if not count_owner.isdigit():
        logger.warning("User entered incorrect format count_owner! user_id=%s", user_id)
        await message.answer("Вы ввели неверный формат количества владельцев.\nВ числе владельцев не должно быть никаких символов кроме чисел!")
        await message.answer("Попробуйте снова:")
        await state.set_state(GetDataForCar.count_owner)
        return
    if 0 > int(count_owner):
        logger.warning("User entered incorrect format count_owner! user_id=%s", user_id)
        await message.answer(f"Вы ввели неверный формат количества владельцев.\nЧисло владельцев не может быть ниже 0.")
        await message.answer("Попробуйте снова:")
        await state.set_state(GetDataForCar.count_owner)
        return

    logger.info("User %s entered count_owner", user_id)
    await state.update_data(count_owner=count_owner)
    await message.answer("Введите кол-во ДТП:")
    await state.set_state(GetDataForCar.count_accidents)

@user_router_bot.message(GetDataForCar.count_accidents)
async def text_generate_get_count_accidents(message: Message, state: FSMContext):
    user_id = message.from_user.id
    count_accidents = message.text
    if not count_accidents.isdigit():
        logger.warning("User entered incorrect format count_accidents! user_id=%s", user_id)
        await message.answer("Вы ввели неверный формат количества ДТП.\nВ числе ДТП не должно быть никаких символов кроме чисел!")
        await message.answer("Попробуйте снова:")
        await state.set_state(GetDataForCar.count_accidents)
        return
    if 0 > int(count_accidents):
        logger.warning("User entered incorrect format count_accidents! user_id=%s", user_id)
        await message.answer(f"Вы ввели неверный формат количества ДТП.\nЧисло ДТП не может быть ниже 0.")
        await message.answer("Попробуйте снова:")
        await state.set_state(GetDataForCar.count_accidents)
        return
    logger.info("User %s entered count_accidents", message.from_user.id)
    await state.update_data(count_accidents=count_accidents)

    await message.answer("Опишите состояние корпуса:")
    await state.set_state(GetDataForCar.body_condition)


@user_router_bot.message(GetDataForCar.body_condition)
async def text_generate_get_body_condition(message: Message, state: FSMContext):
    body_condition = message.text
    logger.info("User %s entered body_condition", message.from_user.id)
    await state.update_data(body_condition=body_condition)

    await message.answer("Опишите состояние двигателя:")
    await state.set_state(GetDataForCar.engine_condition)

@user_router_bot.message(GetDataForCar.engine_condition)
async def text_generate_get_engine_condition(message: Message, state: FSMContext):
    bot = message.bot
    engine_condition = message.text
    logger.info("User %s entered engine_condition", message.from_user.id)
    await state.update_data(engine_condition=engine_condition)

    bot_message = await message.answer("Выберете имеющиеся у вас комплектующие: ")
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=bot_message.message_id,
        reply_markup=await equipment_kb(bot_message.message_id, [])
    )



@user_router_bot.callback_query(F.data.startswith("equipment_success"))
async def text_generate_get_equipment(callback: CallbackQuery, state: FSMContext):
    logger.info("equipment success")
    await callback.answer()
    await callback.message.answer("Напишите причину продажи: ")
    await state.set_state(GetDataForCar.reason_for_sale)


@user_router_bot.callback_query(F.data.startswith("equipment"))
async def text_generate_add_equipment(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    equipment = callback.data.split(":")[1]
    logger.info("User %s click equipment - %s", callback.message.from_user.id, equipment)
    message_id = int(callback.data.split(":")[2])
    bot = callback.bot
    data = await state.get_data()

    if equipment in data["equipment"]:
        data["equipment"].remove(equipment)
        new_equipments = data["equipment"]
    else:
        new_equipments = data["equipment"] + [equipment]
    logger.info("new_equipment - %s", new_equipments)

    await state.update_data(equipment=new_equipments)
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=message_id,
        reply_markup=await equipment_kb(message_id, new_equipments)
    )

@user_router_bot.message(GetDataForCar.reason_for_sale)
async def text_generate_get_reason_for_sale(message: Message, state: FSMContext):
    reason_for_sale = message.text
    logger.info("User %s entered reason_for_sale", message.from_user.id)
    await state.update_data(reason_for_sale=reason_for_sale)

    await message.answer('Если хотите добавить чтото еще напишите через запятую.\nЕсли нет, напишите "нет":')
    await state.set_state(GetDataForCar.additional)

@user_router_bot.message(GetDataForCar.additional)
async def text_generate_get_additional(message: Message, state: FSMContext):
    additional = message.text
    logger.info("User %s entered additional", message.from_user.id)
    await state.update_data(additional=additional)
    data = await state.get_data()
    text = "Processes Data: "
    for key, value in data.items():
        text += f"\n{key}: {value}"
    await message.answer(text)

    # request AI
    logger.info("AI request started for user %s", message.from_user.id)
    resp = await ai.get_avito_text(data)

    logger.info("AI response received for user - %s, length response - %s", message.from_user.id, len(resp))
    await message.answer(resp)

    await state.clear()


############################################### profile ####################################################################

@user_router_bot.message(F.text.casefold().endswith("профиль"))
async def to_profile(message: Message, db: Session):
    user_id = message.from_user.id
    logger.info("Function to_profile called for user %s", user_id)
    logger.info("DB request get_user user_id=%s", user_id)
    user = crud.get_user_tg_id(user_id, db)
    logger.info("DB response get_user user_id=%s", user_id)
    if user is None:
        logger.warning(f"User not found in DB user_id=%s", user_id)
        await message.answer(f"Вы не зарегистрированны!", reply_markup=await register_kb())
        return
    logger.info("Request in db get user user_id=%s", user_id)
    data_user = crud.get_user_tg_id(message.from_user.id, db)
    logger.info("get_user succeeded user_id=%s", user_id)
    subscription_expires = data_user.subscription_expires
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
    user_id = message.from_user.id
    logger.info("Function to_data_plan called user_id=%s", user_id)
    logger.info("DB request get_user user_id=%s", user_id)
    user = crud.get_user_tg_id(user_id, db)
    logger.info("DB response get_user user_id=%s", user_id)
    if user is None:
        logger.warning(f"User not found in DB user_id=%s", user_id)
        await message.answer(f"Вы не зарегистрированны!", reply_markup=await register_kb())
        return
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
async def view_data_plan(callback: CallbackQuery):
    user_id = callback.message.from_user.id
    logger.info("Function view_data_plan called user_id=%s", user_id)
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


############################################################################################################################

@user_router_bot.message(F.text.casefold().endswith("назад на главную"))
async def back_main(message: Message):
    logger.info("Function back_main called user_id=%s", message.from_user.id)
    return await to_main(message)

@user_router_bot.callback_query(F.data.startswith("register"))
async def process_register_callback(callback: CallbackQuery, state: FSMContext, db: Session):
    logger.info("Function back_main called user_id=%s", callback.message.from_user.id)
    await callback.answer()
    return await register(callback.message, state, db)

############################################################################################################################
############################################################################################################################
############################################################################################################################
