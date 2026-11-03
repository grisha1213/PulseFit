from src.pulsefit.repositories import client_subscription_repository
from src.pulsefit.models import ClientSubscription

def get_all_subscriptions() -> list[ClientSubscription]:
    return client_subscription_repository.get_all()

def buy_subscription(user_id: int, subscription_type_id: int, start_date: str, end_date: str):
    start_date = start_date.strip()
    end_date = end_date.strip()

    if not start_date or not end_date:
        raise Exception("Даты начала и окончания не могут быть пустыми")
    if user_id <= 0 or subscription_type_id <= 0:
        raise Exception("Некорректные данные пользователя или абонемента")

    status = "Активно"
    client_subscription_repository.create(user_id, subscription_type_id, start_date, end_date, status)