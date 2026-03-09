CREATE TABLE IF NOT EXISTS products (
    -- Основной идентификатор
    id SERIAL PRIMARY KEY,
    
    -- Обязательные поля
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    
    -- Опциональные/дополнительные поля
    description TEXT,
    manufacturer VARCHAR(100),
    supplier VARCHAR(100),
    unit VARCHAR(50),
    image TEXT,

    -- Числовые поля
    stock_quantity INTEGER DEFAULT 0,
    discount_percent INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    -- Пароль должен храниться в виде хеша (например, SHA-256)
    password_hash VARCHAR(255) NOT NULL, 
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    
    -- Пример: можно добавить поле для имени
    full_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL, 
    
    -- ИЗМЕНЕНИЕ: Полное имя/информация для отображения в интерфейсе
    full_name VARCHAR(150) NOT NULL, 


    -- 1. Создание таблицы для определения ролей
CREATE TABLE Roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Вставка предопределенных ролей
INSERT INTO Roles (role_name) VALUES 
('Администратор'), 
('Менеджер'), 
('Клиент')
ON CONFLICT (role_name) DO NOTHING;

-- 3. Добавление внешнего ключа (FOREIGN KEY) в таблицу Users
--    Предполагается, что ваша таблица с пользователями называется Users
--    Если у вас уже есть колонка 'role' (VARCHAR), ее нужно удалить/переименовать перед этим шагом
ALTER TABLE Users RENAME COLUMN role TO old_role_name;

ALTER TABLE Users ADD COLUMN role_id INTEGER;

-- 4. Установка внешнего ключа для связи с таблицей Roles
--    Эта связь гарантирует, что каждый пользователь имеет одну из трех допустимых ролей.
ALTER TABLE Users 
ADD CONSTRAINT fk_role
FOREIGN KEY (role_id) 
REFERENCES Roles (id)
ON UPDATE CASCADE 
ON DELETE RESTRICT;

-- 5. Миграция старых данных (если необходимо)
--    Если у вас были пользователи со старыми текстовыми ролями,
--    этот шаг обновит их role_id на основе существующих имен:
UPDATE Users
SET role_id = R.id
FROM Roles R
WHERE Users.old_role_name = R.role_name;

-- 6. Очистка (удаление старой колонки с текстовой ролью)
ALTER TABLE Users 
DROP COLUMN old_role_name;




    
    role VARCHAR(50) NOT NULL DEFAULT 'user'
);





CREATE TABLE IF NOT EXISTS suppliers (
    -- Уникальный идентификатор поставщика, первичный ключ
    id SERIAL PRIMARY KEY,
    -- Имя поставщика. Должно быть уникальным и не пустым.
    name VARCHAR(255) UNIQUE NOT NULL
);



