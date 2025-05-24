from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from storage import db
from utils.drive_uploader import upload_file_to_drive
import os

router = Router()

@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    # Получаем самый большой размер фото
    photo = message.photo[-1]
    file_id = photo.file_id

    # Получаем объект File от Telegram
    file = await message.bot.get_file(file_id)

    # Создаем папку для пользователя, если нет
    folder = f"media/{message.from_user.id}/"
    os.makedirs(folder, exist_ok=True)

    # Локальный путь сохранения фото
    local_path = os.path.join(folder, f"{photo.file_unique_id}.jpg")

    # Скачиваем файл используя file.download (НЕ photo.download!)
    await file.download(destination_file=local_path)

    # Сохраняем путь в базу
    db.save_photo_path(message.from_user.id, local_path)

    # Загружаем на Google Drive (функция upload_file_to_drive из utils)
    drive_link = upload_file_to_drive(local_path, folder_id="1DgPREeT2cnDcEE8NHdhlEdLwRvgGjdx2")

    await message.answer(f"Фото получено и сохранено!\nСсылка на Google Drive: {drive_link}")