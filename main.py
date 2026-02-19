from aiogram import F, types, Bot
from aiogram.types import Message, BotCommand
from aiogram.filters import Command

import asyncio

from app.bot.bot import bot, dp

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("AvitoTextBot")

async def set_my_command(bot: Bot):
    command = [
        BotCommand(command="/start", description="Запуск AvitoBot")
    ]
    await bot.set_my_commands(command)

async def start_bot():
    await set_my_command(bot)
    await dp.start_polling(bot)

async def main():
    await asyncio.gather(
        start_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())