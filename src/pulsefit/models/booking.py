from dataclasses import dataclass

@dataclass
class Booking:
    booking_id: int
    user_id: int
    training_id: int
    status: str
    # Дополнительные служебные поля для имени клиента и названия тренировки
    client_name: str | None = None
    training_title: str | None = None