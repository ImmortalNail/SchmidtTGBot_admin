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

        folder = f"media/{message.from_user.id}/"
        os.makedirs(folder, exist_ok=True)

        local_path = os.path.join(folder, f"{photo.file_unique_id}.jpg")

        await message.bot.download_file(file.file_path, destination=local_path)

        db.save_photo_path(message.from_user.id, local_path)

        drive_link = await asyncio.to_thread(
            upload_file_to_drive,
            local_path,
            folder_id="1DgPREeT2cnDcEE8NHdhlEdLwRvgGjdx2"
        )

        await message.answer(f"Фото получено и сохранено!\nСсылка на Google Drive: {drive_link}")

    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке фото: {e}")
