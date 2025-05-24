from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def init_drive():
    gauth = GoogleAuth()
    # Загружаем настройки из файла client_secrets.json
    # Если используешь Service Account, убедись, что файл JSON указан верно
    gauth.LoadServiceConfigSettings()  # загружает settings.yaml, если есть
    gauth.credentials = gauth.LoadServiceAccountCredentialsFromFile('Schmidt_bot.json')
    drive = GoogleDrive(gauth)
    return drive

def upload_file_to_drive(file_path: str, folder_id: str, file_name: str = None):
    drive = init_drive()
    file_drive = drive.CreateFile({'parents': [{'id': folder_id}]})
    file_drive.SetContentFile(file_path)
    file_drive['title'] = file_name or os.path.basename(file_path)
    file_drive.Upload()
    return file_drive['alternateLink']  # ссылка на файл
