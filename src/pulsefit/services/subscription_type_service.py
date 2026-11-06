from src.pulsefit.repositories import subscription_type_repository
from src.pulsefit.models.subscription_type import SubscriptionType

def get_all() -> list[SubscriptionType]:
    #Возвращает список всех типов абонементов.
    return subscription_type_repository.get_all()

def get_all_types() -> list[SubscriptionType]:
    #Дублирующий алиас на случай, если где-то вызывается get_all_types.
    return subscription_type_repository.get_all()

def add_type(name: str, price: int, duration_days: int):
    #Добавление нового типа абонемента.
    name = name.strip()
    if not name:
        raise Exception("Название абонемента не может быть пустым")
    if price < 0:
        raise Exception("Цена абонемента не может быть отрицательной")
    if duration_days <= 0:
        raise Exception("Длительность абонемента должна быть больше нуля")
    
    subscription_type_repository.create(name, price, duration_days)