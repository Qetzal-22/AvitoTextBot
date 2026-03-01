from aiogram import F, types, Bot
from aiogram.types import Message, BotCommand
from aiogram.filters import Command

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import asyncio
import logging

from app.bot.bot import bot, dp
from app.bot.handler.user import user_router_bot
from app.bot.handler.payments import payment_router_bot
from app.bot.keyboard import register_kb
from app.config.logging_config import setup_logging
from app.scheduler.jobs import check_subscriptions


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("<i>AvitoTextBot</i>\n<b>Зарегистрируйся Бабуин...</b>", parse_mode="HTML", reply_markup=await register_kb())


async def set_my_command(bot: Bot):
    command = [
        BotCommand(command="/start", description="Запуск AvitoBot"),
        BotCommand(command="/main", description="На главную")
    ]
    await bot.set_my_commands(command)

async def start_bot():
    await set_my_command(bot)
    dp.include_router(user_router_bot)
    dp.include_router(payment_router_bot)
    await dp.start_polling(bot)

async def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Vladivostok")

    scheduler.add_job(
        check_subscriptions,
        trigger=IntervalTrigger(seconds=60*60),
        kwargs={"bot": bot}
    )

    scheduler.start()


async def main():
    await asyncio.gather(
        start_bot(),
        start_scheduler()
    )

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Application started")
    asyncio.run(main())