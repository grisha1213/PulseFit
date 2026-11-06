from src.pulsefit.repositories import booking_repository, training_repository, user_repository
from src.pulsefit.models.booking import Booking

def get_all_bookings() -> list[Booking]:
    return booking_repository.get_all()

def get_user_bookings(user_id: int) -> list[Booking]:
    """Возвращает список всех записей конкретного пользователя."""
    all_bookings = booking_repository.get_all()
    return [b for b in all_bookings if b.user_id == user_id]

def book_training(user_id: int, training_id: int):  # Функция записи пользователя на тренировку
    if user_id <= 0 or training_id <= 0:
        raise Exception("Некорректные данные для записи")

    # Проверяем, существует ли тренировка
    training = training_repository.get_by_id(training_id)
    if not training:
        raise Exception(f"Тренировка с ID {training_id} не найдена")

    # Проверяем, существует ли пользователь
    user = user_repository.get_by_id(user_id)
    if not user:
        raise Exception(f"Пользователь с ID {user_id} не найден")

    # Защита от повторной записи на ту же тренировку
    existing_bookings = booking_repository.get_all()
    for b in existing_bookings:
        if b.user_id == user_id and b.training_id == training_id and b.status == "Активно":
            raise Exception("Вы уже записаны на эту тренировку!")

    status = "Активно"
    booking_repository.create(user_id, training_id, status)

def cancel_booking(booking_id: int):
    # Проверяем, существует ли такое бронирование перед удалением
    booking = booking_repository.get_by_id(booking_id)
    if not booking:
        raise Exception(f"Бронирование с ID {booking_id} не найдено")
        
    booking_repository.delete(booking_id)