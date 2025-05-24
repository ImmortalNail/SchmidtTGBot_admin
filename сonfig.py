import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env в окружение
load_dotenv()

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Получаем список админов как список целых чисел, разделённых запятыми в .env
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

# ID Google таблицы
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# ID папки Google Drive для хранения фото
GOOGLE_FOLDER_ID = os.getenv("GOOGLE_FOLDER_ID")