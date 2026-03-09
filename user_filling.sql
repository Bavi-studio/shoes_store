-- Создание ролей
INSERT INTO roles (role_name) VALUES
('Администратор'),
('Менеджер'),
('Авторизированный клиент');

-- Создание таблицы поставщиков, если ещё не создана
CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Вставка уникальных поставщиков из списка товаров
INSERT INTO suppliers (name)
VALUES
('Kari'),
('Обувь для вас')
ON CONFLICT (name) DO NOTHING;  -- предотвращает дубли

-- Вставка пользователей

INSERT INTO users (login, password, full_name, role_id)
VALUES
-- Администраторы
('94d5ous@gmail.com', 'uzWC67', 'Никифорова Весения Николаевна', 
    (SELECT id FROM roles WHERE role_name='Администратор')),
('uth4iz@mail.com', '2L6KZG', 'Сазонов Руслан Германович', 
    (SELECT id FROM roles WHERE role_name='Администратор')),
('yzls62@outlook.com', 'JlFRCZ', 'Одинцов Серафим Артёмович', 
    (SELECT id FROM roles WHERE role_name='Администратор')),

-- Менеджеры
('1diph5e@tutanota.com', '8ntwUp', 'Степанов Михаил Артёмович', 
    (SELECT id FROM roles WHERE role_name='Менеджер')),
('tjde7c@yahoo.com', 'YOyhfR', 'Ворсин Петр Евгеньевич', 
    (SELECT id FROM roles WHERE role_name='Менеджер')),
('wpmrc3do@tutanota.com', 'RSbvHv', 'Старикова Елена Павловна', 
    (SELECT id FROM roles WHERE role_name='Менеджер')),

-- Авторизированные клиенты
('5d4zbu@tutanota.com', 'rwVDh9', 'Михайлюк Анна Вячеславовна', 
    (SELECT id FROM roles WHERE role_name='Авторизированный клиент')),
('ptec8ym@yahoo.com', 'LdNyos', 'Ситдикова Елена Анатольевна', 
    (SELECT id FROM roles WHERE role_name='Авторизированный клиент')),
('1qz4kw@mail.com', 'gynQMT', 'Ворсин Петр Евгеньевич', 
    (SELECT id FROM roles WHERE role_name='Авторизированный клиент')),
('4np6se@mail.com', 'AtnDjr', 'Старикова Елена Павловна', 
    (SELECT id FROM roles WHERE role_name='Авторизированный клиент'));

