import sqlite3
from pathlib import Path

# Определяем пути относительно текущего скрипта
BASE_DIR = Path(__file__).parent 
SCHEMA_PATH = BASE_DIR / "schema.sql" 
DB_PATH = BASE_DIR / "fitpulse.db" 

def init_db():
    with open(SCHEMA_PATH, encoding="utf-8") as f: 
        script = f.read() 
        
    conn = sqlite3.connect(DB_PATH)
    # Включаем поддержку внешних ключей (Foreign Keys)
    conn.execute('PRAGMA foreign_keys = ON;')
    
    try:
        conn.executescript(script) 
        conn.commit() 
    finally: 
        # Гарантированное закрытие соединения при любых ошибках
        conn.close() 

    print("\nБаза данных fitpulse.db успешно создана в нужной папке!")

if __name__ == "__main__":
    init_db()