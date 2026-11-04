from src.pulsefit.database.init_db import get_connection # Подключение к базе данных 
from src.pulsefit.models.subscription_type import SubscriptionType #подключаются необходимые зависимости

# вспомогательная функция преобразования данных
def _map(row) -> SubscriptionType: 
    return SubscriptionType(*row)
#SQLite возвращает строки таблицы в виде кортежей (tuple). Например:
#(1, None, 3, 5, '2026-06-09', 1)
# Работать с такими структурами неудобно, поэтому данные преобразуются в объект модели SubscriptionType. 
# Это делает код более читаемым и позволяет обращаться к полям по имени.

# функция для получения  все типы абонементов
def get_all() -> list[SubscriptionType]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT subscription_type_id, name, price, duration_days 
        FROM subscription_types
    """) # Метод execute() выполняет SQL-команду SELECT для получения данны


    rows = cur.fetchall() # Метод fetchall() возвращает список всех найденных строк
    conn.close()
    return [_map(r) for r in rows] # Генератор списка преобразует каждую строку таблицы в объект модели

# функция для получения тип абонемента по ID
def get_by_id(sub_type_id: int) -> SubscriptionType | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT subscription_type_id, name, price, duration_days 
        FROM subscription_types
        WHERE subscription_type_id = ?
    """, (sub_type_id,))
    row = cur.fetchone() # Метод fetchone() возвращает одну запись из результата запроса
    conn.close()
    return _map(row) if row else None # Выполняется проверка: если запись отсутствует, возвращается None

# функция для добавления нового типа абонемента
def create(name: str, price: int, duration_days: int):
    conn = get_connection() # создаётся подключение к базе данных
    cur = conn.cursor() # создаётся курсор,Курсор используется для выполнения SQL-запросов.

    cur.execute("""
        INSERT INTO subscription_types(name, price, duration_days)
        VALUES (?, ?, ?)
    """, (name, price, duration_days)) # Метод execute() выполняет SQL-команду

    conn.commit()
    conn.close()

# Изменить цену абонемента
def update_price(sub_type_id: int, new_price: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE subscription_types
        SET price = ?
        WHERE subscription_type_id = ?
    """, (new_price, sub_type_id))

    conn.commit()
    conn.close()

# Удалить тип абонемента
def delete(sub_type_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM subscription_types
        WHERE subscription_type_id = ?
    """, (sub_type_id,))

    conn.commit()
    conn.close()