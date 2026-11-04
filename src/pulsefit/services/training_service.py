from src.pulsefit.repositories import training_repository # Импортируем репозиторий тренировок
from src.pulsefit.models import Training # Импортируем модель тренировки

def get_all_trainings() -> list[Training]: # Функция для получения расписания всех тренировок
    return training_repository.get_all()


def add_training(trainer_id: int, title: str, start_time: str): # Функция добавления новой тренировки в расписание
    title = title.strip()
    start_time = start_time.strip()

    if not title:
        raise Exception("Название тренировки не может быть пустым")
    if not start_time:
        raise Exception("Время начала тренировки не может быть пустым")
    if trainer_id <= 0:
        raise Exception("Некорректный ID тренера")

    training_repository.create(trainer_id, title, start_time) # Создаем запись в базе данных через репозиторий

def remove_training(training_id: int):
    training_repository.delete(training_id)