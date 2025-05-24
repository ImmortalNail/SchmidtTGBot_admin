import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(",")))
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_FOLDER_ID = os.getenv("GOOGLE_FOLDER_ID")

EXAMPLE .env:
BOT_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMIN_IDS=123456789,987654321
GOOGLE_SHEET_ID=sheet_id_from_google
GOOGLE_FOLDER_ID=folder_id_from_google_drive