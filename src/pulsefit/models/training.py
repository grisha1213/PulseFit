from dataclasses import dataclass

@dataclass
class Training:
    training_id: int
    trainer_id: int
    title: str
    start_time: str
    # Дополнительное служебное поле для имени тренировки
    trainer_name: str | None = None