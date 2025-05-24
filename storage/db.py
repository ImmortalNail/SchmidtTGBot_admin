import sqlite3
from pathlib import Path

# Путь к базе данных
db_path = Path("storage.db")

# Контекстный менеджер для подключения к базе данных
# Рекомендуется открывать и закрывать соединение при каждой операции,
# но для простоты сейчас используем глобальное подключение.
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создаем таблицу пользователей (если её нет)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER UNIQUE,
    name TEXT,
    dob TEXT
)
""")

# Создаем таблицу с путями к фото пользователей (если её нет)
cursor.execute("""
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER,
    path TEXT
)
""")

conn.commit()


def save_user(tg_id: int, name: str, dob: str):
    """
    Сохраняет пользователя в БД.
    tg_id — Telegram ID пользователя (уникальный)
    name — имя пользователя
    dob — дата рождения в формате строки
    """
    cursor.execute("""
        INSERT OR IGNORE INTO users (tg_id, name, dob) VALUES (?, ?, ?)
    """, (tg_id, name, dob))
    conn.commit()


def save_photo_path(tg_id: int, path: str):
    """
    Сохраняет путь к фото пользователя.
    tg_id — Telegram ID пользователя
    path — строка с путем к фото (например, URL или локальный путь)
    """
    cursor.execute("""
        INSERT INTO photos (tg_id, path) VALUES (?, ?)
    """, (tg_id, path))
    conn.commit()


def get_all_users():
    """
    Возвращает список всех пользователей в формате:
    [{'id': tg_id, 'name': имя, 'dob': дата рождения}, ...]
    """
    cursor.execute("SELECT tg_id, name, dob FROM users")
    rows = cursor.fetchall()
    return [{"id": row[0], "name": row[1], "dob": row[2]} for row in rows]