from src.pulsefit.services import (
    training_service, 
    booking_service, 
    subscription_type_service, 
    client_subscription_service,
    user_service
    )
def admin_menu(admin_user):
    while True:
        print("\n" + "═" * 50)
        print(f"    ПАНЕЛЬ АДМИНИСТРАТОРА | Админ: {admin_user.name}")
        print("═" * 50)
        print("  1.  Посмотреть всех пользователей")
        print("  2.  Редактировать пользователя")
        print("  3.  Удалить пользователя")
        print("  4.  Добавить нового администратора") # <-- Твоя новая вкладка
        print("  0.  Выйти из аккаунта")
        print("═" * 50)
        
        choice = input("  Выберите действие: ").strip()

        if choice == "1":
            print("\n" + "─" * 40)
            print("         👥 СПИСОК ПОЛЬЗОВАТЕЛЕЙ")
            print("─" * 40)
            users = user_service.get_all_users()
            if not users:
                print("  📭 База пуста.")
            else:
                for u in users:
                    print(f"  [ID: {u.user_id}] {u.name} {u.surname} | Тел: {u.phone} | Роль: {u.user_role_id}")
            print("─" * 40)

        elif choice == "2":
            try:
                u_id = int(input("\n   Введите ID пользователя для изменения: "))
                print("  Введите новые данные (или те же самые, если менять не нужно):")
                new_name = input("  Новое имя: ").strip()
                new_surname = input("  Новая фамилия: ").strip()
                new_phone = input("  Новый телефон: ").strip()
                
                user_service.update_user(u_id, new_name, new_surname, new_phone)
                print("  ✅ Данные успешно обновлены!")
            except ValueError:
                print("  ❌ Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")

        elif choice == "3":
            try:
                u_id = int(input("\n   Введите ID пользователя для удаления: "))
                if u_id == admin_user.user_id:
                    print("  ❌ Ошибка: Вы не можете удалить собственный аккаунт!")
                else:
                    user_service.delete_user(u_id)
                    print("  ✅ Пользователь успешно удален из базы!")
            except ValueError:
                print("  ❌ Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")

        elif choice == "4":
            # Логика новой вкладки для добавления админа
            print("\n" + "─" * 40)
            print("      ➕ ДОБАВЛЕНИЕ НОВОГО АДМИНА")
            print("─" * 40)
            login = input("  Логин: ").strip()
            password = input("  Пароль: ").strip()
            name = input("  Имя: ").strip()
            surname = input("  Фамилия: ").strip()
            phone = input("  Телефон: ").strip()
            
            try:
                user_service.create_admin(login, password, name, surname, phone)
                print("  ✅ Успех: Новый администратор успешно добавлен в базу!")
            except Exception as e:
                print(f"  ❌ Ошибка при создании админа: {e}")

        elif choice == "0":
            print("\n   Выход из панели администратора...")
            break
        else:
            print("  ❌ Неверный ввод.")
def client_menu(user):
    while True:
        print("\n" + "═" * 50)
        print(f"   ЛИЧНЫЙ КАБИНЕТ КЛИЕНТА | Пользователь: {user.name}")
        print("═" * 50)
        print("  1.  Посмотреть расписание тренировок")
        print("  2.  Записаться на тренировку")
        print("  3.  Мои активные записи")
        print("  4.  Купить абонемент")
        print("  5.  Посмотреть мой абонемент")  # <-- Новый пункт меню
        print("  0.  Выйти из аккаунта")
        print("═" * 50)
        
        choice = input("   Выберите действие: ").strip()

        if choice == "1":
            print("\n" + "─" * 40)
            print("       📅 РАСПИСАНИЕ ТРЕНИРОВОК")
            print("─" * 40)
            trainings = training_service.get_all_trainings()
            if not trainings:
                print("   Расписание пока пусто.")
            else:
                for t in trainings:
                    print(f"  [ID: {t.training_id}] {t.title} 🕒 Время: {t.start_time}")
            print("─" * 40)

        elif choice == "2":
            print("\n--- Запись на тренировку ---")
            trainings = training_service.get_all_trainings()
            if not trainings:
                print("  📭 Нет доступных тренировок.")
                continue
            
            print("  Доступные тренировки:")
            for t in trainings:
                print(f"  [ID: {t.training_id}] {t.title} ({t.start_time})")

            try:
                training_id = int(input("  Введите ID тренировки для записи: "))
                booking_service.book_training(user.user_id, training_id)
                print("  🎉 Вы успешно записаны на тренировку!")
            except ValueError:
                print("  ❌ Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")

        elif choice == "3":
            print("\n" + "─" * 40)
            print("         МОИ ЗАПИСИ НА ТРЕНИРОВКИ")
            print("─" * 40)
            my_bookings = booking_service.get_user_bookings(user.user_id)
            if not my_bookings:
                print("  📭 У вас пока нет активных записей.")
            else:
                for b in my_bookings:
                    print(f"  [Запись ID: {b.booking_id}] Тренировка ID: {b.training_id} | Статус: {b.status}")
            print("─" * 40)

        elif choice == "4":
            print("\n" + "─" * 40)
            print("         💳 ДОСТУПНЫЕ АБОНЕМЕНТЫ")
            print("─" * 40)
            types = subscription_type_service.get_all()
            for st in types:
                print(f"  [ID: {st.subscription_type_id}] {st.name} — 💰 {st.price} руб. (Дней: {st.duration_days})")
            
            try:
                sub_type_id = int(input("   Введите ID нужного абонемента: "))
                start_date = input("   Дата начала (ДД.ММ.ГГГГ): ").strip()
                
                end_date = client_subscription_service.buy_subscription(user.user_id, sub_type_id, start_date)
                print(f"  🎉 Абонемент успешно оформлен! Действует до: {end_date}")
            except ValueError:
                print("  ❌ Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")

        elif choice == "5":  # <-- Логика обработки нового пункта меню
            print("\n" + "─" * 40)
            print("        🎫 МОИ АБОНЕМЕНТЫ")
            print("─" * 40)
            my_subs = client_subscription_service.get_user_subscriptions(user.user_id)
            if not my_subs:
                print("  📭 У вас пока нет оформленных абонементов.")
            else:
                for sub in my_subs:
                    print(f"  [ID абонемента: {sub.client_subscription_id}]")
                    print(f"   • Тип ID: {sub.subscription_type_id}")
                    print(f"   • Период: с {sub.start_date} по {sub.end_date}")
                    print(f"   • Статус: {sub.status}")
                    print("  " + "─" * 30)
            print("─" * 40)

        elif choice == "0":
            print("\n   Выход из личного кабинета...")
            break
        else:
            print("  ❌ Неверный ввод, выберите пункт из меню.")