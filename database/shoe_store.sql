-- ВАЖНО: исходный build.sql содержит DROP TABLE / DROP SEQUENCE.
-- Скрипт рассчитан на пустую учебную БД. Повторный запуск удалит
-- существующие таблицы и данные. Перед запуском в непустой БД
-- необходимо сделать резервную копию и проверить последствия.

BEGIN;

-- Схема (из sql_builds/build.sql)
DROP TABLE IF EXISTS public.orders CASCADE;
DROP TABLE IF EXISTS public.pvz CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.suppliers CASCADE;
DROP TABLE IF EXISTS public.roles CASCADE;

DROP SEQUENCE IF EXISTS public.users_id_seq;
DROP SEQUENCE IF EXISTS public.products_id_seq;
DROP SEQUENCE IF EXISTS public.roles_id_seq;
DROP SEQUENCE IF EXISTS public.suppliers_id_seq;

CREATE SEQUENCE public.roles_id_seq START 1 INCREMENT 1;
CREATE SEQUENCE public.suppliers_id_seq START 1 INCREMENT 1;
CREATE SEQUENCE public.products_id_seq START 1 INCREMENT 1;
CREATE SEQUENCE public.users_id_seq START 1 INCREMENT 1;

CREATE TABLE public.roles (
    id integer NOT NULL DEFAULT nextval('roles_id_seq'::regclass),
    role_name character varying(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (role_name)
);

CREATE TABLE public.suppliers (
    id integer NOT NULL DEFAULT nextval('suppliers_id_seq'::regclass),
    name character varying(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE TABLE public.products (
    id integer NOT NULL DEFAULT nextval('products_id_seq'::regclass),
    name character varying(255) NOT NULL,
    category character varying(100),
    description text,
    manufacturer character varying(100),
    supplier character varying(100),
    supplier_id integer REFERENCES public.suppliers(id),
    unit character varying(50),
    price numeric(10,2) NOT NULL DEFAULT 0.00,
    stock_quantity integer NOT NULL DEFAULT 0,
    discount_percent integer NOT NULL DEFAULT 0 CHECK (discount_percent >= 0 AND discount_percent <= 100),
    image_path character varying(255),
    PRIMARY KEY (id)
);

CREATE TABLE public.users (
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    login character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    role_id integer NOT NULL REFERENCES public.roles(id) ON DELETE RESTRICT,
    PRIMARY KEY (id),
    UNIQUE (login)
);

CREATE TABLE public.pvz (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL
);

CREATE TABLE public.orders (
    id SERIAL PRIMARY KEY,
    order_number INT NOT NULL,
    items TEXT NOT NULL,
    order_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    pvz_id INT REFERENCES pvz(id),
    client_name TEXT NOT NULL,
    pickup_code INT NOT NULL,
    status VARCHAR(50) NOT NULL
);

-- Пункты выдачи (из sql_builds/pvz.sql)
INSERT INTO pvz (address) VALUES
('420151, г. Лесной, ул. Вишневая, 32'),
('125061, г. Лесной, ул. Подгорная, 8'),
('630370, г. Лесной, ул. Шоссейная, 24'),
('400562, г. Лесной, ул. Зеленая, 32'),
('614510, г. Лесной, ул. Маяковского, 47'),
('410542, г. Лесной, ул. Светлая, 46'),
('620839, г. Лесной, ул. Цветочная, 8'),
('443890, г. Лесной, ул. Коммунистическая, 1'),
('603379, г. Лесной, ул. Спортивная, 46'),
('603721, г. Лесной, ул. Гоголя, 41'),
('410172, г. Лесной, ул. Северная, 13'),
('614611, г. Лесной, ул. Молодежная, 50'),
('454311, г. Лесной, ул. Новая, 19'),
('660007, г. Лесной, ул. Октябрьская, 19'),
('603036, г. Лесной, ул. Садовая, 4'),
('394060, г. Лесной, ул. Фрунзе, 43'),
('410661, г. Лесной, ул. Школьная, 50'),
('625590, г. Лесной, ул. Коммунистическая, 20'),
('625683, г. Лесной, ул. 8 Марта'),
('450983, г. Лесной, ул. Комсомольская, 26'),
('394782, г. Лесной, ул. Чехова, 3'),
('603002, г. Лесной, ул. Дзержинского, 28'),
('450558, г. Лесной, ул. Набережная, 30'),
('344288, г. Лесной, ул. Чехова, 1'),
('614164, г. Лесной, ул. Степная, 30'),
('394242, г. Лесной, ул. Коммунистическая, 43'),
('660540, г. Лесной, ул. Солнечная, 25'),
('125837, г. Лесной, ул. Шоссейная, 40'),
('125703, г. Лесной, ул. Партизанская, 49'),
('625283, г. Лесной, ул. Победы, 46'),
('614753, г. Лесной, ул. Полевая, 35'),
('426030, г. Лесной, ул. Маяковского, 44'),
('450375, г. Лесной, ул. Клубная, 44'),
('625560, г. Лесной, ул. Некрасова, 12'),
('630201, г. Лесной, ул. Комсомольская, 17'),
('190949, г. Лесной, ул. Мичурина, 26');

-- Товары (из sql_builds/tovar.sql)
INSERT INTO products (name, unit, price, supplier, manufacturer, category, discount_percent, stock_quantity, description, image_path)
VALUES
('Ботинки', 'шт.', 4990, 'Kari', 'Kari', 'Женская обувь', 3, 6, 'Женские Ботинки демисезонные kari', '1.jpg'),
('Ботинки', 'шт.', 3244, 'Обувь для вас', 'Marco Tozzi', 'Женская обувь', 2, 13, 'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый', '2.jpg'),
('Туфли', 'шт.', 4499, 'Kari', 'Kari', 'Мужская обувь', 4, 5, 'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный', '3.jpg'),
('Ботинки', 'шт.', 5900, 'Kari', 'Рос', 'Мужская обувь', 2, 8, 'Мужские ботинки Рос-Обувь кожаные с натуральным мехом', '4.jpg'),
('Ботинки', 'шт.', 3800, 'Обувь для вас', 'Riexker', 'Мужская обувь', 2, 16, 'B3430/14 Полуботинки мужские Rieker', '5.jpg'),
('Кроссовки', 'шт.', 4100, 'Обувь для вас', 'Рос', 'Мужская обувь', 3, 6, '129615-4 Кроссовки мужские', '6.jpg'),
('Туфли', 'шт.', 2700, 'Kari', 'Marco Tozzi', 'Женская обувь', 2, 14, 'Туфли Marco Tozzi женские летние, размер 39, цвет черный', '7.jpg'),
('Полуботинки', 'шт.', 1890, 'Обувь для вас', 'Alessio Nesca', 'Женская обувь', 4, 4, 'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый', '8.jpg'),
('Туфли', 'шт.', 4300, 'Kari', 'Rieker', 'Женская обувь', 2, 6, 'Туфли Rieker женские демисезонные, размер 41, цвет коричневый', '9.jpg'),
('Туфли', 'шт.', 2800, 'Kari', 'Kari', 'Женская обувь', 3, 15, 'Туфли kari женские TR-YR-413017, размер 37, цвет: черный', '10.jpg'),
('Полуботинки', 'шт.', 2156, 'Обувь для вас', 'CROSBY', 'Мужская обувь', 3, 6, '407700/01-01 Полуботинки мужские CROSBY', NULL),
('Полуботинки', 'шт.', 1800, 'Kari', 'Kari', 'Женская обувь', 2, 14, 'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный', NULL),
('Кеды', 'шт.', 5500, 'Обувь для вас', 'CROSBY', 'Мужская обувь', 3, 0, 'Кеды Caprice мужские демисезонные, размер 42, цвет черный', NULL),
('Полуботинки', 'шт.', 2100, 'Обувь для вас', 'CROSBY', 'Мужская обувь', 2, 3, '407700/01-02 Полуботинки мужские CROSBY', NULL),
('Туфли', 'шт.', 5400, 'Обувь для вас', 'Rieker', 'Женская обувь', 4, 18, 'Туфли женские демисезонные Rieker артикул 55073-68/37', NULL),
('Ботинки', 'шт.', 6600, 'Kari', 'Kari', 'Женская обувь', 12, 9, 'Ботинки женские зимние ROMER арт. 893167-01 Черный', NULL),
('Тапочки', 'шт.', 500, 'Kari', 'Kari', 'Мужская обувь', 13, 0, 'Тапочки мужские Арт.70701-55-67син р.41', NULL),
('Ботинки', 'шт.', 2700, 'Обувь для вас', 'Rieker', 'Мужская обувь', 2, 5, 'Мужские кожаные ботинки/мужские ботинки', NULL),
('Туфли', 'шт.', 6800, 'Kari', 'CROSBY', 'Женская обувь', 15, 15, 'Туфли женские, ARGO, размер 38', NULL),
('Ботинки', 'шт.', 10200, 'Kari', 'Alessio Nesca', 'Женская обувь', 15, 9, 'Ботинки женские, ARGO, размер 40', NULL),
('Ботинки', 'шт.', 11800, 'Обувь для вас', 'Rieker', 'Женская обувь', 15, 11, 'Ботинки на молнии с декоративной пряжкой FRAU', NULL),
('Полуботинки', 'шт.', 4600, 'Kari', 'CROSBY', 'Женская обувь', 3, 13, 'Полуботинки Ботинки черные зимние, мех', NULL),
('Туфли', 'шт.', 12400, 'Kari', 'Kari', 'Женская обувь', 16, 5, 'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши', NULL),
('Тапочки', 'шт.', 9900, 'Обувь для вас', 'CROSBY', 'Мужская обувь', 17, 15, 'Мужские кожаные тапочки Профиль С.Дали', NULL),
('Полуботинки', 'шт.', 1700, 'Kari', 'Kari', 'Женская обувь', 2, 7, 'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный', NULL),
('Кроссовки', 'шт.', 2800, 'Обувь для вас', 'Rieker', 'Мужская обувь', 18, 3, 'Кроссовки мужские TOFA', NULL),
('Туфли', 'шт.', 4399, 'Обувь для вас', 'Rieker', 'Женская обувь', 3, 12, 'Туфли Rieker женские демисезонные, размер 36, цвет коричневый', NULL),
('Сапоги', 'шт.', 4699, 'Kari', 'CROSBY', 'Женская обувь', 2, 5, 'Сапоги замша Цвет: синий', NULL),
('Тапочки', 'шт.', 599, 'Kari', 'Rieker', 'Мужская обувь', 20, 2, 'Тапочки мужские син р.41', NULL),
('Ботинки', 'шт.', 2300, 'Обувь для вас', 'Rieker', 'Женская обувь', 2, 7, 'Женские Ботинки демисезонные', NULL);

-- Роли, поставщики и пользователи (из sql_builds/user_filling.sql)
INSERT INTO roles (role_name) VALUES
('Администратор'),
('Менеджер'),
('Авторизированный клиент');

INSERT INTO suppliers (name)
VALUES ('Kari'), ('Обувь для вас')
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (login, password, full_name, role_id)
VALUES
('94d5ous@gmail.com', 'uzWC67', 'Никифорова Весения Николаевна', (SELECT id FROM roles WHERE role_name='Администратор')),
('uth4iz@mail.com', '2L6KZG', 'Сазонов Руслан Германович', (SELECT id FROM roles WHERE role_name='Администратор')),
('yzls62@outlook.com', 'JlFRCZ', 'Одинцов Серафим Артёмович', (SELECT id FROM roles WHERE role_name='Администратор')),
('1diph5e@tutanota.com', '8ntwUp', 'Степанов Михаил Артёмович', (SELECT id FROM roles WHERE role_name='Менеджер')),
('tjde7c@yahoo.com', 'YOyhfR', 'Ворсин Петр Евгеньевич', (SELECT id FROM roles WHERE role_name='Менеджер')),
('wpmrc3do@tutanota.com', 'RSbvHv', 'Старикова Елена Павловна', (SELECT id FROM roles WHERE role_name='Менеджер')),
('5d4zbu@tutanota.com', 'rwVDh9', 'Михайлюк Анна Вячеславовна', (SELECT id FROM roles WHERE role_name='Авторизированный клиент')),
('ptec8ym@yahoo.com', 'LdNyos', 'Ситдикова Елена Анатольевна', (SELECT id FROM roles WHERE role_name='Авторизированный клиент')),
('1qz4kw@mail.com', 'gynQMT', 'Ворсин Петр Евгеньевич', (SELECT id FROM roles WHERE role_name='Авторизированный клиент')),
('4np6se@mail.com', 'AtnDjr', 'Старикова Елена Павловна', (SELECT id FROM roles WHERE role_name='Авторизированный клиент'));

-- Заказы (из sql_builds/orders.sql; требуют уже созданные записи pvz)
INSERT INTO orders (order_number, items, order_date, delivery_date, pvz_id, client_name, pickup_code, status) VALUES
(1, 'А112Т4, 2, F635R4, 2', '2025-02-27', '2025-04-20', 1, 'Степанов Михаил Артёмович', 901, 'Завершен'),
(2, 'H782T5, 1, G783F5, 1', '2022-09-28', '2025-04-21', 11, 'Никифорова Весения Николаевна', 902, 'Завершен'),
(3, 'J384T6, 10, D572U8, 10', '2025-03-21', '2025-04-22', 2, 'Сазонов Руслан Германович', 903, 'Завершен'),
(4, 'F572H7, 5, D329H3, 4', '2025-02-20', '2025-04-23', 11, 'Одинцов Серафим Артёмович', 904, 'Завершен'),
(5, 'А112Т4, 2, F635R4, 2', '2025-03-17', '2025-04-24', 2, 'Степанов Михаил Артёмович', 905, 'Завершен'),
(6, 'H782T5, 1, G783F5, 1', '2025-03-01', '2025-04-25', 15, 'Никифорова Весения Николаевна', 906, 'Завершен'),
(7, 'J384T6, 10, D572U8, 10', '2025-02-28', '2025-04-26', 3, 'Сазонов Руслан Германович', 907, 'Завершен'),
(8, 'F572H7, 5, D329H3, 4', '2025-03-31', '2025-04-27', 19, 'Одинцов Серафим Артёмович', 908, 'Новый'),
(9, 'B320R5, 5, G432E4, 1', '2025-04-02', '2025-04-28', 5, 'Степанов Михаил Артёмович', 909, 'Новый'),
(10, 'S213E3, 5, E482R4, 5', '2025-04-03', '2025-04-29', 19, 'Степанов Михаил Артёмович', 910, 'Новый');

COMMIT;
