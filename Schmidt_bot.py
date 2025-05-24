from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
from config import BOT_TOKEN
from handlers import registration, photo_upload, admin

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

dp.include_routers(
    registration.router,
    photo_upload.router,
    admin.router
)

await bot.delete_webhook(drop_pending_updates=True)
await dp.start_polling(bot)

if name == "main":
asyncio.run(main())