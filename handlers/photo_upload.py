from aiogram import Router
from aiogram.types import Message
from storage import db
from utils.drive_uploader import upload_file_to_drive
import os

router = Router()

@router.message(lambda m: m.photo)
async def handle_photo(message: Message):
file = message.photo[-1]
file_id = file.file_id
file_path = await message.bot.get_file(file_id)
f = await message.bot.download_file(file_path.file_path)
folder = f"media/{message.from_user.id}/"
os.makedirs(folder, exist_ok=True)
filename = folder + file_id + ".jpg"
with open(filename, "wb") as out_file:
    out_file.write(f.read())

db.save_photo_path(message.from_user.id, filename)
await message.answer("Фото сохранено!")
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = f"media/{photo.file_unique_id}.jpg"
    await photo.download_to_drive(file_path)

    # загружаем в Google Drive
    drive_link = upload_file_to_drive(file_path, folder_id="1DgPREeT2cnDcEE8NHdhlEdLwRvgGjdx2")

    await message.answer(f"Фото получено и сохранено!\nСсылка: {drive_link}")