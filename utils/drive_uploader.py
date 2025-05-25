import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_file_to_drive(file_path: str, folder_id: str) -> str:
    # Чтение JSON-ключа из переменной окружения
    json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not json_str:
        raise Exception("Переменная окружения GOOGLE_SERVICE_ACCOUNT_JSON не задана")

    credentials_info = json.loads(json_str)
    creds = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')

    # Делаем файл доступным по ссылке
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file_id, body=permission).execute()

    return f'https://drive.google.com/uc?id={file_id}'
