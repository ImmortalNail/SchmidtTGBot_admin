from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from storage import db
import gspread
import re
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date

router = Router()

class RegState(StatesGroup):
    consent = State()
    full_name = State()
    birth_date = State()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Для продолжения регистрации необходимо согласие на обработку персональных данных.\n"
        "Пожалуйста, напишите 'да' для согласия или 'нет' для отказа."
    )
    await state.set_state(RegState.consent)

@router.message(RegState.consent)
async def process_consent(message: Message, state: FSMContext):
    text = message.text.strip().lower()
    if text not in ["да", "нет"]:
        return await message.answer("Пожалуйста, ответьте 'да' или 'нет'.")

    if text == "нет":
        await state.clear()
        return await message.answer("Регистрация отменена из-за отказа от обработки данных.")

    await message.answer("Введите ФИО (не менее 3 символов):")
    await state.set_state(RegState.full_name)

@router.message(RegState.full_name)
async def process_name(message: Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        return await message.answer("ФИО должно быть не менее 3 символов. Повторите:")

    await state.update_data(full_name=message.text.strip())
    await message.answer("Введите дату рождения в формате ДД.ММ.ГГГГ:")
    await state.set_state(RegState.birth_date)

@router.message(RegState.birth_date)
async def process_birth(message: Message, state: FSMContext):
    if not re.match(r"\d{2}\.\d{2}\.\d{4}$", message.text):
        return await message.answer("Неверный формат. Введите как 01.01.2000")

    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        return await message.answer("Некорректная дата. Попробуйте ещё раз.")

    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    if age < 18:
        await state.clear()
        return await message.answer("Извините, регистрация доступна только для совершеннолетних.")

    await state.update_data(birth_date=message.text)
    data = await state.get_data()

    db.save_user(message.from_user.id, data["full_name"], data["birth_date"])

    sheet_id = "ВАШ_SPREADSHEET_ID_ТУТ"
    row = [str(message.from_user.id), data["full_name"], data["birth_date"]]
    try:
        append_row_to_sheet(row, sheet_id)
    except Exception as e:
        await message.answer(f"Ошибка при записи в Google Sheets: {e}")

    await message.answer("Спасибо, вы зарегистрированы. Можете загружать фото.")
    await state.clear()

def append_row_to_sheet(data_list: list, sheet_id: str):
    json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not json_str:
        raise ValueError("Переменная окружения GOOGLE_SERVICE_ACCOUNT_JSON не установлена")

    info = json.loads(json_str)
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(info, scopes=scopes)

    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    worksheet.append_row(data_list)
