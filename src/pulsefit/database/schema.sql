--  Сброс старых таблиц (сначала зависимые, потом независимые)
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS trainings;
DROP TABLE IF EXISTS client_subscriptions;
DROP TABLE IF EXISTS subscription_types;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_roles;

-- Справочник ролей
CREATE TABLE user_roles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Пользователи системы (клиенты, тренеры, администраторы)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    phone TEXT NOT NULL,
    password TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE,
    user_role_id INTEGER NOT NULL,
    FOREIGN KEY (user_role_id) REFERENCES user_roles(user_role_id)
);

--  Каталог типов абонементов
CREATE TABLE subscription_types (
    subscription_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    duration_days INTEGER NOT NULL
);

-- Купленные абонементы клиентов
CREATE TABLE client_subscriptions (
    client_subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subscription_type_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (subscription_type_id) REFERENCES subscription_types(subscription_type_id)
);

-- Расписание тренировок
CREATE TABLE trainings (
    training_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trainer_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start_time TEXT NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES users(user_id)
);

-- Записи клиентов на тренировки
CREATE TABLE booking (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    training_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (training_id) REFERENCES trainings(training_id)
);



-- Роли пользователей
INSERT INTO user_roles (name) VALUES 
('Администратор'),
('Тренер'),
('Клиент');

-- Пользователи
INSERT INTO users (name, surname, patronymic, phone, password, login, user_role_id) VALUES 
('Алексей', 'Петров', 'Сергеевич', '+79991112233', 'pass123', 'trainer_alex', 2),
('Мария', 'Иванова', 'Алексеевна', '+79998887766', 'secret321', 'client_maria', 3);

-- Виды абонементов
INSERT INTO subscription_types (name, price, duration_days) VALUES 
('Безлимит на 1 месяц', 4500, 30),
('Йога (8 занятий)', 3200, 45);

-- Купленные абонементы
INSERT INTO client_subscriptions (user_id, subscription_type_id, start_date, end_date, status) VALUES 
(2, 1, '2026-10-01', '2026-11-01', 'Активен');

-- Тренировки
INSERT INTO trainings (trainer_id, title, start_time) VALUES 
(1, 'Утренняя йога', '2026-10-25 09:00');

-- Записи клиентов
INSERT INTO booking (user_id, training_id, status) VALUES 
(2, 1, 'Записан');