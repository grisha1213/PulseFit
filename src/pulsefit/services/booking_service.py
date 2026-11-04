from src.pulsefit.repositories import booking_repository
from src.pulsefit.models import Booking

def get_all_bookings() -> list[Booking]:
    return booking_repository.get_all()

def book_training(user_id: int, training_id: int):  # Функция записи пользователя на тренировку
    if user_id <= 0 or training_id <= 0:
        raise Exception("Некорректные данные для записи")

    status = "Активно"
    booking_repository.create(user_id, training_id, status)

def cancel_booking(booking_id: int):
    booking_repository.delete(booking_id)