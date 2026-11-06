# Подключаем функцию получения соединения и нужную модель данных
from src.pulsefit.database.init_db import get_connection
from src.pulsefit.models.user import User

# Вспомогательная функция, преобразующая строку из БД в объект модели
def _map(row) -> User:
    return User(*row)

def get_all() -> list[User]:
    # Создаётся подключение к базе данных
    conn = get_connection()
    cur = conn.cursor()
    
    # Делаем SELECT с LEFT JOIN, чтобы сразу вытащить r.name (текстовое название роли)
    # Оно автоматически попадет в наше дополнительное поле role_name
    cur.execute("""
        SELECT u.user_id, u.name, u.surname, u.patronymic, 
               u.phone, u.password, u.login, u.user_role_id, 
               r.name 
        FROM users u
        LEFT JOIN user_roles r ON u.user_role_id = r.user_role_id
    """)
    rows = cur.fetchall()
    
    # После завершения работы соединение закрывается
    conn.close()
    return [_map(r) for r in rows]

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    
    # Ищем конкретного пользователя по логину (нужно для авторизации)
    cur.execute("""
        SELECT u.user_id, u.name, u.surname, u.patronymic, 
               u.phone, u.password, u.login, u.user_role_id, 
               r.name 
        FROM users u
        LEFT JOIN user_roles r ON u.user_role_id = r.user_role_id
        WHERE u.login = ?
    """, (login,))
    row = cur.fetchone()
    
    conn.close()
    # Если пользователь найден, возвращаем объект, иначе None
    return _map(row) if row else None

def create(name: str, surname: str, patronymic: str | None, phone: str, password: str, login: str, user_role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    # Операция создания записи (Create) с использованием параметров ?
    cur.execute("""
        INSERT INTO users(name, surname, patronymic, phone, password, login, user_role_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, surname, patronymic, phone, password, login, user_role_id))
    
    # Сохраняем изменения
    conn.commit()
    conn.close()

def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    # Физическое удаление пользователя
    cur.execute("""
        DELETE FROM users
        WHERE user_id = ?
    """, (user_id,))
    
    conn.commit()
    conn.close()

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.user_id, u.name, u.surname, u.patronymic, 
               u.phone, u.password, u.login, u.user_role_id, 
               r.name 
        FROM users u
        LEFT JOIN user_roles r ON u.user_role_id = r.user_role_id
        WHERE u.user_id = ?
    """, (user_id,))
    row = cur.fetchone()

    conn.close()
    return _map(row) if row else None