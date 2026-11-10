from configparser import ConfigParser
from pathlib import Path


CONFIG_FILE = Path(__file__).resolve().with_name("config.ini")

_config = ConfigParser()
if not _config.read(CONFIG_FILE, encoding="utf-8"):
    raise FileNotFoundError(
        f"Не найден файл настроек БД: {CONFIG_FILE}. "
        "Скопируйте config.ini.example в config.ini и укажите параметры подключения."
    )

if "database" not in _config:
    raise ValueError(f"В файле {CONFIG_FILE} отсутствует секция [database].")

_db = _config["database"]

try:
    DB_SETTINGS = {
        "host": _db["host"],
        "database": _db["name"],
        "user": _db["user"],
        "password": _db["password"],
        "port": _db.getint("port"),
    }
except (KeyError, ValueError) as error:
    raise ValueError(
        f"Некорректные параметры подключения в {CONFIG_FILE}. "
        "Проверьте host, port, name, user и password."
    ) from error
