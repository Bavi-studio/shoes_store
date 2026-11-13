# shoes_store — магазин обуви

Учебное настольное приложение на Python для работы с каталогом обуви и заказами. Интерфейс реализован на **PySide6**, данные хранятся в **PostgreSQL**.

## Возможности проекта

- авторизация пользователей;
- интерфейсы для администратора, менеджера, пользователя и гостя;
- просмотр каталога обуви;
- добавление и редактирование товаров;
- просмотр и обработка заказов.

## Технологии и требования

- Python 3.10;
- PySide6;
- PostgreSQL 14;
- зависимости Python из `requirements.txt`.

> В исходном проекте используется PySide6, а не PyQt5. Замена GUI-библиотеки для контейнеризации не требуется: графическое приложение запускается в Windows, а в Docker будут размещены PostgreSQL и отдельный диагностический сервис.

## Структура репозитория

- `main.py` — точка входа приложения;
- `auth.py` — окно авторизации;
- `admin.py`, `manager.py`, `user.py`, `guest.py` — окна приложения для разных ролей;
- `add.py`, `edit_window.py` — добавление и редактирование товаров;
- `orders.py` — работа с заказами;
- `database.py` — классы доступа к PostgreSQL;
- `db_config.py` — чтение параметров подключения из локального `config.ini`;
- `config.ini.example` — образец локальной конфигурации;
- `database/shoe_store.sql` — единый SQL-скрипт создания и заполнения базы;
- `sql_builds/` — исходные SQL-файлы проекта;
- `1.jpg`–`10.jpg`, `Icon.JPG`, `picture.png` — изображения проекта.

## Установка

Создайте виртуальное окружение и установите зависимости:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Создайте локальный файл конфигурации:

```powershell
Copy-Item config.ini.example config.ini
```

Откройте `config.ini` и укажите параметры своего PostgreSQL. Файл `config.ini` содержит локальные настройки и исключён из Git.

## Подготовка базы данных

Создайте пустую базу данных с именем `shoes_shop` и настройте пользователя PostgreSQL, указанные в `config.ini`. Затем выполните SQL-скрипт из корня репозитория:

```powershell
psql -h localhost -p 5432 -U shoe_user -d shoes_shop -v ON_ERROR_STOP=1 -f database/shoe_store.sql
```

В команде замените порт и пользователя на фактические значения своей установки PostgreSQL. При запуске PostgreSQL через Docker Compose в практической работе № 12 приложение будет подключаться к опубликованному локальному порту `5433`; в этом случае укажите `port = 5433` в `config.ini`.

**Важно:** `database/shoe_store.sql` предназначен для первоначального развёртывания в пустой базе. Скрипт удаляет существующие таблицы и пересоздаёт схему. Не запускайте его повторно в базе с нужными данными без резервной копии.

## Запуск приложения

После настройки `config.ini` и подготовки базы данных выполните:

```powershell
python main.py
```

## Настройки и безопасность

- Не добавляйте `config.ini` и `.env` в Git.
- Для нового компьютера создайте `config.ini` копированием `config.ini.example` и заполните собственными значениями.
- Не храните пароли PostgreSQL в исходном коде или README.

## Постоянное хранение и сети

### Постоянное хранение данных

Для хранения данных PostgreSQL используется именованный Docker volume `db_data`, подключённый к `/var/lib/postgresql/data`. Данные сохраняются при удалении и пересоздании контейнера.

Перед изменением конфигурации рекомендуется создать резервную копию базы:

```powershell
docker compose exec db pg_dump -U shoe_user -d shoe_store -f /tmp/shoe_store_before_volume.sql
docker compose cp db:/tmp/shoe_store_before_volume.sql ./backups/shoe_store_before_volume.sql
```

Для восстановления базы из резервной копии:

```powershell
docker compose cp ./backups/shoe_store_before_volume.sql db:/tmp/restore.sql
docker compose exec db psql -v ON_ERROR_STOP=1 -U shoe_user -d shoe_store -f /tmp/restore.sql
```

### Сетевая конфигурация

Контейнеры `db` и `db-check` подключены к пользовательской сети `shoe-backend` с драйвером `bridge`.

- Контейнер `db-check` обращается к PostgreSQL по адресу `db:5432`.
- Приложение Windows подключается к PostgreSQL через `localhost:5433`.
- Порт PostgreSQL опубликован только на локальном интерфейсе `127.0.0.1`.

### Запуск и проверка

```powershell
docker compose up --build -d
docker compose ps
docker compose run --rm db-check
docker volume ls
docker network ls
```

**Важно:** команда `docker compose down -v` удаляет именованные тома проекта и может привести к потере данных PostgreSQL. Не используйте её без необходимости и предварительной резервной копии.


## Постоянное хранение и сети

### Постоянное хранение данных

Для хранения данных PostgreSQL используется именованный Docker volume `db_data`, подключённый к `/var/lib/postgresql/data`. Данные сохраняются при удалении и пересоздании контейнера.

Перед изменением конфигурации рекомендуется создать резервную копию базы:

```powershell
docker compose exec db pg_dump -U shoe_user -d shoe_store -f /tmp/shoe_store_before_volume.sql
docker compose cp db:/tmp/shoe_store_before_volume.sql ./backups/shoe_store_before_volume.sql
```

Для восстановления базы из резервной копии:

```powershell
docker compose cp ./backups/shoe_store_before_volume.sql db:/tmp/restore.sql
docker compose exec db psql -v ON_ERROR_STOP=1 -U shoe_user -d shoe_store -f /tmp/restore.sql
```

### Сетевая конфигурация

Контейнеры `db` и `db-check` подключены к пользовательской сети `shoe-backend` с драйвером `bridge`.

- Контейнер `db-check` обращается к PostgreSQL по адресу `db:5432`.
- Приложение Windows подключается к PostgreSQL через `localhost:5433`.
- Порт PostgreSQL опубликован только на локальном интерфейсе `127.0.0.1`.

### Запуск и проверка

```powershell
docker compose up --build -d
docker compose ps
docker compose run --rm db-check
docker volume ls
docker network ls
```

**Важно:** команда `docker compose down -v` удаляет именованные тома проекта и может привести к потере данных PostgreSQL. Не используйте её без необходимости и предварительной резервной копии.