from src.pulsefit.database.init_db import get_connection
from src.pulsefit.models.client_subscription import ClientSubscription

def _map(row) -> ClientSubscription:
    return ClientSubscription(*row)

# Функция для получения всех абонементов клиентов
def get_all() -> list[ClientSubscription]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT client_subscription_id, user_id, subscription_type_id, start_date, end_date, status
        FROM client_subscriptions
    """)

    rows = cur.fetchall()
    conn.close()

    return [_map(r) for r in rows]




# Функция для поиска абонемента по ID
def get_by_id(client_sub_id: int) -> ClientSubscription | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT client_subscription_id, user_id, subscription_type_id, start_date, end_date, status
        FROM client_subscriptions
        WHERE client_subscription_id = ?
    """, (client_sub_id,))

    row = cur.fetchone()
    conn.close()

    return _map(row) if row else None

# Функция для оформления нового абонемента
def create(user_id: int, subscription_type_id: int, start_date: str, end_date: str, status: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO client_subscriptions(user_id, subscription_type_id, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, subscription_type_id, start_date, end_date, status))

    conn.commit()
    conn.close()


