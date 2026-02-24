import uuid
from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message

from sqlalchemy.orm import Session

from app.config.config import DATA_PLAN
from app.db import crud
from app.db.models import Status_Pay, Data_Plan
from app.utils.user import activate_subscription

payment_router_bot = Router()

@payment_router_bot.callback_query(F.data.startswith("new_data_plan:pay"))
async def data_plan_pay(callback: CallbackQuery, db: Session):
    await callback.answer()
    user_id = callback.message.from_user.id
    data_plan_type = callback.data.split(":")[2]
    data_plan = DATA_PLAN[f"{data_plan_type}"]

    payload = str(uuid.uuid4())
    amount = data_plan["amount"]

    crud.create_payment(payload, user_id, amount, Status_Pay.PENDING, Data_Plan(data_plan_type), db)

    prices = [LabeledPrice(label=f"{data_plan['title'].upper()} - подписка", amount=amount)]

    await callback.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=f"Подписка {data_plan['title'].upper()}",
        description="Подписка на 30 дней",
        payload=payload,
        currency="XTR",
        prices=prices
    )


@payment_router_bot.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True
    )

@payment_router_bot.message(F.successful_payment)
async def successful_payment(message: Message, db: Session):
    payload = message.successful_payment.invoice_payload
    payment = crud.get_payment(payload, db)

    if not payment:
        await message.answer("Ошибка платежа!")
        return

    if payment.status == Status_Pay.SUCCESS:
        await message.answer("Платеж уже прошел")
        return

    await activate_subscription(payment.plan)
    crud.update_payment_status(payload, Status_Pay.SUCCESS, db)

    await message.answer("✅ Подписка активирована")


