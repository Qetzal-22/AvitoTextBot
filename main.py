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
from app.scheduler.jobs import check_subscriptions, reset_monthly_requests, reset_daily_requests


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "<i>AvitoTextBot</i>\n"
        "Для начала работы зарегистрируйся",
        parse_mode="HTML",
        reply_markup=await register_kb()
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<i>AvitoTextBot</i>\n"
        "<b>Commands:</b>\n"
        "1) /start - Запуск бота\n"
        "2) /register - Регистрация\n"
        "3) /main - На главную\n"
        "4) /help - Помощь",
        parse_mode="HTML",
        reply_markup=await register_kb()
    )


async def set_my_command(bot: Bot):
    command = [
        BotCommand(command="/start", description="Запуск AvitoBot"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/main", description="На главную"),
        BotCommand(command="/help", description="Помощь")
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
        trigger=IntervalTrigger(seconds=60 * 60),
        kwargs={"bot": bot}
    )
    scheduler.add_job(
        reset_monthly_requests,
        trigger="cron",
        day=1,
        hour=0,
        minute=0
    )
    scheduler.add_job(
        reset_daily_requests,
        trigger="cron",
        hour=0,
        minute=0
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
