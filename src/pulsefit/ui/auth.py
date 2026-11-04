from src.pulsefit.services import user_service

def login_ui():
    print("\n=== Авторизация ===")
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    
    # Обращаемся к слою сервисов для проверки
    user = user_service.authenticate(login, password)
    
    if user:
        print(f"Успешный вход! Добро пожаловать, {user.name}.")
        return user  # Возвращаем пользователя для дальнейшего определения его меню
    else:
        print("Ошибка: Неверный логин или пароль.")
        return None

def register_ui():
    print("\n=== Регистрация нового клиента ===")
    login = input("Придумайте логин: ")
    password = input("Придумайте пароль: ")
    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество (если нет, нажмите Enter): ")
    phone = input("Номер телефона: ")
    
    # Отлов исключений (Exception) из бизнес-логики сервиса
    try:
        user_service.register_client(login, password, name, surname, phone, patronymic)
        print("Регистрация успешно завершена! Теперь вы можете войти.")
    except Exception as e:
        print(f"Ошибка регистрации: {e}")