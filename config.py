import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings

_ENV = os.getenv("ENV", "local")
print(_ENV)
_ENV_FILE = Path(__file__).parent / "config" / f".env.{_ENV}"


class Settings(BaseSettings):
    ENV: str
    BASE_API_URL: str = Field(alias="BASE_API_URL")
    AUTH_KEY: str
    BASE_UI_URL: str
    BROWSER: str

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        # cli_parse_args=True,
        extra="ignore"
    )

settings = Settings()


