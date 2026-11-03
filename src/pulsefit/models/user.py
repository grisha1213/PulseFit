from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    name: str
    surname: str
    patronymic: str | None
    phone: str
    password: str
    login: str
    user_role_id: int
    # Дополнительное служебное поле для названия роли 
    role_name: str | None = None