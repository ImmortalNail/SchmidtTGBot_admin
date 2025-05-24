from aiogram import Router, F
from aiogram.types import Message, InputFile
from aiogram.filters import Command
from config import ADMIN_IDS
from storage import db
import os

router = Router()

# Словарь для хранения временных данных рассылки по admin_id
broadcast_sessions = {}

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("Доступ запрещён.")
    
    await message.answer("Админ-панель:\n- /users — список\n- /broadcast <текст> — начать рассылку\n"
                         "- После команды /broadcast отправьте фото для рассылки или напишите 'нет' для без фото")

@router.message(Command("users"))
async def list_users(message: Message):
    users = db.get_all_users()
    text = "\n".join([f"{u['id']}: {u['name']} ({u['dob']})" for u in users])
    await message.answer(text or "Нет пользователей")

@router.message(Command("broadcast"))
async def start_broadcast(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    text_parts = message.text.split(maxsplit=1)
    if len(text_parts) < 2:
        await message.answer("Введите сообщение для рассылки после команды /broadcast")
        return

    broadcast_text = text_parts[1]

    # Запоминаем текст рассылки, ждем фото или 'нет'
    broadcast_sessions[message.from_user.id] = {"text": broadcast_text, "photo": None}
    await message.answer("Текст сохранён. Теперь отправьте фото для рассылки или напишите 'нет' для рассылки без фото.")

@router.message(F.photo)
async def receive_photo_for_broadcast(message: Message):
    user_id = message.from_user.id
    if user_id not in broadcast_sessions:
        return  # Не в режиме рассылки

    # Получаем фото (самый большой размер)
    photo = message.photo[-1]

    # Сохраняем фото локально
    folder = "temp_broadcast_photos"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{user_id}_{photo.file_unique_id}.jpg")
    await photo.download(destination_file=path)

    # Сохраняем путь к фото в сессии рассылки
    broadcast_sessions[user_id]["photo"] = path

    await message.answer("Фото сохранено. Начинаю рассылку...")

    await do_broadcast(message.bot, user_id)
    # После рассылки очищаем сессию
    broadcast_sessions.pop(user_id, None)

@router.message()
async def no_photo_response(message: Message):
    user_id = message.from_user.id
    if user_id not in broadcast_sessions:
        return

    if message.text.lower() == "нет":
        await message.answer("Начинаю рассылку без фото...")

        await do_broadcast(message.bot, user_id)
        # После рассылки очищаем сессию
        broadcast_sessions.pop(user_id, None)
    else:
        await message.answer("Пожалуйста, отправьте фото или напишите 'нет' для рассылки без фото.")

async def do_broadcast(bot, admin_id):
    session = broadcast_sessions.get(admin_id)
    if not session:
        return

    users = db.get_all_users()
    text = session["text"]
    photo_path = session.get("photo")
    count = 0

    for user in users:
        try:
            if photo_path:
                with open(photo_path, "rb") as photo_file:
                    await bot.send_photo(chat_id=user["id"], photo=photo_file, caption=text)
            else:
                await bot.send_message(chat_id=user["id"], text=text)
            count += 1
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user['id']}: {e}")

    await bot.send_message(chat_id=admin_id, text=f"Рассылка завершена. Отправлено: {count} сообщений.")

    # Удаляем временный файл с фото
    if photo_path:
        try:
            os.remove(photo_path)
        except Exception as e:
            print(f"Ошибка при удалении временного файла: {e}")
