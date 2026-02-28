import uuid
from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message

from sqlalchemy.orm import Session
import logging

from app.config.config import DATA_PLAN
from app.db import crud
from app.db.models import Status_Pay, Data_Plan
from app.utils.user import activate_subscription

payment_router_bot = Router()

logger = logging.getLogger(__name__)

@payment_router_bot.callback_query(F.data.startswith("new_data_plan:pay"))
async def data_plan_pay(callback: CallbackQuery, db: Session):
    logger.info("Payment process started user_id=%s", callback.message.from_user.id)
    await callback.answer()
    user_id = callback.message.from_user.id
    data_plan_type = callback.data.split(":")[2]
    logger.info("User selected plan - %s, user_id=%s", data_plan_type, user_id)
    if data_plan_type not in DATA_PLAN:
        logger.warning("Data plan type not found in DATA_PLAN user_id=%s", user_id)
        await callback.message.answer("Ошибка выбора тарифа")
        return

    data_plan = DATA_PLAN[f"{data_plan_type}"]

    payload = str(uuid.uuid4())
    amount = data_plan["amount"]

    logger.info("Creating payment record user_id=%s", user_id)
    crud.create_payment(payload, user_id, amount, Status_Pay.PENDING, Data_Plan(data_plan_type), db)
    logger.info("create_payment succeeded user_id=%s", user_id)

    prices = [LabeledPrice(label=f"{data_plan['title'].upper()} - подписка", amount=amount)]

    logger.info("Create invoice user_id=%s", user_id)
    await callback.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=f"Подписка {data_plan['title'].upper()}",
        description="Подписка на 30 дней",
        payload=payload,
        currency="XTR",
        prices=prices
    )
    logger.info("Send invoice for user user_id=%s", user_id)


@payment_router_bot.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    logger.info("Pre_checkout confirmed user_id=%s", pre_checkout_query.from_user.id)
    await pre_checkout_query.bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True
    )

@payment_router_bot.message(F.successful_payment)
async def successful_payment(message: Message, db: Session):
    user_id = message.from_user.id
    logger.info("Handler payment_successful for user user_id=%s", user_id)
    payload = message.successful_payment.invoice_payload
    payment = crud.get_payment(payload, db)

    if not payment:
        logger.error("Payment record not found, payload=%s, user_id=%s", payload, user_id)
        await message.answer("Ошибка платежа!")
        return

    if payment.status == Status_Pay.SUCCESS:
        logger.warning("Payment already confirmed user_id=%s", user_id)
        await message.answer("Платеж уже прошел")
        return

    if message.successful_payment.total_amount != payment.amount:
        logger.error("Payment amount mismatch user_id=%s payload=%s", user_id, payload)
        await message.answer("Ошибка суммы платежа")
        return

    if message.successful_payment.currency != "XTR":
        logger.error("Payment incorrect currency user_id=%s payload=%s", user_id, payload)
        await message.answer("Ошибка валюты")
        return

    logger.info("Activating subscription plan=%s, user_id=%s", payment.plan, user_id)
    try:
        await activate_subscription(user_id, payment.plan)
    except:
        logger.exception("Error activate subscription")
        await message.answer("Ошибка активации подписки")
        return

    logger.info("Started request db update_payment_status user_id=%s", user_id)
    crud.update_payment_status_success(payload, db)
    logger.info("update_payment_status succeeded user_id=%s", user_id)

    logger.info("Subscription activated user_id=%s", user_id)
    await message.answer("✅ Подписка активирована")


