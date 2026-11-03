from src.pulsefit.models import User
from src.pulsefit.repositories import user_repository

# Задаем константы для ролей (предположим, 1 - Админ, 2 - Клиент, 3 - Тренер)
ADMIN_ROLE_ID = 1
CLIENT_ROLE_ID = 2
TRAINER_ROLE_ID = 3

# Проверяет данные для входа
def authenticate(login: str, password: str) -> User | None:
    login = login.strip()
    password = password.strip()

    if not login or not password:
        return None

    user = user_repository.get_by_login(login) # поиск пользователя в базе
    if not user or user.password != password:
        return None

    return user

# Управляет процессом регистрации клиента
def register_client(
    login: str, 
    password: str, 
    name: str, 
    surname: str, 
    phone: str,
    patronymic: str | None = None
):
    login = login.strip()
    password = password.strip()
    name = name.strip()
    surname = surname.strip()
    phone = phone.strip()
    if patronymic:
        patronymic = patronymic.strip()

    if not login:
        raise Exception("Логин не может быть пустым")
    if not password:
        raise Exception("Пароль не может быть пустым")
    if not name or not surname:
        raise Exception("Имя и фамилия клиента не могут быть пустыми")
    if not phone:
        raise Exception("Номер телефона не может быть пустым")

    if user_repository.get_by_login(login): # проверка дубликата
        raise Exception(f"Пользователь с логином '{login}' уже существует")

    # Создаем аккаунт пользователя с ролью "Клиент"
    user_repository.create(name, surname, patronymic, phone, password, login, CLIENT_ROLE_ID)


# Создание нового сотрудника (администратора)
def create_admin(
    login: str, 
    password: str, 
    name: str, 
    surname: str, 
    phone: str,
    patronymic: str | None = None
):
    login = login.strip()
    password = password.strip()
    name = name.strip()
    surname = surname.strip()
    
    if not login:
        raise Exception("Логин не может быть пустым")
    if not password:
        raise Exception("Пароль не может быть пустым")
    if not name or not surname:
        raise Exception("Имя и фамилия администратора не могут быть пустыми")

    if user_repository.get_by_login(login):
        raise Exception(f"Пользователь с логином '{login}' уже существует")

    user_repository.create(name, surname, patronymic, phone, password, login, ADMIN_ROLE_ID)