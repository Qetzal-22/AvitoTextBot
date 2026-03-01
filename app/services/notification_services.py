from aiogram import Bot

from app.bot.keyboard import data_plan_kb


async def send_notification_ended_sub(bot: Bot, chat_id: int):
    await bot.send_message(
        chat_id=chat_id,
        text="У вас закончилась подписка.\nОбновите ее и продолжайте пользоватся преемуществами <i>AvitoTextBot</i>",
        parse_mode="HTML",
        reply_markup=await data_plan_kb()
    )
