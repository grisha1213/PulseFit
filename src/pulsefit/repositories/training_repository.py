from src.pulsefit.database.init_db import get_connection
from src.pulsefit.models.training import Training

# Вспомогательная функция преобразования данных
def _map(row) -> Training:
    return Training(*row)

# Функция для получения всех тренировок
def get_all() -> list[Training]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT training_id, trainer_id, title, start_time
        FROM trainings
    """)

    rows = cur.fetchall()
    conn.close()

    return [_map(r) for r in rows]

# Функция для вывода информации о тренировке по ID
def get_by_id(training_id: int) -> Training | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT training_id, trainer_id, title, start_time
        FROM trainings
        WHERE training_id = ? 
    """, (training_id,)) # Обрати внимание на запятую внутри скобок!

    row = cur.fetchone()
    conn.close()

    return _map(row) if row else None

# Функция для создания новой тренировки
def create(trainer_id: int, title: str, start_time: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trainings(trainer_id, title, start_time)
        VALUES (?, ?, ?)
    """, (trainer_id, title, start_time))

    conn.commit()
    conn.close()

# Функция для удаления тренировки
def delete(training_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM trainings
        WHERE training_id = ?
    """, (training_id,))

    conn.commit()
    conn.close()