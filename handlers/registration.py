from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from storage import db
import gspread
import re

router = Router()

class RegState(StatesGroup):
    full_name = State()
    birth_date = State()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
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

    data = await state.get_data()
    db.save_user(message.from_user.id, data["full_name"], message.text)
    await message.answer("Спасибо, вы зарегистрированы. Можете загружать фото.")
    await state.clear()

def append_row_to_sheet(data_list: list, sheet_id: str):
    gc = gspread.service_account(filename="tg-bot-drive-key.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    worksheet.append_row(data_list)