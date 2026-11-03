from src.pulsefit.repositories import training_repository
from src.pulsefit.models import Training

def get_all_trainings() -> list[Training]:
    return training_repository.get_all()

def get_training(training_id: int) -> Training | None:
    return training_repository.get_by_id(training_id)

def add_training(trainer_id: int, title: str, start_time: str):
    title = title.strip()
    start_time = start_time.strip()

    if not title:
        raise Exception("Название тренировки не может быть пустым")
    if not start_time:
        raise Exception("Время начала тренировки не может быть пустым")
    if trainer_id <= 0:
        raise Exception("Некорректный ID тренера")

    training_repository.create(trainer_id, title, start_time)

def remove_training(training_id: int):
    training_repository.delete(training_id)