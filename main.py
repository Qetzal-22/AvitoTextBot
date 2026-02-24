from aiogram import F, types, Bot
from aiogram.types import Message, BotCommand
from aiogram.filters import Command

import asyncio
import logging

from app.bot.bot import bot, dp
from app.bot.handler.user import user_router_bot
from app.bot.handler.payments import payment_router_bot
from app.config.logging_config import setup_logging

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("AvitoTextBot")

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


async def main():
    await asyncio.gather(
        start_bot()
    )

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Application started")
    asyncio.run(main())