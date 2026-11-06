from src.pulsefit.database.init_db import get_connection
from src.pulsefit.models.booking import Booking

# Вспомогательная функция преобразования данных из строки БД в объект модели
def _map(row) -> Booking:
    return Booking(*row)

# Функция для получения всех бронирований
def get_all() -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT booking_id, user_id, training_id, status
        FROM booking
    """)

    rows = cur.fetchall()
    conn.close()

    return [_map(r) for r in rows]

# Функция для вывода информации о бронировании по ID
def get_by_id(booking_id: int) -> Booking | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT booking_id, user_id, training_id, status
        FROM booking
        WHERE booking_id = ? 
    """, (booking_id,))

    row = cur.fetchone()
    conn.close()

    return _map(row) if row else None

# Функция для создания нового бронирования
def create(user_id: int, training_id: int, status: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO booking(user_id, training_id, status)
        VALUES (?, ?, ?)
    """, (user_id, training_id, status))

    conn.commit()
    conn.close()

# Функция для удаления бронирования
def delete(booking_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM booking
        WHERE booking_id = ?
    """, (booking_id,))

    conn.commit()
    conn.close()