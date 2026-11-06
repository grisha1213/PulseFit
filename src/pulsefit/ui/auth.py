from src.pulsefit.services import user_service

def login_ui() -> user_service.User | None:
    print("\n" + "=" * 40)
    print("         🔐 АВТОРИЗАЦИЯ В СИСТЕМЕ")
    print("=" * 40)
    
    login = input("  🔸 Введите логин: ").strip()
    password = input("  🔸 Введите пароль: ").strip()

    try:
        user = user_service.authenticate(login, password)
        if user:
            print(f"\n  ✅ Добро пожаловать, {user.name} {user.surname}!")
            return user
        else:
            print("\n  ❌ Ошибка: неверный логин или пароль.")
            return None
    except Exception as e:
        print(f"\n  ❌ Ошибка при входе: {e}")
        return None

def register_ui():
    print("\n" + "=" * 40)
    print("         📝 РЕГИСТРАЦИЯ НОВОГО КЛИЕНТА")
    print("=" * 40)

    try:
        login = input("  🔸 Придумайте логин: ").strip()
        password = input("  🔸 Придумайте пароль: ").strip()
        name = input("  🔸 Имя: ").strip()
        surname = input("  🔸 Фамилия: ").strip()
        patronymic = input("  🔸 Отчество (если есть, иначе Enter): ").strip() or None
        phone = input("  🔸 Телефон (+7...): ").strip()

        user_service.register_client(login, password, name, surname, phone, patronymic)
        print("\n  🎉 Регистрация прошла успешно! Теперь вы можете войти в систему.")
    except Exception as e:
        print(f"\n  ❌ Ошибка регистрации: {e}")