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
# Главная функция запуска программы
def start_app():
    while True:
        print("\n=== Фитнес-клуб FitPulse ===")
        print("  1. Войти как клиент")
        print("  2. Войти в систему ")
        print("  3. Регистрация нового клиента")
        print("  0. Выход из программы")
        
        choice = input(" Выберите действие: ").strip()
        
        if choice == "1":
            print("\n--- Вход для клиентов ---")
            user = auth.login_ui()
            if user:
                # Пускаем только если роль не админ (например, 2 - клиент, 3 - тренер)
                if user.user_role_id != 1: 
                    menu.client_menu(user)
                else:
                    print("  ❌ Ошибка: Администраторы должны входить через специальный раздел.")
                    
        elif choice == "2":
            print("\n--- Вход для администраторов ---")
            user = auth.login_ui()
            if user:
                # Пускаем только если роль админа (1)
                if user.user_role_id == 1:
                    menu.admin_menu(user)
                else:
                    print("  ❌ У вас нет прав доступа в панель администратора.")
                    
        elif choice == "3":
            # Вызываем интерфейс регистрации
            auth.register_ui()
            
        elif choice == "0":
            print("Завершение работы программы...")
            break
            
        else:
            print("  ❌ Неверный ввод.")

# Точка входа в программу
if __name__ == "__main__":
    from src.pulsefit.services import user_service
    
    # 1. Пытаемся создать первого админа при запуске
    try:
        user_service.create_admin("admin", "123", "Григорий", "Волков", "79990000000")
        print("✅ Первый админ (admin / 123) успешно создан в базе!")
    except Exception:
        # Если админ уже существует, идем дальше
        pass 
        
    # 2. Только после этого запускаем само меню
    start_app()