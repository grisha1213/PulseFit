# Импортируем сервисы с бизнес-логикой
from src.pulsefit.services import subscription_type_service
from src.pulsefit.services import training_service
from src.pulsefit.services import client_subscription_service
from src.pulsefit.services import booking_service

# Функция отображения панели администратора
def admin_menu(user):
    while True:
        print(f"\n=== Панель администратора | {user.name} ===")
        print("1. Добавить новый тип абонемента")
        print("2. Добавить тренировку в расписание")
        print("0. Выйти из аккаунта")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            print("\n--- Добавление абонемента ---")
            name = input("Название: ")
            price = int(input("Стоимость: "))
            duration = int(input("Длительность (дни): "))
            try:
                subscription_type_service.add_type(name, price, duration)
                print("Абонемент добавлен!")
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "2":
            print("\n--- Добавление тренировки ---")
            title = input("Название: ")
            start_time = input("Время начала: ")
            trainer_id = int(input("ID тренера: "))
            try:
                training_service.add_training(trainer_id, title, start_time)
                print("Тренировка добавлена!")
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "0":
            # Выход из цикла меню администратора
            break
        else:
            print("Неверный ввод.")

# Функция отображения кабинета клиента
def client_menu(user):
    while True:
        print(f"\n=== Личный кабинет | {user.name} ===")
        print("1. Оформить абонемент")
        print("2. Записаться на тренировку")
        print("0. Выйти из аккаунта")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            print("\n--- Оформление абонемента ---")
            sub_type_id = int(input("ID типа абонемента: "))
            start_date = input("Дата начала: ")
            end_date = input("Дата окончания: ")
            try:
                client_subscription_service.buy_subscription(user.user_id, sub_type_id, start_date, end_date)
                print("Абонемент оформлен!")
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "2":
            print("\n--- Запись на тренировку ---")
            training_id = int(input("ID тренировки: "))
            try:
                training_id = int(input("ID тренировки: "))
                booking_service.book_training(user.user_id, training_id)
                print("Вы записаны!")
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "0":
            # Выход из цикла кабинета клиента
            break
        else:
            print("Неверный ввод.")