from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from storage import db
from utils.drive_uploader import upload_file_to_drive
import os
import asyncio

router = Router()

@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    try:
        photo = message.photo[-1]
        file_id = photo.file_id
        file = await message.bot.get_file(file_id)

        user_id = message.from_user.id
        username = message.from_user.username or "no_username"

        folder = f"media/{user_id}/"
        os.makedirs(folder, exist_ok=True)

        # Формируем имя файла с ID пользователя
        file_name = f"{user_id}_{photo.file_unique_id}.jpg"
        local_path = os.path.join(folder, file_name)

        await message.bot.download_file(file.file_path, destination=local_path)

        # Сохраняем путь в базу
        db.save_photo_path(user_id, local_path)

        # Загружаем в Google Drive с новым именем
        drive_link = await asyncio.to_thread(
            upload_file_to_drive,
            local_path,
            folder_id="1DgPREeT2cnDcEE8NHdhlEdLwRvgGjdx2",
            file_name=file_name  # передаём новое имя
        )

        await message.answer(
            f"Фото получено и сохранено!\n"
            f"Telegram ID: {user_id}\n"
            f"Ссылка на Google Drive: {drive_link}"
        )

    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке фото: {e}")