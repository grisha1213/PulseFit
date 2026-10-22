import sqlite3
from pathlib import Path

# Определяем пути относительно текущего скрипта
BASE_DIR = Path(__file__).parent # Папка работы
SCHEMA_PATH = BASE_DIR / "schema.sql" # Файл sql схемы
DB_PATH = BASE_DIR / "fitpulse.db"  # Файл, где будет ДБ

def init_db():
    with open(SCHEMA_PATH, encoding="utf-8") as f:  # Читаем наш SQL код в script
        script = f.read() 
        
    conn = sqlite3.connect(DB_PATH)# Подключение к БД(Если её нет, то она создатся)
    # Включаем поддержку внешних ключей (Foreign Keys)
    conn.execute('PRAGMA foreign_keys = ON;')
    
    try:
        conn.executescript(script)  # Выполняет sql script, создавая описанные таблицы
        conn.commit() # Сохранение таблиц из sql скрипта
    finally: 
        # Гарантированное закрытие соединения при любых ошибках
        conn.close() 

    print("\nDatabase fitpulse.db successfully created in the correct folder!")

if __name__ == "__main__":
    init_db()