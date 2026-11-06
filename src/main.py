import sys
from pathlib import Path

# Находим корневую папку проекта (на 3 уровня выше текущего файла main.py)
# и добавляем её в пути поиска Python, чтобы работали импорты from src...
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Импортируем соседние модули интерфейса из этой же папки
from src.pulsefit.ui import auth
from src.pulsefit.ui import menu

# Главная функция запуска программы
def start_app():
    # Главный бесконечный цикл стартового окна
    while True:
        print("\n=== Фитнес-клуб FitPulse ===")
        print("1. Вход")
        print("2. Регистрация")
        print("0. Выход из программы")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            # Вызываем UI авторизации и получаем объект пользователя
            user = auth.login_ui()
            # Если вход успешен, проверяем роль и перенаправляем в нужное меню
            if user:
                if user.user_role_id == 1:
                    # Вызов меню администратора
                    menu.admin_menu(user)
                elif user.user_role_id in (2, 3):
                    # Вызов меню клиента (учитываем роли из БД)
                    menu.client_menu(user)
                else:
                    print("Ошибка: неизвестная роль.")
        elif choice == "2":
            # Вызываем интерфейс регистрации
            auth.register_ui()
        elif choice == "0":
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод.")

# Точка входа в программу: если скрипт запущен напрямую, выполняется start_app()
if __name__ == "__main__":
    start_app()