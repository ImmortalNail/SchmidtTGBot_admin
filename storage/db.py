import sqlite3
from pathlib import Path

db_path = Path("storage.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
tg_id INTEGER,
name TEXT,
dob TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS photos (
id INTEGER PRIMARY KEY,
tg_id INTEGER,
path TEXT
)
""")
conn.commit()

def save_user(tg_id, name, dob):
    cursor.execute("INSERT INTO users (tg_id, name, dob) VALUES (?, ?, ?)", (tg_id, name, dob))
    conn.commit()

def save_photo_path(tg_id, path):
    cursor.execute("INSERT INTO photos (tg_id, path) VALUES (?, ?)", (tg_id, path))
    conn.commit()

def get_all_users():
    cursor.execute("SELECT tg_id, name, dob FROM users")
    return [{"id": row[0], "name": row[1], "dob": row[2]} for row in cursor.fetchall()]