from src.pulsefit.repositories import subscription_type_repository # Импортируем репозиторий типов абонементов
from src.pulsefit.models.subscription_type import SubscriptionType # Импортируем модель типа абонемента

def get_all_types() -> list[SubscriptionType]: # Функция для запроса всех доступных абонементов, возвращающая список объектов
    return subscription_type_repository.get_all()

def add_type(name: str, price: int, duration_days: int): # Функция для добавления нового типа абонемента
    name = name.strip()

    if not name:
        raise Exception("Название абонемента не может быть пустым")
    if price < 0:
        raise Exception("Цена абонемента не может быть отрицательной")
    if duration_days <= 0:
        raise Exception("Длительность абонемента должна быть больше нуля")

    subscription_type_repository.create(name, price, duration_days)