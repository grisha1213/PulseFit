from dataclasses import dataclass

@dataclass
class ClientSubscription:
    client_subscription_id: int
    user_id: int
    subscription_type_id: int
    start_date: str
    end_date: str
    status: str
    # Дополнительные служебные поля для названия абонемента и имени клиента
    subscription_name: str | None = None
    client_name: str | None = None