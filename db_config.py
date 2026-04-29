import configparser
from pathlib import Path


def load_db_config_from_authserver() -> dict:
    conf_path = Path(__file__).resolve().parent / "configs" / "authserver.conf"
    parser = configparser.ConfigParser()
    if not parser.read(conf_path, encoding="utf-8"):
        raise RuntimeError("Failed to read configs/authserver.conf")
    if "authserver" not in parser:
        raise RuntimeError("Section [authserver] not found in configs/authserver.conf")
    login_info = parser["authserver"].get("LoginDatabaseInfo")
    if not login_info:
        raise RuntimeError("LoginDatabaseInfo not found in [authserver]")
    parts = login_info.split(";")
    if len(parts) != 5:
        raise RuntimeError("Invalid LoginDatabaseInfo format in configs/authserver.conf")
    host, port, user, password, _database = parts
    return {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "database": "acore_world",
        "charset": "utf8mb4",
        "autocommit": False,
    }
