-- Скрипт создания БД без заполнения данных

-- 1. ОЧИСТКА СУЩЕСТВУЮЩИХ ОБЪЕКТОВ
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

-- 2. СОЗДАНИЕ ПОСЛЕДОВАТЕЛЬНОСТЕЙ
CREATE SEQUENCE public.roles_id_seq START 1 INCREMENT 1;
CREATE SEQUENCE public.suppliers_id_seq START 1 INCREMENT 1;
CREATE SEQUENCE public.products_id_seq START 1 INCREMENT 1;
CREATE SEQUENCE public.users_id_seq START 1 INCREMENT 1;

-- 3. СОЗДАНИЕ ТАБЛИЦ
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
