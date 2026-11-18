from src.pulsefit.repositories import client_subscription_repository
from src.pulsefit.models.client_subscription import ClientSubscription
from datetime import datetime, timedelta
from src.pulsefit.repositories import client_subscription_repository, subscription_type_repository
from src.pulsefit.services.export_service import ExportService

def get_all_subscriptions() -> list[ClientSubscription]:
    return client_subscription_repository.get_all()

def buy_subscription(user_id: int, subscription_type_id: int, start_date: str) -> str:
    start_date = start_date.strip()

    if not start_date:
        raise Exception("Дата начала не может быть пустой")
    if user_id <= 0 or subscription_type_id <= 0:
        raise Exception("Некорректные данные пользователя или абонемента")

    # 1. Проверяем и парсим дату в формате ДД.ММ.ГГГГ
    try:
        start_dt = datetime.strptime(start_date, "%d.%m.%Y")
    except ValueError:
        raise Exception("Неверный формат даты! Введите в формате ДД.ММ.ГГГГ (например, 01.01.2026)")

    # 2. Получаем выбранный тип абонемента, чтобы узнать количество дней
    sub_type = subscription_type_repository.get_by_id(subscription_type_id)
    if not sub_type:
        raise Exception("Абонемент с таким ID не найден")

    # 3. Автоматически вычисляем дату окончания
    end_dt = start_dt + timedelta(days=sub_type.duration_days)
    start_date_str = start_dt.strftime("%d.%m.%Y")
    end_date_str = end_dt.strftime("%d.%m.%Y")

    status = "Активно"
    client_subscription_repository.create(user_id, subscription_type_id, start_date_str, end_date_str, status)
    client_subscription_repository.create(user_id, subscription_type_id, start_date_str, end_date_str, status)
    ExportService().export_client_subscriptions()  # автообновление папки out/
    
    return end_date_str

def get_user_subscriptions(user_id: int) -> list[ClientSubscription]:
    """Возвращает список всех абонементов конкретного пользователя."""
    all_subs = client_subscription_repository.get_all()
    return [sub for sub in all_subs if sub.user_id == user_id]