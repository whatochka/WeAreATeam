from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Поднимаемся на 3 уровня вверх

load_dotenv(BASE_DIR / ".env")

_parse_settings = SettingsConfigDict(
    env_file=str(BASE_DIR / ".env"),
    env_file_encoding="utf-8",
    extra="ignore",
)


class DBConfig(BaseSettings):
    model_config = _parse_settings

    db_url: PostgresDsn


def get_db_config() -> DBConfig:
    return DBConfig()
