from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_IDS
from storage import db

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
if message.from_user.id not in ADMIN_IDS:
return await message.answer("Доступ запрещён.")
await message.answer("Админ-панель:\n- /users — список\n- /broadcast <текст>")

@router.message(Command("users"))
async def list_users(message: Message):
users = db.get_all_users()
text = "\n".join([f"{u['id']}: {u['name']} ({u['dob']})" for u in users])
await message.answer(text or "Нет пользователей")

@router.message(Command("broadcast"))
async def broadcast(message: Message):
if message.from_user.id not in ADMIN_IDS:
return
text = message.text.split(maxsplit=1)
if len(text) < 2:
return await message.answer("Введите сообщение для рассылки")
text = text[1]
for user in db.get_all_users():
try:
await message.bot.send_message(user["id"], text)
except:
continue
await message.answer("Рассылка завершена")