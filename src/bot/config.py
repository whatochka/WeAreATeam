from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

parse_settings = SettingsConfigDict(
    env_file=str(BASE_DIR / ".env"),
    env_file_encoding="utf-8",
    extra="ignore",
)


class BotConfig(BaseSettings):
    model_config = parse_settings

    bot_token: str
    owner_id: list[int] | str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field("DEBUG")


def get_bot_config() -> BotConfig:
    return BotConfig()
